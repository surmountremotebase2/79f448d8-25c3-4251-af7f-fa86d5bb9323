from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD, SMA
from surmount.data import Asset, SectorsPERatio, IndustriesPERatio
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Curated list of tickers representing companies in the smart manufacturing sector
        self.tickers = ["ROBO", "BOTZ", "XSD", "SOXX"]  # Example ETFs and stocks in robotics and semiconductors
        self.industry = "Technology"
        self.sector = "Industrials"
    
    @property
    def interval(self):
        return "1day"  # Using daily intervals for the analysis
    
    @property
    def assets(self):
        return self.tickers
    
    @property
    def data(self):
        data_list = [SectorsPERatio(self.sector), IndustriesPERatio(self.industry)]
        return data_list

    def run(self, data):
        allocation_dict = {}
        sector_pe = data.get(("sectors_pe_ratio", self.sector))
        industry_pe = data.get(("industries_pe_ratio", self.industry))
        
        if sector_pe and industry_pe:
            log(f"Latest Sector PE: {sector_pe[-1]['pe']}, Industry PE: {industry_pe[-1]['pe']}")
            # Initialize allocation equally if P/E ratios look favorable compared to historical data
            initial_allocation = 1.0 / len(self.tickers)
        else:
            log("Missing P/E data, defaulting to initial allocation")
            initial_allocation = 0.25

        for ticker in self.tickers:
            # Basic momentum strategy based on SMA and MACD
            sma_short = SMA(ticker, data, 20)  # 20-day simple moving average
            sma_long = SMA(ticker, data, 50)  # 50-day simple moving average
            macd_indicator = MACD(ticker, data, fast=12, slow=26)
            rsi = RSI(ticker, data, length=14)

            if not sma_short or not sma_long or not macd_indicator or not rsi:
                log(f"Insufficient data for ticker {ticker}, skipping...")
                allocation_dict[ticker] = 0
                continue
            
            if sma_short[-1] > sma_long[-1] and macd_indicator['MACD'][-1] > macd_indicator['signal'][-1] and rsi[-1] < 70:
                # Bullish signals: Short-term SMA above long-term SMA, MACD above signal line, and RSI below 70
                allocation_dict[ticker] = initial_allocation
            else:
                # Bearish or neutral signals: allocate a minimal portion
                allocation_dict[ticker] = 0.1 * initial_allocation
                
        return TargetAllocation(allocation_dict)