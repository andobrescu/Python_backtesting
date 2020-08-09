import backtrader as bt
import numpy as np
from configuration import parameters
from backtest_strategy import Backtrader_Strategy

class custom_strategy_example(Backtrader_Strategy):
	# Custom strategy class :
	def __init__(self):
		super().__init__()
		
		self.counter = 0
		# Add any indicator here:
		self.indicator_params = (('maperiod', 15),)
		self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=15)
		
		self.atr = bt.indicators.ATR(self.datas[0], period=14 ,plot=True)

	def next(self):

		# Log the closing price of the series from the reference
		self.log('Close, %.4f' % self.dataclose[0])

		# Write what to do on next candle
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


