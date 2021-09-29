class MACrossover(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 1)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        # self.AddEquity("SPY", Resolution.Minute)
        self.long_list = []
        self.short_list = []
        
        self.stop = False
        
        self.currencies = ["EURUSD", "GBPJPY"]
        self.AddForex("EURUSD", Resolution.Daily)
        self.AddForex("GBPJPY", Resolution.Daily)


    def OnData(self, data):
        
        if self.stop:
            return
        
        currencies = self.currencies
        
        for currency in currencies:
            self.Debug(currency)
            currency_data = self.History([currency], 30, Resolution.Daily)
            
            MA21_Pre = currency_data.close[8:29].mean()
            MA5_Pre = currency_data.close[24:29].mean()
            MA21_Current = currency_data.close[9:30].mean()
            MA5_Current = currency_data.close[25:30].mean()
            
            
            # First Trade entry
            if currency not in self.long_list and currency not in self.short_list:
                self.Debug("First trade: " + str(currency))
                
                # Check for Bullish Crossover for Entry
                if MA5_Pre < MA21_Pre and MA5_Current > MA21_Current:
                    self.SetHoldings(currency, 0.5)
                    self.long_list.append(currency)
                    
                # Check for Bearish Crossover for Entry
                if MA5_Pre > MA21_Pre and MA5_Current < MA21_Current:
                    self.SetHoldings(currency, -0.5)
                    self.short_list.append(currency)


            # Long List Checking
            if currency in self.long_list:
                # Check for Bearish Crossover
                if MA5_Pre > MA21_Pre and MA5_Current < MA21_Current:
                    self.SetHoldings(currency, -0.5)
                    self.long_list.remove(currency)
                    self.short_list.append(currency)


            # Short List Checking
            if currency in self.short_list:
                # Check for Bullish Crossover for Entry
                if MA5_Pre < MA21_Pre and MA5_Current > MA21_Current:
                    self.SetHoldings(currency, 0.5)
                    self.short_list.remove(currency)
                    self.long_list.append(currency)
                    

        if self.Portfolio.Cash < 85000:
            self.stop = True
            self.Liquidate()


