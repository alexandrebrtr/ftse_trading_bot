import React, { useState } from 'react';
import { Activity, Database, Zap, Shield, BarChart3, Settings, AlertTriangle, CheckCircle2, Clock, TrendingUp } from 'lucide-react';

const TradingBotGuide = () => {
  const [activeTab, setActiveTab] = useState('architecture');

  const tabs = [
    { id: 'architecture', label: 'Architecture', icon: Activity },
    { id: 'code', label: 'Code Live', icon: Zap },
    { id: 'broker', label: 'Connexion Broker', icon: Database },
    { id: 'risk', label: 'Risk Management', icon: Shield },
    { id: 'deployment', label: 'Déploiement', icon: Settings }
  ];

  return (
    <div className="w-full max-w-6xl mx-auto p-6 bg-gradient-to-br from-slate-900 to-slate-800 rounded-xl shadow-2xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
          <TrendingUp className="text-green-400" />
          Robot Trading FTSE100 - Guide Complet
        </h1>
        <p className="text-slate-300">De la stratégie au bot en production</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {tabs.map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              <Icon size={18} />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Content */}
      <div className="bg-slate-800 rounded-lg p-6 text-slate-100">
        {activeTab === 'architecture' && <ArchitectureTab />}
        {activeTab === 'code' && <CodeTab />}
        {activeTab === 'broker' && <BrokerTab />}
        {activeTab === 'risk' && <RiskTab />}
        {activeTab === 'deployment' && <DeploymentTab />}
      </div>
    </div>
  );
};

const ArchitectureTab = () => (
  <div className="space-y-6">
    <h2 className="text-2xl font-bold text-white mb-4">Architecture du Robot</h2>
    
    <div className="grid md:grid-cols-2 gap-4">
      <div className="bg-slate-700 p-4 rounded-lg">
        <h3 className="font-bold text-green-400 mb-2 flex items-center gap-2">
          <CheckCircle2 size={20} />
          Composants Essentiels
        </h3>
        <ul className="space-y-2 text-sm">
          <li>✅ <strong>Data Feed</strong> : Récupération temps réel (WebSocket)</li>
          <li>✅ <strong>Strategy Engine</strong> : Calculs indicateurs + signaux</li>
          <li>✅ <strong>Order Manager</strong> : Exécution des trades</li>
          <li>✅ <strong>Risk Controller</strong> : Validation pré-trade</li>
          <li>✅ <strong>Database</strong> : Historique + logs</li>
          <li>✅ <strong>Monitoring</strong> : Dashboard + alertes</li>
        </ul>
      </div>

      <div className="bg-slate-700 p-4 rounded-lg">
        <h3 className="font-bold text-yellow-400 mb-2 flex items-center gap-2">
          <AlertTriangle size={20} />
          Points Critiques
        </h3>
        <ul className="space-y-2 text-sm">
          <li>⚠️ <strong>Latence</strong> : &lt;100ms pour data feed</li>
          <li>⚠️ <strong>Reconnexion</strong> : Auto-reconnect broker</li>
          <li>⚠️ <strong>Kill Switch</strong> : Arrêt d'urgence manuel</li>
          <li>⚠️ <strong>Position Sync</strong> : Vérification état réel</li>
          <li>⚠️ <strong>Logs</strong> : Traçabilité complète</li>
          <li>⚠️ <strong>Backup Data</strong> : Pas de perte de données</li>
        </ul>
      </div>
    </div>

    <div className="bg-blue-900 bg-opacity-30 border border-blue-500 rounded-lg p-4">
      <h3 className="font-bold text-blue-300 mb-3">🔄 Pipeline de Données</h3>
      <div className="flex items-center gap-2 text-sm overflow-x-auto pb-2">
        <div className="bg-slate-700 px-3 py-2 rounded whitespace-nowrap">Broker WebSocket</div>
        <span>→</span>
        <div className="bg-slate-700 px-3 py-2 rounded whitespace-nowrap">Data Parser</div>
        <span>→</span>
        <div className="bg-slate-700 px-3 py-2 rounded whitespace-nowrap">Indicator Engine</div>
        <span>→</span>
        <div className="bg-slate-700 px-3 py-2 rounded whitespace-nowrap">Signal Generator</div>
        <span>→</span>
        <div className="bg-slate-700 px-3 py-2 rounded whitespace-nowrap">Risk Check</div>
        <span>→</span>
        <div className="bg-green-700 px-3 py-2 rounded whitespace-nowrap">Order Execution</div>
      </div>
    </div>

    <div className="bg-slate-700 p-4 rounded-lg">
      <h3 className="font-bold mb-3">📊 Technologies Recommandées</h3>
      <div className="grid grid-cols-2 gap-3 text-sm">
        <div><strong className="text-green-400">Langage:</strong> Python 3.10+</div>
        <div><strong className="text-green-400">Broker API:</strong> Interactive Brokers / MetaTrader 5</div>
        <div><strong className="text-green-400">Data:</strong> pandas, numpy</div>
        <div><strong className="text-green-400">Base de données:</strong> PostgreSQL / InfluxDB</div>
        <div><strong className="text-green-400">WebSocket:</strong> websockets / asyncio</div>
        <div><strong className="text-green-400">Monitoring:</strong> Grafana / Prometheus</div>
      </div>
    </div>
  </div>
);

const CodeTab = () => (
  <div className="space-y-4">
    <h2 className="text-2xl font-bold text-white mb-4">Code du Robot Live</h2>
    
    <div className="bg-slate-900 p-4 rounded-lg">
      <h3 className="font-bold text-yellow-400 mb-3">⚡ Structure Principale</h3>
      <pre className="text-xs overflow-x-auto text-green-300">
{`# trading_bot.py
import asyncio
import pandas as pd
from datetime import datetime
from strategy import FTSE100Strategy
from broker_connector import BrokerAPI
from risk_manager import RiskManager
from database import DatabaseManager

class TradingBot:
    def __init__(self):
        self.strategy = FTSE100Strategy()
        self.broker = BrokerAPI()
        self.risk_mgr = RiskManager(max_daily_loss=-0.02)
        self.db = DatabaseManager()
        self.position = 0
        self.running = False
        
    async def connect(self):
        await self.broker.connect()
        await self.db.connect()
        print("✅ Bot connecté")
        
    async def on_tick(self, tick_data):
        """Callback à chaque nouveau tick"""
        # 1. Mise à jour des données
        self.strategy.update_data(tick_data)
        
        # 2. Calcul des indicateurs
        signal = self.strategy.generate_signal()
        
        # 3. Vérification risk management
        if not self.risk_mgr.can_trade():
            return
        
        # 4. Exécution si signal valide
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
            
    async def run(self):
        """Boucle principale du bot"""
        self.running = True
        await self.connect()
        
        async for tick in self.broker.stream_ticks('FTSE100'):
            if not self.running:
                break
            await self.on_tick(tick)

if __name__ == "__main__":
    bot = TradingBot()
    asyncio.run(bot.run())`}
      </pre>
    </div>

    <div className="bg-slate-900 p-4 rounded-lg">
      <h3 className="font-bold text-blue-400 mb-3">📈 Strategy Module</h3>
      <pre className="text-xs overflow-x-auto text-blue-300">
{`# strategy.py
import pandas as pd
import numpy as np
from collections import deque

class FTSE100Strategy:
    def __init__(self, lookback=500):
        self.data = deque(maxlen=lookback)
        self.kf = KalmanFilter()
        
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
        
        # Calcul indicateurs
        returns = df['close'].pct_change()
        vol_regime = self._ewma_vol(returns)
        vol_5j = vol_regime.rolling(5).mean()
        kalman = self._kalman_filter(df['close'])
        spec_mom = self._spectral_momentum(df['close'])
        
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
            
    def calculate_stops(self, price):
        """Calculer SL/TP basé sur ATR"""
        atr = self.get_atr()
        sl = price - 1.2 * atr
        tp = price + 1.8 * atr
        return sl, tp`}
      </pre>
    </div>
  </div>
);

const BrokerTab = () => (
  <div className="space-y-4">
    <h2 className="text-2xl font-bold text-white mb-4">Connexion aux Brokers</h2>
    
    <div className="grid md:grid-cols-2 gap-4">
      <div className="bg-slate-700 p-4 rounded-lg">
        <h3 className="font-bold text-green-400 mb-3">🏦 Interactive Brokers (Recommandé)</h3>
        <div className="space-y-2 text-sm">
          <p><strong>Avantages:</strong></p>
          <ul className="list-disc list-inside space-y-1 text-slate-300">
            <li>API Python officielle (ib_insync)</li>
            <li>Données temps réel gratuites</li>
            <li>Frais très bas (0.08% FTSE100)</li>
            <li>Capital minimum: 10 000 USD</li>
          </ul>
          <div className="bg-slate-900 p-2 rounded mt-2">
            <code className="text-xs text-green-300">
              pip install ib_insync
            </code>
          </div>
        </div>
      </div>

      <div className="bg-slate-700 p-4 rounded-lg">
        <h3 className="font-bold text-blue-400 mb-3">📊 MetaTrader 5</h3>
        <div className="space-y-2 text-sm">
          <p><strong>Avantages:</strong></p>
          <ul className="list-disc list-inside space-y-1 text-slate-300">
            <li>Populaire pour CFD FTSE100</li>
            <li>API Python MetaTrader5</li>
            <li>Capital minimum: 500-1000€</li>
            <li>Backtesting intégré</li>
          </ul>
          <div className="bg-slate-900 p-2 rounded mt-2">
            <code className="text-xs text-blue-300">
              pip install MetaTrader5
            </code>
          </div>
        </div>
      </div>
    </div>

    <div className="bg-slate-900 p-4 rounded-lg">
      <h3 className="font-bold text-yellow-400 mb-3">🔌 Exemple: Connexion IB</h3>
      <pre className="text-xs overflow-x-auto text-yellow-300">
{`from ib_insync import IB, Stock, MarketOrder

class IBConnector:
    def __init__(self):
        self.ib = IB()
        
    async def connect(self):
        self.ib.connect('127.0.0.1', 7497, clientId=1)
        print("✅ Connecté à Interactive Brokers")
        
    async def stream_ticks(self, symbol):
        contract = Stock(symbol, 'LSE', 'GBP')
        self.ib.reqMktData(contract)
        
        async for tick in self.ib.pendingTickersEvent:
            yield {
                'time': tick.time,
                'close': tick.last,
                'bid': tick.bid,
                'ask': tick.ask,
                'volume': tick.volume
            }
            
    async def place_order(self, symbol, side, quantity):
        contract = Stock(symbol, 'LSE', 'GBP')
        order = MarketOrder(side, quantity)
        trade = self.ib.placeOrder(contract, order)
        
        while not trade.isDone():
            await asyncio.sleep(0.1)
            
        return {
            'status': 'FILLED',
            'price': trade.orderStatus.avgFillPrice,
            'quantity': quantity
        }`}
      </pre>
    </div>
  </div>
);

const RiskTab = () => (
  <div className="space-y-4">
    <h2 className="text-2xl font-bold text-white mb-4">Risk Management</h2>
    
    <div className="bg-red-900 bg-opacity-30 border border-red-500 rounded-lg p-4">
      <h3 className="font-bold text-red-300 mb-3 flex items-center gap-2">
        <AlertTriangle />
        Règles Critiques - NON NÉGOCIABLES
      </h3>
      <ul className="space-y-2 text-sm">
        <li>🛑 <strong>Max Daily Loss:</strong> -2% du capital → STOP trading</li>
        <li>🛑 <strong>Max Position Size:</strong> 0.5% risk par trade</li>
        <li>🛑 <strong>Max Drawdown:</strong> -15% → Review stratégie</li>
        <li>🛑 <strong>Kill Switch:</strong> Bouton arrêt accessible 24/7</li>
        <li>🛑 <strong>No Trading:</strong> Pendant annonces BoE, NFP, FOMC</li>
      </ul>
    </div>

    <div className="bg-slate-900 p-4 rounded-lg">
      <h3 className="font-bold text-green-400 mb-3">💰 Position Sizing (Kelly Criterion)</h3>
      <pre className="text-xs overflow-x-auto text-green-300">
{`class RiskManager:
    def __init__(self, max_daily_loss=-0.02, risk_per_trade=0.005):
        self.max_daily_loss = max_daily_loss
        self.risk_per_trade = risk_per_trade
        self.daily_pnl = 0
        self.trades_today = 0
        
    def calculate_position_size(self, price, atr, equity):
        """Calcul position size avec Kelly fractionnaire"""
        # Risk amount en devise
        risk_amount = equity * self.risk_per_trade
        
        # Stop-loss en points
        sl_distance = 1.2 * atr
        
        # Position size = Risk / Stop Distance
        position_size = risk_amount / sl_distance
        
        # Kelly fraction (0.3 = 30% du Kelly optimal)
        kelly_fraction = 0.3
        position_size *= kelly_fraction
        
        # Arrondi au lot standard
        position_size = int(position_size)
        
        return max(1, position_size)
        
    def can_trade(self):
        """Vérifier si on peut trader"""
        # Check daily loss limit
        if self.daily_pnl <= self.max_daily_loss:
            print("🛑 Max daily loss atteint!")
            return False
            
        # Check max trades par jour
        if self.trades_today >= 10:
            print("⚠️ Max trades today atteint")
            return False
            
        return True
        
    def emergency_stop(self):
        """Arrêt d'urgence"""
        print("🚨 EMERGENCY STOP TRIGGERED!")
        # Fermer toutes positions
        # Envoyer alerte SMS/Email`}
      </pre>
    </div>
  </div>
);

const DeploymentTab = () => (
  <div className="space-y-4">
    <h2 className="text-2xl font-bold text-white mb-4">Déploiement en Production</h2>
    
    <div className="space-y-3">
      <div className="bg-slate-700 p-4 rounded-lg">
        <h3 className="font-bold text-blue-400 mb-2">1️⃣ Phase de Test (Paper Trading)</h3>
        <ul className="space-y-1 text-sm list-disc list-inside">
          <li>Utiliser compte démo broker (IB Paper Trading)</li>
          <li>Laisser tourner 1-3 mois minimum</li>
          <li>Vérifier stabilité des résultats</li>
          <li>Tester reconnexion en cas de coupure</li>
        </ul>
      </div>

      <div className="bg-slate-700 p-4 rounded-lg">
        <h3 className="font-bold text-green-400 mb-2">2️⃣ Infrastructure</h3>
        <div className="space-y-2 text-sm">
          <p><strong>Option A - VPS Trading:</strong></p>
          <ul className="list-disc list-inside ml-4 text-slate-300">
            <li>VPS spécialisé trading (Beeks, Vultr)</li>
            <li>Latence &lt;5ms vers broker</li>
            <li>Coût: 30-100€/mois</li>
          </ul>
          <p className="mt-2"><strong>Option B - Cloud (AWS/GCP):</strong></p>
          <ul className="list-disc list-inside ml-4 text-slate-300">
            <li>EC2 t3.medium ou équivalent</li>
            <li>Auto-scaling si nécessaire</li>
            <li>Coût: 50-150€/mois</li>
          </ul>
        </div>
      </div>

      <div className="bg-slate-700 p-4 rounded-lg">
        <h3 className="font-bold text-yellow-400 mb-2">3️⃣ Monitoring & Alertes</h3>
        <pre className="text-xs overflow-x-auto bg-slate-900 p-3 rounded text-yellow-300">
{`# monitoring.py
import smtplib
from telegram import Bot

class MonitoringSystem:
    def __init__(self):
        self.telegram_bot = Bot(token='YOUR_TOKEN')
        self.chat_id = 'YOUR_CHAT_ID'
        
    async def send_alert(self, message, level='INFO'):
        """Envoyer alerte Telegram"""
        emoji = '✅' if level == 'INFO' else '🚨'
        await self.telegram_bot.send_message(
            chat_id=self.chat_id,
            text=f"{emoji} {message}"
        )
        
    def check_health(self, bot):
        """Vérification santé du bot"""
        issues = []
        
        if not bot.broker.is_connected():
            issues.append("❌ Broker déconnecté")
            
        if bot.risk_mgr.daily_pnl <= -0.015:
            issues.append("⚠️ Daily loss -1.5%")
            
        if bot.position != 0 and bot.position_age > 3600:
            issues.append("⚠️ Position ouverte >1h")
            
        return issues`}
        </pre>
      </div>

      <div className="bg-slate-700 p-4 rounded-lg">
        <h3 className="font-bold text-purple-400 mb-2">4️⃣ Checklist Avant Production</h3>
        <div className="space-y-1 text-sm">
          {[
            'Backtest sur 5+ ans validé',
            'Paper trading 3 mois OK',
            'Kill switch testé et fonctionnel',
            'Alertes Telegram configurées',
            'Backup automatique données',
            'Logs centralisés',
            'Plan B en cas de panne serveur',
            'Capital suffisant (min 5000€)',
            'Commencer avec 10% du capital max'
          ].map((item, i) => (
            <div key={i} className="flex items-center gap-2">
              <CheckCircle2 size={16} className="text-green-400" />
              <span>{item}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-blue-900 bg-opacity-30 border border-blue-500 rounded-lg p-4">
        <h3 className="font-bold text-blue-300 mb-2">🚀 Commande de Démarrage</h3>
        <pre className="text-xs bg-slate-900 p-3 rounded text-blue-300">
{`# Sur VPS, utiliser screen/tmux pour persistance
screen -S ftse_bot

# Activer environnement
source venv/bin/activate

# Lancer le bot
python trading_bot.py --mode=live --capital=10000

# Détacher: Ctrl+A puis D
# Réattacher: screen -r ftse_bot`}
        </pre>
      </div>
    </div>
  </div>
);

export default TradingBotGuide;
