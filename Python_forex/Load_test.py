import datetime
import glob
import numpy as np
import pandas as pd


class load_forex_data(object):
	def __init__(self, path):
		self.data_folder = path

	def read_files(self, file_path):
		read_file = pd.read_csv(file_path, header=None, index_col=0, parse_dates=True,  names=["Date", "Time", "Open", "High", "Low","Close","Volume"])
		return read_file

	def read_forex_files(self):

		forex_daily_path = np.array(glob.glob(self.data_folder + '*.csv'))
		
		forex_data = np.empty([len(forex_daily_path)], dtype = object)
		file_names = np.empty([len(forex_daily_path)], dtype = object)
		forex_symbols = np.empty([len(forex_daily_path)], dtype = object)
		
		for i, j in enumerate(forex_daily_path):
			file_names[i] = j[-14:]
			temp_df = self.read_files(j)
			del temp_df['Time']
			forex_data[i] = temp_df

		for i, j in enumerate(file_names):
			forex_symbols[i] = j[:3] + '_' + j[3:6]		


		return forex_symbols, forex_data



	def read_metal_files(self):

		metal_daily_path = np.array(glob.glob(self.data_folder + '*.csv'))

		metal_data = np.empty([len(metal_daily_path)], dtype = object)
		file_names = np.empty([len(metal_daily_path)], dtype = object)
		metal_symbols = np.empty([len(metal_daily_path)], dtype = object)
		
		for i, j in enumerate(metal_daily_path):
			file_names[i] = j[-14:]
			temp_df = self.read_files(j)
			del temp_df['Time']
			metal_data[i] = temp_df

		for i, j in enumerate(file_names):
			metal_symbols[i] = j[:3] + '_' + j[3:6]

		return metal_symbols, metal_data



