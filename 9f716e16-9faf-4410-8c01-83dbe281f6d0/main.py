from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import FinancialStatement, Ratios, Dividend

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers of interest that are potentially beneficial from an aging population
        # These are examples and should be replaced with actual research findings
        self.tickers = ["JNJ", "PFE", "PG", "MDT"]
        # Collect financial statements, ratios, and dividend data for each ticker
        self.data_list = [FinancialStatement(i) for i in self.tickers] + \
                         [Ratios(i) for i in self.tickers] + \
                         [Dividend(i) for i in self.tickers]

    @property
    def interval(self):
        # Daily data would be sufficient for this long-term strategy
        return "1day"
    
    @property 
    def assets(self):
        # Define the assets that the strategy will trade
        return self.tickers

    @property
    def data(self):
        # Return the data required by the strategy
        return self.data_list
    
    def run(self, data):
        allocation_dict = dict()
        
        # Iterate over each ticker to make decisions
        for ticker in self.tickers:
            # Example decision-making process based on simplified indicators
            # Investors might look for solid dividend-yielding stocks as part of an aging demographics play
            # Check if a dividend is present and the payout ratio is reasonable
            ratios = data.get(("ratios", ticker))
            dividend = data.get(("dividend", ticker))
            
            # Check if the necessary data is available
            if dividend and ratios:
                # Example criteria: positive recent dividend, payout ratio below 60%
                recent_dividend = dividend[-1]["dividend"] > 0
                payout_ratio = next((item for item in ratios if item.get("payoutRatio")), {}).get("payoutRatio", 100)
                
                # Assuming a payout ratio of less than 60% is considered sustainable
                if recent_dividend and payout_ratio < 0.6:
                    # Allocate funds to this stock, equally divided among chosen assets for simplicity
                    allocation_dict[ticker] = 1 / len(self.tickers)
                else:
                    # Do not allocate to this stock due to failing the criteria
                    allocation_dict[ticker] = 0
            else:
                # In case of missing data, skip allocation
                allocation_dict[ticker] = 0
        
        return TargetAllocation(allocation_dict)