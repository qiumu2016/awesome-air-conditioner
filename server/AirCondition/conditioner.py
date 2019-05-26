class conditioner:
    def __init__(self,Mode,Temp_highLimit,Temp_lowLimit,default_TargetTemp,FeeRate_H,FeeRate_M,FeeRate_L):
        self.Mode = Mode
        self.Temp_highLimit = 30
        self.Temp_lowLimit = 10
        self.default_TargetTemp = default_TargetTemp
        self.FeeRate_H = 0.75
        self.FeeRate_M = 0.5
        self.FeeRate_L = 0.25
