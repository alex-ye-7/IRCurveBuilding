from date import *
from calender import *
from curve import *

class Deposit():
    def __init__(start: dt.date, tenor : Tenor, dcc: DCC):  # Money Market Convention
        self.tenor = Tenor(tenor)
        self.basis = dcc.get_denominator()
        self.start = pydate_to_exceldate(start)
        self.end = date_roll(date_step(self.start, self.tenor.n, self.tenor.unit), 'US') 
        self.accruals = np.array([self.start, self.end])
        self.dcf = calculate_dcfs(self.accruals, self.basis)[0]
        
    def get_pillar_date(self):
        return self.end
        
    def calc_par_rate(self, curve: Curve): # given df, what is par rate
        delta = (self.end - self.start)/self.basis
        df = curve.get_df(self.accruals)
        return (df[0] / df[1] - 1) / self.dcf
