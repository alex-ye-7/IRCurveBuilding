# Alexander Ye, 2024

from date import *
from curveplotter import *
import scipy.interpolate
import numpy as np
import random

class ExponentialInterpolator:
    def __init__(self, interp):
        self.interp = interp

    def value(self, t):
        return np.exp(self.interp(t))
    
class Curve:
    def __init__(self, eval_date, dates, dfs, interpolation_mode): 
        try:
            spot = pydate_to_exceldate(eval_date)
            times = [pydate_to_exceldate(date) for date in dates]
            self.times = np.append(spot, times)
            self.dfs = np.append(1.0, dfs)
            self.interpolation_mode = 'linear'
            
        except BaseException as ex:
            raise BaseException("Unable to create curve")        
        
    def set_interpolator(self):
        logdf = np.log(self.dfs)
        interp = scipy.interpolate.interp1d(self.times, logdf, self.interpolation_mode, fill_value='extrapolate') 
        self.interpolator = ExponentialInterpolator(interp)

    def get_df(self, t):
        return self.interpolator.value(t)
    
    def set_df(self, d, df):
        xd = pydate_to_exceldate(d)
        if np.in1d(xd,self.times):
            idx = np.searchsorted(self.times, xd)
            self.dfs[idx] = df
        else:
            self.times = np.append(self.times, xd)
            self.dfs = np.append(self.dfs, df)
        self.set_interpolator()
        
    def get_fwd_rate(self, t_start, t_end):
        dfs_start = self.get_df(t_start)
        dfs_end = self.get_df(t_end)
        dcf = calculate_dcf(t_start, t_end)
        return (dfs_start / dfs_end - 1) / dcf
    
    def get_fwd_rate_aligned(self, t):
        dfs = self.get_df(t)
        df1 = dfs[:-1]
        df2 = dfs[1:]
        dcf = calculate_dcfs(t, 360)
        return (df1 / df2 - 1) / dcf
        
    def get_zero_rate(self, t):
        dfs = self.get_df(t)
        dcf = calculate_dcf(self.times[0], t, 360)
        return (1 / dfs - 1) / dcf

class CurveMaker:
    @staticmethod # No constructor needed
    def makeCurveFromShortRateModel(times, r0: float, speed: float, r_mean: float, sigma: float, 
                                    interpolation_mode):
        r = r0
        timesxl = np.array([pydate_to_exceldate(t) for t in times])
        rates = []
        dts = timesxl[1:] - timesxl[:-1]
        dts = dts / 365.
        for dt_ in dts: 
            rates.append(r)
            dr = speed * (r_mean - r) * dt_ + sigma * random.gauss(0.0, 1.0) * dt_**.5
            r += dr
    
        rates = np.array(rates)
        dfs_fwd = np.exp(-rates * dts)
        dfs = np.cumprod(dfs_fwd)
        return Curve(eval_date=times[0], dates = times[1:], dfs=dfs, interpolation_mode=interpolation_mode)

    
if __name__ == '__main__': # Testing short rate model
    times = [exceldate_to_pydate(i) for i in range(2, 2 + 80 * 365 + 1, 180)]
    curve = CurveMaker.makeCurveFromShortRateModel(times, r0=0.022, speed=0.0001,
                                                r_mean=0.05, sigma=0.0005,
                                                interpolation_mode='linear')
    curve.set_interpolator()
 
    dcurve = CurvePlotter(curve, 1000, 'pydate', PlotMode.DF)
    dcurve.plot()
 