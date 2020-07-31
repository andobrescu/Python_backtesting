import numpy as np

# Stop loss is at 1.5 x ATR away from price
# Risk is 2% of account value per trade 
# Find pip value : Risk /1.5 x ATR

# Example : 10000£ account
# 10000 * 0.02 = 200 (Risk)
# Get an Atr for a pair = 86 * 1.5  = 129 pips example
# 1.1707 (price) - 129 pips = 1.1578
# 200 (risk money) / 129 (risk pips) = 1.550

# if JPY_pair == True: #check if a YEN cross and change the multiplier
#     multiplier = 0.01
# else:
#     multiplier = 0.0001

class forex_risk_calculator():
    def __init__(self, base, target, order, price, price_base_currency, risk, atr, balance):
        # base = account currency
        # target = target currency pair as a STR
        # price = the value of the target pair at the time of calculation 
        # price_base_currency = if the target pair does not include the account curency 
        #                       the price of the account currency vs the target currency goes here
        # risk = how much risk on the overall account ballance
        # atr = the ATR value at the time of calculation
        # balance = total account balance at the time of calculation
        self.base = base
        self.target = target
        self.price = price
        self.price_base = price_base_currency 
        self.risk = risk
        self.atr = atr
        self.order = order
        self.balance = balance
        self.multiplier = 0.0001
        self.multiplier_jpy = 0.01
    def basic_calc(self):
        pair = self.target
        counter_currency = pair[4:]
        quote_currency = pair[:3]
        balance_risk = self.balance * self.risk
        pip_risk = self.atr * 1.5
        target_pip_value = balance_risk / pip_risk
        
        if 'JPY' not in pair:
            
            if self.order == 'buy':
                sl_price = (price * (1 / self.multiplier) - pip_risk) * self.multiplier # Stop loss if buying
            elif self.order == 'sell':
                sl_price = (price * (1 / self.multiplier) + pip_risk) * self.multiplier # Stop loss if selling
            else: 
                return print('Please enter valid order')
    
            if self.base in pair:
                if self.base in counter_currency:
                    target_lot_size = target_pip_value / self.multiplier
                else:
                    target_lot_size = (target_pip_value / self.multiplier) * price
                
            else:
                target_lot_size = (target_pip_value * price_base_currency) / self.multiplier
                
        else: 
            
            if self.order == 'buy':
                sl_price = (price * (1 / self.multiplier_jpy) - pip_risk) * self.multiplier_jpy # Stop loss if buing
            elif self.order == 'sell':
                sl_price = (price * (1/self.multiplier_jpy) + pip_risk) * self.multiplier_jpy # Stop loss if selling
            else: 
                return print('Please enter valid order')
            
            if self.base in pair:
                if self.base in counter_currency:
                    target_lot_size = target_pip_value / self.multiplier_jpy
                else:
                    target_lot_size = (target_pip_value / self.multiplier_jpy) * price
                
            else:
                target_lot_size = (target_pip_value * price_base_currency) / self.multiplier_jpy
    
        
        trade_parameters = np.array([target_pip_value, pip_risk, target_lot_size, sl_price])
        print(f'Trade of {self.target} at {self.price} with risk of {balance_risk}.')
        print(f'The pip desired value is {target_pip_value}, indicated Unit size of {target_lot_size}')
        print(f'Stop loss {pip_risk} pips away at {sl_price}')
        return trade_parameters