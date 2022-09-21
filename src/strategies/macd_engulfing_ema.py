import numpy as np
import talib
import datetime

from src.position import Position
from src.strategies.strategy import Strategy

timeperiod = 200
atr_multiplier = 1.5

class MacdEngulfingStrategy(Strategy):
    def __init__(self, ohlcvs, ohlcv_data, timeperiod=200, atr_multiplier=2):
        super().__init__(ohlcvs, ohlcv_data, rr=2)
        self.timeperiod = timeperiod
        self.atr_multiplier = atr_multiplier
        self.ema = talib.EMA(self.closes, timeperiod=timeperiod)
        self.atr = talib.ATR(self.highs, self.lows, self.closes)
        self.macd = talib.MACD(self.closes)

    def execute(self):
        long_position = self.long()
        short_position = self.short()

        if long_position:
            return long_position

        if short_position:
            return short_position

    def long(self):
        first_candle, second_candle, engulf_candle = self.get_last_three_candles()
        open_time = datetime.datetime.fromtimestamp(engulf_candle.timestamp/1000.0)

        print(f'[LONG, {open_time}] First Candle Check: {first_candle.close_price < first_candle.open_price}')
        print(f'[LONG, {open_time}] Second Candle Check: {second_candle.close_price < second_candle.open_price}')
        print(f'[LONG, {open_time}] Engulf Check: {engulf_candle.close_price > second_candle.open_price}')
        print(f'[LONG, {open_time}] MACD Check: {macd[-2] < 0}')
        print(f'[LONG, {open_time}] EMA Check: {ema[-2] > engulf_candle.close_price}')

        if first_candle.close_price < first_candle.open_price and \
            second_candle.close_price < second_candle.open_price and \
            engulf_candle.close_price > second_candle.open_price and \
            self.macd[-2] < 0 and \
            self.ema[-2] > engulf_candle.close_price:
            
            entry_price = engulf_candle.close_price
            whichever_is_lowest = second_candle.lowest if second_candle.highest < engulf_candle.highest else engulf_candle.lowest
            stop_loss = whichever_is_lowest
            take_profit = entry_price + (entry_price - stop_loss) * self.rr

            print(f'\n[LONG][{open_time}] Opened at: {entry_price}, Stop Loss: {stop_loss}, Take Profit: {take_profit}, EMA: {self.ema[-2]} MACD: {self.macd[-2]}')
            position = Position("buy", open_time, entry_price, stop_loss, take_profit, self.ema[-2], self.atr[-2])
            
            return position

    def short(self):
        first_candle, second_candle, engulf_candle = self.get_last_three_candles()
        open_time = datetime.datetime.fromtimestamp(engulf_candle.timestamp/1000.0)

        print(f'[SHORT, {open_time}] First Candle Check: {first_candle.close_price < first_candle.open_price}')
        print(f'[SHORT, {open_time}] Second Candle Check: {second_candle.close_price < second_candle.open_price}')
        print(f'[SHORT, {open_time}] Engulf Check: {engulf_candle.close_price > second_candle.open_price}')
        print(f'[SHORT, {open_time}] MACD Check: {macd[-2] > 0}')
        print(f'[SHORT, {open_time}] EMA Check: {ema[-2] < engulf_candle.close_price}')

        if first_candle.close_price > first_candle.open_price and \
            second_candle.close_price > second_candle.open_price and \
            engulf_candle.close_price < second_candle.open_price and \
            self.macd[-2] > 0 and \
            self.ema[-2] > engulf_candle.close_price:

            entry_price = engulf_candle.close_price
            whichever_is_highest = second_candle.highest if second_candle.highest > engulf_candle.highest else engulf_candle.highest
            stop_loss = whichever_is_highest
            take_profit = entry_price - (stop_loss - entry_price) * self.rr

            print(f'\n[SHORT][{open_time}] Opened at: {entry_price}, Stop Loss: {stop_loss}, Take Profit: {take_profit}, EMA: {self.ema[-2]} MACD: {self.macd[-2]}')

            position = Position("sell", open_time, entry_price, stop_loss, take_profit, self.ema[-2], self.atr[-2])

            return position
