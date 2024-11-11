# Alexander Ye, 2024

from curve import *
from date import *
import matplotlib.pyplot as plt
import numpy as np

class PlotMode(enum.Enum):
    DF = 0
    ZR = 1
    FWD = 2
    
class CurvePlotter:
    def __init__(self, curve: Curve, samples: int, date_mode: str, mode = PlotMode.DF): 
        self.curve = curve
        self.mode = mode
        self.samples = samples
        self.date_mode = date_mode
        
    def plot(self):
        timesample_excel = np.linspace(self.curve.times[0], self.curve.times[-1], self.samples)
        timesample_pydate = [exceldate_to_pydate(t) for t in timesample_excel]
        
        if self.date_mode == 'excel':
            timesample = timesample_excel
        elif self.date_mode == 'pydate': 
            timesample = timesample_pydate
            
        y_new = self.curve.get_df(timesample_excel[1:])
        zero_rate = self.curve.get_zero_rate(timesample_excel[1:])
        fwd = self.curve.get_fwd_rate_aligned(timesample_excel)
        
        if self.mode == PlotMode.DF:
            plt.figure(figsize=(10,6))
            plt.plot(timesample[1:], y_new)
            plt.xlabel("Time")
            plt.ylabel("Rate")
            plt.show()
            
        elif self.mode == PlotMode.ZR:
            plt.figure(figsize=(10,6))
            plt.plot(timesample[1:], zero_rate)
            plt.xlabel("Time")
            plt.ylabel("Rate")
            plt.show()
            
        elif self.mode == PlotMode.FWD:
            plt.figure(figsize=(10,6))
            plt.plot(timesample[1:], fwd)
            plt.xlabel("Time")
            plt.ylabel("Rate")
            plt.show()
    
        else:
            raise BaseException("Unknown Plotting Mode")
    