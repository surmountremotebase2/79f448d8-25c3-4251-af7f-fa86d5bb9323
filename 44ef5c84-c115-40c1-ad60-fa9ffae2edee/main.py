from surmount.base_class import Strategy, TargetAllocation
from surmount.data import WestTexasIntermediate

class TradingStrategy(Strategy):
    def __init__(self):
        # This strategy will focus on an energy sector ETF or stock symbol as a proxy
        self.tickers = ["XLE"]  # Example: Energy Select Sector SPDR Fund, heavily influenced by oil prices
        self.data_list = [WestTexasIntermediate()]

    @property
    def interval(self):
        return "1day"  # Use daily data for analysis

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {ticker: 0 for ticker in self.tickers}  # Default allocation to 0

        # Access latest West Texas Intermediate crude oil price from data
        wti_data = data[("west_texas_intermediate",)]
        if wti_data:
            latest_price = wti_data[-1]["value"]  # Get the latest WTI price
            if latest_price > 60:  # Arbitrary decision rule, believing >$60 indicates strong demand / economy
                allocation_dict["XLE"] = 1  # Full allocation to energy sector ETF if oil price is high
            else:
                # Stay out of the market or allocate minimally; flexible for additional logic
                allocation_dict["XLE"] = 0.1  # Minimal allocation, depending on risk appetite
        else:
            # No recent WTI data could indicate an issue; strategy opts for a cautious approach
            pass  # Keeps default allocation of 0

        return TargetAllocation(allocation_dict)