from surmount.base_class import Strategy, TargetAllocation
from surmount.data import SocialSentiment, FinancialStatement, Dividend
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Identifying a set of tickers related to outdoor recreational activities,
        # which would likely include companies relevant to angling demographics.
        # This list should be refined based on actual companies of interest.
        self.tickers = ["CAB", "YETI", "JOUT"]  # Example tickers: Cabela's, YETI, Johnson Outdoors
        self.data_list = [SocialSentiment(ticker) for ticker in self.tickers]
        self.data_list += [FinancialStatement(ticker) for ticker in self.tickers]
        self.data_list += [Dividend(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        # Analyzing sentiment and financial stability to decide allocation
        for ticker in self.tickers:
            sentiment_data = data.get(("social_sentiment", ticker))
            financial_data = data.get(("financial_statement", ticker))
            dividend_data = data.get(("dividend", ticker))
            
            # Assuming positive sentiment and financial stability as indicators
            if sentiment_data and financial_data:
                recent_sentiment = sentiment_data[-1]['twitterSentiment'] + sentiment_data[-1]['stocktwitsSentiment']
                
                # Checking for healthy financial indicators such as positive net income and operating cash flow
                if financial_data[-1]['netIncome'] > 0 and financial_data[-1]['operatingCashFlow'] > 0 and recent_sentiment > 1:
                    # Prioritize dividend-paying stocks
                    if dividend_data and dividend_data[-1]['dividend'] > 0:
                        allocation_dict[ticker] = 0.4
                    else:
                        allocation_dict[ticker] = 0.3
                else:
                    allocation_dict[ticker] = 0.2
            else:
                # If insufficient data, maintain a conservative position
                allocation_dict[ticker] = 0.1
        
        # Normalize allocations to ensure sum does not exceed 1
        total_alloc = sum(allocation_dict.values())
        if total_alloc > 0:
            normalized_allocations = {k: v / total_alloc for k, v in allocation_dict.items()}
        else:
            # Uniform distribution if total_alloc is 0
            normalized_allocations = {ticker: 1.0 / len(self.tickers) for ticker in self.tickers}
        
        return TargetAllocation(normalized_allocations)