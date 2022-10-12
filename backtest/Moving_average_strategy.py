import backtrader as bt
import datetime
import yfinance as yf
from backtrader import plot 
from main import BtMain

class MaStrategy(bt.Strategy):
    
	def __init__(self):
		self.ma = bt.indicators.SimpleMovingAverage(self.data.close, period=100)
		self.order = None
 
	def next(self):
		if self.order:
			return
		if not self.position: # to check if we already have a position in the market
      
			if (self.data.close[0] > self.ma[0]) & (self.data.close[-1] < self.ma[-1]):
				self.log('Buy Create, %.2f' % self.data.close[0])
				self.order = self.buy(size=10) # buy when closing price today crosses above MA.
    
			if (self.data.close[0] < self.ma[0]) & (self.data.close[-1] > self.ma[-1]):
				self.log('Sell Create, %.2f' % self.data.close[0])
				self.order = self.sell(size=10)  # sell when closing price today below MA
		else:
		# This means we are in a position, and hence you need to define exit strategy here.
			if len(self) >= (self.bar_executed + 4):
				self.log('Position Closed, %.2f' % self.data.close[0])
				self.order = self.close()

	def log(self, txt):
		dt=self.datas[0].datetime.date(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def notify_order(self, order):
		if order.status == order.Completed:
			if order.isbuy():
				self.log(
				"Executed BUY (Price: %.2f, Value: %.2f, Commission %.2f)" %
				(order.executed.price, order.executed.value, order.executed.comm))
			else:
				self.log(
				"Executed SELL (Price: %.2f, Value: %.2f, Commission %.2f)" %
				(order.executed.price, order.executed.value, order.executed.comm))
			self.bar_executed = len(self)
		elif order.status in [order.Canceled, order.Margin, order.Rejected]:
			self.log("Order was canceled/margin/rejected")
		self.order = None
  
  
if __name__ == '__main__':
        # Create a cerebro instance, add our strategy, some starting cash at broker and a 0.1% broker commission
        cerebro = bt.Cerebro()
        cerebro.addstrategy(MaStrategy)
        cerebro.broker.setcash(10000)
        cerebro.broker.setcommission(commission=0.001)
        FEED = BtMain()
        data = bt.feeds.PandasData(dataname=FEED.get_feeds('SOL-USD','2021-1-1','2022-1-1'))
        cerebro.adddata(data)
    
        print('<START> Brokerage account: $%.2f' % cerebro.broker.getvalue())
        cerebro.run()
        print('<FINISH> Brokerage account: $%.2f' % cerebro.broker.getvalue())
        # Plot the strategy
        cerebro.plot(style='candlestick',loc='grey', grid=False) #You can leave inside the paranthesis empty
            