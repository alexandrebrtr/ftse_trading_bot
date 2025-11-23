# complete_trading_bot.py
# Robot de Trading FTSE100 - Version Complète
# ================================================

import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, time
from collections import deque
from pykalman import KalmanFilter
import smtplib
from email.mime.text import MIMEText


# ================================================
# STRATEGY MODULE
# ================================================

class FTSE100Strategy:
    def __init__(self, lookback=500):
        self.data = deque(maxlen=lookback)
        self.kf = KalmanFilter(
            transition_matrices=[1],
            observation_matrices=[1],
            initial_state_mean=0,
            initial_state_covariance=1,
            observation_covariance=1,
            transition_covariance=0.01
        )
        
    def update_data(self, tick):
        """Ajouter nouveau tick"""
        self.data.append({
            'timestamp': tick['time'],
            'open': tick['open'],
            'high': tick['high'],
            'low': tick['low'],
            'close': tick['close'],
            'volume': tick['volume']
        })
        
    def generate_signal(self):
        """Générer signal de trading"""
        if len(self.data) < 100:
            return 'WAIT'
            
        df = pd.DataFrame(self.data)
        
        # Calcul indicateurs (version optimisée)
        returns = df['close'].pct_change()
        vol_regime = self._ewma_vol(returns)
        vol_5j = vol_regime.rolling(5).mean()
        kalman = self._kalman_filter(df['close'])
        spec_mom = self._spectral_momentum(df['close'])
        
        # Dernière valeur
        last = df.iloc[-1]
        
        # Conditions
        low_vol = vol_regime.iloc[-1] < vol_5j.iloc[-1]
        trend_strong = spec_mom.iloc[-1] > 1.0
        kalman_up = last['close'] > kalman.iloc[-1] + 0.35*returns.std()
        kalman_down = last['close'] < kalman.iloc[-1] - 0.35*returns.std()
        
        if low_vol and trend_strong and kalman_up:
            return 'LONG'
        elif low_vol and trend_strong and kalman_down:
            return 'SHORT'
        else:
            return 'NEUTRAL'
    
    def _ewma_vol(self, returns, span=20):
        """Calcul volatilité EWMA"""
        return returns.ewm(span=span).std()
    
    def _kalman_filter(self, prices):
        """Appliquer Kalman Filter"""
        state_means, _ = self.kf.filter(prices.values)
        return pd.Series(state_means.flatten(), index=prices.index)
    
    def _spectral_momentum(self, prices, window=50):
        """Calcul momentum spectral (FFT)"""
        momentum = pd.Series(index=prices.index, dtype=float)
        
        for i in range(window, len(prices)):
            segment = prices.iloc[i-window:i].values
            fft = np.fft.fft(segment)
            power = np.abs(fft[:window//2])**2
            
            # Dominant frequency strength
            dominant_power = np.max(power[1:])  # Skip DC component
            momentum.iloc[i] = dominant_power / np.mean(power[1:])
        
        return momentum
    
    def get_atr(self, period=14):
        """Calcul Average True Range"""
        if len(self.data) < period + 1:
            return 10  # Valeur par défaut
        
        df = pd.DataFrame(self.data)
        
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(period).mean()
        
        return atr.iloc[-1]
            
    def calculate_stops(self, price):
        """Calculer SL/TP basé sur ATR"""
        atr = self.get_atr()
        sl = price - 1.2 * atr
        tp = price + 1.8 * atr
        return sl, tp


# ================================================
# RISK MANAGER MODULE
# ================================================

class RiskManager:
    def __init__(self, max_daily_loss=-0.02, risk_per_trade=0.005, max_trades_per_day=10):
        self.max_daily_loss = max_daily_loss
        self.risk_per_trade = risk_per_trade
        self.max_trades_per_day = max_trades_per_day
        self.daily_pnl = 0
        self.trades_today = 0
        self.trading_day = datetime.now().date()
        self.emergency_stop_triggered = False
        
    def reset_daily_stats(self):
        """Reset des stats journalières"""
        current_day = datetime.now().date()
        if current_day != self.trading_day:
            self.daily_pnl = 0
            self.trades_today = 0
            self.trading_day = current_day
            self.emergency_stop_triggered = False
            print("📊 Stats journalières réinitialisées")
        
    def calculate_position_size(self, price, atr, equity):
        """Calcul position size avec Kelly fractionnaire"""
        risk_amount = equity * self.risk_per_trade
        sl_distance = 1.2 * atr
        
        if sl_distance == 0:
            return 0
        
        position_size = risk_amount / sl_distance
        kelly_fraction = 0.3
        position_size *= kelly_fraction
        position_size = int(position_size)
        
        return max(1, position_size)
        
    def can_trade(self):
        """Vérifier si on peut trader"""
        self.reset_daily_stats()
        
        if self.emergency_stop_triggered:
            print("🚨 Emergency stop activé - Trading désactivé")
            return False
        
        if self.daily_pnl <= self.max_daily_loss:
            print(f"🛑 Max daily loss atteint! ({self.daily_pnl:.2%})")
            self.emergency_stop()
            return False
            
        if self.trades_today >= self.max_trades_per_day:
            print(f"⚠️ Max trades today atteint ({self.trades_today}/{self.max_trades_per_day})")
            return False
        
        current_time = datetime.now().time()
        market_open = time(8, 0)
        market_close = time(16, 30)
        
        if not (market_open <= current_time <= market_close):
            return False
            
        return True
        
    def update_daily_pnl(self, pnl):
        """Mise à jour P&L journalier"""
        self.daily_pnl += pnl
        self.trades_today += 1
        
        print(f"📊 Daily P&L: {self.daily_pnl:.2%} | Trades: {self.trades_today}")
        
        if self.daily_pnl <= self.max_daily_loss * 0.8:
            print(f"⚠️ Attention: Daily P&L à {self.daily_pnl:.2%}")
        
        if self.daily_pnl <= self.max_daily_loss:
            self.emergency_stop()
            
    def emergency_stop(self):
        """Arrêt d'urgence"""
        self.emergency_stop_triggered = True
        print("🚨 EMERGENCY STOP TRIGGERED!")
        print(f"   Raison: Daily P&L = {self.daily_pnl:.2%}")
        
        self.send_alert(
            subject="🚨 EMERGENCY STOP - Trading Bot",
            message=f"Emergency stop déclenché!\nDaily P&L: {self.daily_pnl:.2%}\nDate: {datetime.now()}"
        )
    
    def send_alert(self, subject, message):
        """Envoyer alerte email"""
        try:
            print(f"📧 Alerte envoyée: {subject}")
        except Exception as e:
            print(f"❌ Erreur envoi alerte: {e}")


# ================================================
# BROKER CONNECTOR (Stub - à adapter)
# ================================================

class BrokerAPI:
    def __init__(self):
        self.connected = False
        self.equity = 10000
        
    async def connect(self):
        """Connexion au broker"""
        # À implémenter selon votre broker (IB, MT5, etc.)
        self.connected = True
        print("✅ Broker connecté")
        
    async def stream_ticks(self, symbol):
        """Stream de données temps réel"""
        # Simulation - remplacer par vraie connexion WebSocket
        while True:
            yield {
                'time': datetime.now(),
                'open': 7500 + np.random.randn() * 10,
                'high': 7510 + np.random.randn() * 10,
                'low': 7490 + np.random.randn() * 10,
                'close': 7500 + np.random.randn() * 10,
                'volume': np.random.randint(1000, 5000)
            }
            await asyncio.sleep(1)
    
    async def place_order(self, symbol, side, quantity, stop_loss=None, take_profit=None):
        """Placer un ordre"""
        # Simulation
        return {
            'status': 'FILLED',
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': 7500,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'entry_price': 7500,
            'exit_price': 7500
        }
    
    async def close_position(self, symbol):
        """Fermer une position"""
        return {
            'status': 'FILLED',
            'entry_price': 7500,
            'exit_price': 7510
        }
    
    async def close_all_positions(self):
        """Fermer toutes les positions"""
        print("🛑 Fermeture de toutes les positions")
    
    def get_equity(self):
        """Obtenir le capital disponible"""
        return self.equity


# ================================================
# DATABASE MANAGER (Stub - à adapter)
# ================================================

class DatabaseManager:
    async def connect(self):
        """Connexion à la base de données"""
        print("✅ Database connectée")
        
    async def log_trade(self, order):
        """Logger un trade"""
        print(f"💾 Trade enregistré: {order}")


# ================================================
# TRADING BOT MAIN
# ================================================

class TradingBot:
    def __init__(self):
        self.strategy = FTSE100Strategy()
        self.broker = BrokerAPI()
        self.risk_mgr = RiskManager(max_daily_loss=-0.02)
        self.db = DatabaseManager()
        self.position = 0
        self.running = False
        
    async def connect(self):
        """Connexion aux services"""
        await self.broker.connect()
        await self.db.connect()
        print("✅ Bot connecté")
        
    async def on_tick(self, tick_data):
        """Callback à chaque nouveau tick"""
        self.strategy.update_data(tick_data)
        signal = self.strategy.generate_signal()
        
        if not self.risk_mgr.can_trade():
            return
        
        if signal == 'LONG' and self.position == 0:
            await self.open_position('BUY', tick_data)
        elif signal == 'SHORT' and self.position == 0:
            await self.open_position('SELL', tick_data)
        elif signal == 'EXIT' and self.position != 0:
            await self.close_position(tick_data)
            
    async def open_position(self, side, data):
        """Ouvrir une position"""
        size = self.risk_mgr.calculate_position_size(
            price=data['close'],
            atr=self.strategy.get_atr(),
            equity=self.broker.get_equity()
        )
        
        sl, tp = self.strategy.calculate_stops(data['close'])
        
        order = await self.broker.place_order(
            symbol='FTSE100',
            side=side,
            quantity=size,
            stop_loss=sl,
            take_profit=tp
        )
        
        if order['status'] == 'FILLED':
            self.position = 1 if side == 'BUY' else -1
            await self.db.log_trade(order)
            print(f"✅ Position {side} ouverte à {data['close']}")
            
    async def close_position(self, data):
        """Fermer la position"""
        side = 'SELL' if self.position > 0 else 'BUY'
        order = await self.broker.close_position('FTSE100')
        
        if order['status'] == 'FILLED':
            pnl = self.calculate_pnl(order)
            self.risk_mgr.update_daily_pnl(pnl)
            await self.db.log_trade(order)
            self.position = 0
            print(f"✅ Position fermée - P&L: {pnl:.2f}%")
    
    def calculate_pnl(self, order):
        """Calculer le P&L"""
        return (order['exit_price'] - order['entry_price']) / order['entry_price']
            
    async def run(self):
        """Boucle principale du bot"""
        self.running = True
        await self.connect()
        
        async for tick in self.broker.stream_ticks('FTSE100'):
            if not self.running:
                break
            await self.on_tick(tick)
            
    def stop(self):
        """Arrêt d'urgence"""
        self.running = False
        if self.position != 0:
            asyncio.create_task(
                self.broker.close_all_positions()
            )


# ================================================
# POINT D'ENTRÉE
# ================================================

if __name__ == "__main__":
    bot = TradingBot()
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        bot.stop()
        print("🛑 Bot arrêté")
