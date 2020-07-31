import backtrader as bt
import numpy as np
from backtest_strategy import Backtrader_Strategy

class class1(Backtrader_Strategy):
	def __init__(self):
		super().__init__()
		# Write the custom strategy here:

		# Add any indicator here:

	def next(self):
		# Write what to do on next candle
		print('Done strategy')
		x = 24


