class SimpleMovingAverage(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 9, 25)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.AddEquity("TSLA", Resolution.Daily)


    # def OnData(self, data):

        
    def OnEndOfAlgorithm(self):
        history_tsla = self.History(self.Symbol("TSLA"), 30, Resolution.Daily)
        tsla = history_tsla["close"]
        SMA5 = tsla[26:].mean()
        self.Debug(tsla[26:])
        self.Debug(SMA5)
        