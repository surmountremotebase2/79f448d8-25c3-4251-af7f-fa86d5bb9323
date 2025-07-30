from surmount.base_class import Strategy, TargetAllocation
from surmount.data import WestTexasIntermediate, SectorsPERatio
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Focusing on energy ETFs and tech stocks as proxies
        self.tickers = ["XLE", "AAPL"]  # XLE - Energy Sector ETF, AAPL - Represents tech growth
        self.data_list = [WestTexasIntermediate(), SectorsPERatio("NYSE")]

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
        allocation_dict = {"XLE": 0, "AAPL": 0}
        
        # Check recent WTI oil prices as an indicator for energy sector performance
        oil_prices = data[("west_texas_intermediate",)]
        if oil_prices and len(oil_prices) > 0 and oil_prices[-1]['value'] > 60:
            # Favoring energy sector investment if oil prices are high, indicating potential growth
            allocation_dict["XLE"] = 0.6
        
        # Review PE ratios for the tech sector to decide on AAPL allocation
        pe_ratios_for_tech = [item for item in data[("sectors_pe_ratio", "NYSE")] if item['sector'] == "Technology"]
        
        if pe_ratios_for_tech and len(pe_ratios_for_tech) > 0:
            last_pe_ratio = float(pe_ratios_for_tech[-1]['pe'])
            if last_pe_ratio < 25:
                # If the PE ratio is low, it may indicate that tech stocks are undervalued
                allocation_dict["AAPL"] = 0.4
        
        # Log the strategy decision
        log("Allocations: " + str(allocation_dict))
        
        return TargetAllocation(allocation_dict)