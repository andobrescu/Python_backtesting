import backtrader as bt
import numpy as np
from config import parameters

class Backtrader_Strategy(bt.Strategy):

	def log(self, txt, dt=None):
		''' Logging function for this strategy'''
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		# Keep a reference to the "close" line in the data[0] dataseries
		self.dataclose = self.datas[0].close

		self.params = parameters()

		# To keep track of pending orders and buy price/commission
		self.order = None
		self.buyprice = None
		self.buycomm = None


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

		self.order = None

	def notify_trade(self, trade):
		if not trade.isclosed:
			return

		self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
				 (trade.pnl, trade.pnlcomm))

	def trade_params(self):
		
		base = self.params['account_base']
		target = self.params['target_symbol']
		order = self.params['order']
		balance = self.params['account_balance']
		risk = self.params['risk_per_trade']

		if self.mode == 'forex':
			pair = self.params['target_symbol']
			counter_currency = pair[4:]
			quote_currency = pair[:3]

			price = self.params['price']

			if base not in pair:
				base_price = self.params['base_currency_price']
			else:
				base_price = self.params['price']

		else:
			print('I can only do forex at the moment')
			return
		
		atr = self.params['atr']

		trade_specs = forex_risk_calculator(self, base, target, order, price, base_price, risk, atr, balance)

		return trade_specs
