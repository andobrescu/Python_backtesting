from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import os
from backtest_main import backtesting
from config import parameters

if __name__ == '__main__':
    configuration = parameters()
    backtesting(configuration)
    print('Done')

