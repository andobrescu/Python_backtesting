import backtrader as bt
import numpy as np
from configuration import parameters
from data_reader import load_data
from money_management import forex_risk_calculator

class Backtrader_Strategy(bt.Strategy):

	def log(self, txt, dt=None):
		# Logging function for this strategy
		dt = dt or self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self):
		# Keep a reference to the "close" line in the data[0] dataseries
		self.dataclose = self.datas[0].close
		self.dataopen = self.datas[0].open

		self.config = parameters()
		self.data_path = self.config['data_path']

		base_price_needed = False

		# Get all the data for currency conversion if the target pair does not contain your account currency. TODO Should change how this is done
		if self.config['trading_mode'] == 'forex':
			if self.config['account_base'] not in self.config['target_symbol']:
				self.config['base_target_symbol'] = self.config['account_base'] + '_' + self.config['target_symbol'][4:]
				data_loader = load_data(self.config)

				self.all_symbols, self.all_data = data_loader.load_all_data()

				self.base_symbol_data = data_loader.load_symbol(self.all_data, self.all_symbols, self.config['base_target_symbol'])

				self.target_symbol_data = data_loader.load_symbol(self.all_data, self.all_symbols, self.config['target_symbol'])

				base_price_needed = True
				print('ping pong long')


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

				self.config['order'] = 'buy' 
				self.config['price'] = self.dataopen[0]
				self.config['atr'] = self.atr[0] * 10**4
				self.config['base_currency_price'] = self.dataopen[0]
				trade_config = self.trade_parameters()
				trade_parameters = trade_config.basic_calc()
				self.stop_loss = trade_parameters[3]

				self.log(f'Stop loss should be placed at {self.stop_loss}')

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
		#Function to notify the outcome of a trade
		if not trade.isclosed:
			return



		self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
				 (trade.pnl, trade.pnlcomm))




	def trade_parameters(self):
		# Function to determine real life trade parameters.
		# May need to remove the self.config for just config

		base = self.config['account_base']
		target = self.config['target_symbol']
		order = self.config['order']
		balance = self.config['account_balance']
		risk = self.config['risk_per_trade']

		if self.config['trading_mode'] == 'forex':
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

		trade_specs = forex_risk_calculator(base, target, order, price, base_price, risk, atr, balance)

		return trade_specs
		
