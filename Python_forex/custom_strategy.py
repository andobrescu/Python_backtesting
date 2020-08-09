import backtrader as bt
import numpy as np
from configuration import parameters
from money_management import forex_risk_calculator
from ta.volatility import average_true_range

class TestStrategy_SMA_Basic(bt.Strategy):
	params = (
		('maperiod', 15),
	)

	def log(self, txt, dt=None):
		''' Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print(f'{dt.isoformat()}, {txt}')

	def __init__(self):
		# Keep a reference to the "close" line in the data[0] dataseries
		self.dataclose = self.datas[0].close
		self.dataopen = self.datas[0].open

		
		
		#print(np.array(self.datas))
		#print(np.array(self.dataclose))

		# To keep track of pending orders and buy price/commission
		self.order = None
		self.buyprice = None
		self.buycomm = None

		print(len(self.dataclose))
		self.config = parameters()
		self.counter = 0
		self.trade_mode = self.config['trading_mode']
		# Add a MovingAverageSimple indicator
		self.sma = bt.indicators.SimpleMovingAverage(
			self.datas[0], period=self.params.maperiod)
		
		self.atr = bt.indicators.ATR(self.datas[0], period=14 ,plot=True)
		bt.indicators.ExponentialMovingAverage(self.datas[0], period=25, plot=False)

	def notify_order(self, order):
		if order.status in [order.Submitted, order.Accepted]:
			# Buy/Sell order submitted/accepted to/by broker - Nothing to do
			return

		# Check if an order has been completed
		# Attention: broker could reject order if not enough cash
		if order.status in [order.Completed]:
			if order.isbuy():
				self.log(
					'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
					(order.executed.price,
					 order.executed.value,
					 order.executed.comm))

				self.buyprice = order.executed.price
				self.buycomm = order.executed.comm
			else:  # Sell
				self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
						 (order.executed.price,
						  order.executed.value,
						  order.executed.comm))

			self.bar_executed = len(self)

		elif order.status in [order.Canceled, order.Margin, order.Rejected]:
			self.log('Order Canceled/Margin/Rejected')

		#self.params['account_balance'] = 

		self.order = None

	def notify_trade(self, trade):
		if not trade.isclosed:
			return

		self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
				 (trade.pnl, trade.pnlcomm))
		self.log(f'cash in account {self.broker.getcash()}')
		self.log(f'value of account {self.broker.getvalue()}')
		
		#cash = self.broker.getcash()
		#value = self.broker.getvalue()

	def next(self):
		# Simply log the closing price of the series from the reference
		self.log('Close, %.4f' % self.dataclose[0])
		
		self.counter += 1
		self.config['price'] = self.dataclose[0]
		pair = self.config['target_symbol']

		# Check if an order is pending ... if yes, we cannot send a 2nd one
		if self.order:
			return

		# Check if we are in the market
		if not self.position:

			# Not yet ... we MIGHT BUY if ...
			if self.dataclose[0] > self.sma[0]:

				self.config['order'] = 'buy' 
				self.config['price'] = self.dataopen[0]
				self.config['atr'] = self.atr[0] * 10**4
				self.config['base_currency_price'] = self.dataopen[0]
				trade_config = self.trade_params()
				self.stop_loss = trade_config[3]
				# base, target, order, price, base_price, risk, atr, balance
				#pong = np.where(self.dataclose == self.dataclose[0])
				#print(pong)
				# BUY, BUY, BUY!!! (with all possible default parameters)
				self.log('BUY CREATE, %.4f' % self.dataclose[0])

				# Keep track of the created order to avoid a 2nd order
				#self.params['order'] = 'buy'
				self.order = self.buy()

		else:

			if self.dataclose[0] < self.sma[0]:
				# SELL, SELL, SELL!!! (with all possible default parameters)
				self.log('SELL CREATE, %.4f' % self.dataclose[0])

				# Keep track of the created order to avoid a 2nd order
				self.order = self.sell()

	def trade_params(self):
		
		base = self.config['account_base']
		target = self.config['target_symbol']
		order = self.config['order']
		balance = self.config['account_balance']
		risk = self.config['risk_per_trade']

		if self.trade_mode == 'forex':
			pair = self.config['target_symbol']
			counter_currency = pair[4:]
			quote_currency = pair[:3]

			price = self.config['price']

			if base not in pair:
				base_price = self.config['base_currency_price']
			else:
				base_price = self.config['price']

		else:
			print('I can only do forex at the moment')
			return
		
		atr = self.config['atr']
		print(target, order, price, base_price, risk, atr, balance)
		specs = forex_risk_calculator(base, target, order, price, base_price, risk, atr, balance)
		trade_specs = specs.basic_calc()

		return trade_specs
