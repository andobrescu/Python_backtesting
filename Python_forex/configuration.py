
def parameters():
    parameters = {
        'data_path' : 'C://Users//adob1//Documents//Forex Tests//Historical_data//Daily//forex//',
        'output_path' : 'C://Users//adob1//Documents//Forex Tests//test_results//',
        'output_filename' : 'results', # Str - the name of the output filename.
        'plot' : False , # bool - to plot or not to plot
        'target_symbol' : 'EUR_USD', # the target symbol for backtesting the strategy
        'base_target_symbol': None, # Leave as None
        'starting_balance' : 10000, # int - starting account balance in units of currency 
        'account_balance' : 10000, # float - this will be final balance after testing
        'account_base' : 'GBP', # str - base account currency 
        'trading_mode' : 'forex', # str - type of trades be it forex or metals or stocks
        'strategy_name' : None, # str - name of your strategy
        'broker_commission' : 0.002, # float - commission per trade float
        'risk_per_trade' : 2, # float - % of total account balance
        'order' : None, # buy/sell order leave as none
        'atr' : None, # float - output of the atr indicator Leave as None
        'price' : None, # float - current price Leave as None
        'base_currency_price' : None # price of the account base with the target counter 
                                      # IMPORTANT if the base currency if not in the target symbol
        }
    return parameters
