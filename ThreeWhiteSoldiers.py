class ThreeWhiteSoldiers(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 1, 1)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.AddForex("EURUSD", Resolution.Daily, Market.Oanda)
        
        self.back_1 = None
        self.back_2 = None
        self.current = None
        
        self.entry_price = None


    def OnData(self, data):
        self.back_2 = self.back_1
        self.back_1 = self.current
        self.current = data["EURUSD"].Close
        
        if self.back_2 == None or self.back_1 == None or self.current == None: return 
    
        # trading conditions, only when we are not invested in EURUSD 
        if self.back_1 > self.back_2 and self.current > self.back_1:
            if not self.Securities["EURUSD"].Invested: 
                self.SetHoldings("EURUSD", 0.1) # invest 10% of capital
                self.entry_price = self.current
                
                
        # exit conditions, only if we are already invested in EURUSD
        if self.Securities["EURUSD"].Invested:
            if self.current <= self.entry_price - 0.0005:
                self.Liquidate("EURUSD", "stop-loss")
            elif self.current >= self.entry_price + 0.0010:
                self.Liquidate("EURUSD", "take-profit")
                
        
        
        
        
        