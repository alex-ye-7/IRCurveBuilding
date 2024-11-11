# Alexander Ye, 2024

from date import *
from curve import *

class CurveSwap:
    def __init__(self, curve_discount: Curve, start: dt.date, length_size: int, length_unit: str, dcc: DCC):
        self.basis = dcc.get_denominator()
        self.curve_discount = curve_discount
        self.start = pydate_to_exceldate(start) 
        self.end = date_step(self.start, length_size, length_unit)
        self.accruals_fixed = generate_schedule(self.start, self.end, 1, 'Y')
        self.dcf_fixed = calculate_dcfs(self.accruals_fixed, self.basis)
 
    def calc_par_rate(self, dcurve): 
        df = dcurve.get_df(self.accruals_fixed)
        denominator = sum(self.dcf_fixed * df[1:])
        df_end = dcurve.get_df(self.end)
        return (1 - df_end) / denominator
    