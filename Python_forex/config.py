

def parameters():
    parameters = {
        'data_path' : 'C://Users//adob1//Documents//Forex Tests//Historical_data//Daily//forex//',
        'output_path' : 'C://Users//adob1//Documents//Forex Tests//test_results//',
        'target_symbol' : 'EUR_USD', # the target symbol for backtesting the strategy
        'starting_balance' : 10000, # starting account balance in units of currency
        'account_balance' : 10000, # this will be final balance after testing
        'account_base' : 'GBP', # base account currency 
        'trading_mode' : 'forex', # type of trades be it forex or metals or stocks
        'strategy_name' : None, # name of your strategy
        'broker_commission' : 0.002, # commission per trade
        'risk_per_trade' : 0.02, # of total account balance
        'order' : None, # buy/sell leave as none
        'atr' : None, # output of the atr indicator
        'price' : None, # current price
        'base_currency_price' : None # price of the account base with the target counter
        }
    return parameters

para = parameters()
print(para.items())