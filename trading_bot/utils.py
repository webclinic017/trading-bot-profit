import datetime
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--symbol', type=str, help='Ticker symbol', default='BTC/USDT')
    parser.add_argument('--timeframe', type=str, help='Timeframe', default='30m')
    parser.add_argument('--risk', type=int, help="Risk in dollars for 1R", default=1)

    return parser.parse_args()

def get_amount(budget, side, price, stop_loss, risk=1):
    amount = 0
    
    if side == 'buy':
        amount = risk / (price - stop_loss)
    elif side == 'sell':
        amount = risk / (stop_loss - price)
    else:
        print("Unknown side. Should be buy or sell")

    assert amount > 0.001, "Smaller than minimum amount 0.001"
    assert amount * price < budget, "Budget is not enough"

    print(amount)

    return amount

def get_x_days_ago_in_iso(x=5):
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=x)
    return (today - delta).isoformat()

if __name__ == '__main__':
    #print(get_amount(80, 'buy', 20000, 19500))
    print(get_amount(175, 'sell', 19702.4, 19742.5))
    #print(get_x_days_ago_in_iso(2))