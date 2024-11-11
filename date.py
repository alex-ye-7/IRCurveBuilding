# Alexander Ye, 2024

import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import enum, calendar, datetime
from dataclasses import dataclass
import unittest

class Tenor: 
    def __init__(self, s):
        try:
            assert isinstance(s, str)
            self.string = s
            self.n = s[:-1]
            self.n = int(self.n) if self.n != "" else 0
            self.unit = s[-1:]
            assert self.unit in ['F', 'D', 'M', 'Q', 'Y']
        except BaseException as ex:
            raise BaseException("Unable to parse tenor %s" % s) from ex

    def __str__(self):
        return self.string
    
class DCC(enum.Enum): # Day Count Convention
    ACT365 = 0
    ACT360 = 1

    def get_denominator(self):
        if self == DCC.ACT360:
            return 360.
        elif self == DCC.ACT365:
            return 365.
        assert False
     
@dataclass
class Convention:
    payment_frequency: Tenor
    dcc: DCC
        
excelBaseDate = dt.date(1899, 12, 30)

def pydate_to_exceldate(d: dt.date) -> int:
    xldate = int((d - excelBaseDate).days)
    return xldate

def exceldate_to_pydate(d: int) -> dt.date:
    return excelBaseDate + relativedelta(days=d)

def create_excel_date(arg):
    if isinstance(arg, int):
        return arg
    elif isinstance(arg, datetime.date):
        return pydate_to_exceldate(arg)

def create_relativedelta(n: int, unit: str) -> relativedelta:
    if unit == 'M':
        return relativedelta(months=n)
    elif unit == 'D':
        return relativedelta(days=n)
    elif unit == 'Y':
        return relativedelta(years=n)
    elif unit == 'Q':
        return relativedelta(months=3 * n)
    else:
        raise BaseException("Unknown unit %s" % unit)
        
def date_step(date: int, step_size: int, step_unit: str, preserve_eom: bool = False):
    pydate = exceldate_to_pydate(date)
    pydate2 = pydate + create_relativedelta(step_size, step_unit)
    if preserve_eom:
        lastDay = calendar.monthrange(pydate.year, pydate.month)[1]
        if pydate.day == lastDay: # if the original date is the EOM
            d2 = calendar.monthrange(pydate2.year, pydate2.month)[1]
            pydate2 = datetime.date(pydate2.year, pydate2.month, d2)
    date2 = pydate_to_exceldate(pydate2)
    return date2

def generate_schedule(start: int, end: int, step: int, unit: str): 
    d = end
    out = []
    stepinv = -step
    while d > start:
        out.append(d)
        d = date_step(d, stepinv, unit)
    if out[-1] != start:
        out.append(start)
    return np.array(out[::-1])
    
def calculate_dcf(date0, date1, basis):
    numerator = date1 - date0
    return numerator / basis 

def calculate_dcfs(dates, basis):
    numerator = dates[1:] - dates[:-1]
    return numerator / basis 

# Unit testing
class DateTests(unittest.TestCase):
    def test_date_convert(self):
        date = dt.date(2024, 4, 1)
        edate = pydate_to_exceldate(date)
        self.assertEqual(edate, 45383)
        self.assertEqual(date, exceldate_to_pydate(45383))
        self.assertEqual(create_excel_date(date), 45383)
        
    def test_dcc(self):
        ACT360 = DCC.ACT360.get_denominator()
        ACT365 = DCC.ACT365.get_denominator()
        d1 = pydate_to_exceldate(dt.date(1995, 1, 1))
        d2 = pydate_to_exceldate(dt.date(1996, 1, 1))
        d3 = pydate_to_exceldate(dt.date(1997, 1, 1))
        self.assertEqual(calculate_dcf(d1, d2, ACT365), 1)
        self.assertEqual(calculate_dcf(d2, d3, ACT360), 366 / 360)
    
    def test_schedule(self):
        schedule = generate_schedule(45383, 45388, 1, 'D')
        self.assertListEqual(list(schedule), [45383, 45384, 45385, 45386, 45387, 45388])
        
if __name__ == '__main__':
    unittest.main()
    