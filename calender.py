# Alexander Ye, 2024

from dateutil.easter import * 
from dateutil.relativedelta import relativedelta
import datetime as dt
import unittest

from date import *

def is_weekend(date: int):
    date = exceldate_to_pydate(date)
    dow = date.isoweekday()
    # 1,2,3,4,5 is Monday to Friday
    # 6,7 is Saturday, Sunday
    return dow >= 6

def find_weekday(DOW_target: int, yyyy: int, mm: int, count: int, ascending: bool = True): # ex: "Third Monday of Janurary"
    d = dt.date(yyyy, mm, 1)
    if ascending:
        dow = d.isoweekday()
        offset = (DOW_target + 7 - dow) % 7
    else: 
        d = last_day(yyyy,mm)
        dow = d.isoweekday()
        offset = (dow + 7 - DOW_target) % 7
    if count > 1:
        offset += 7*(count-1)
    if ascending:
        return d + relativedelta(days=offset)
    else: 
        return d - relativedelta(days=offset)

def is_USHoliday(t: dt.date):
    yy = t.year
    e = easter(yy)
    
    # MLK, New Year, Presidents, Juneteenth, Indepednece, Labor, Columbus, Veterans, Thanksgiving, Christmas
    if (t == find_weekday(1,yy,1,3) or t == dt.date(yy,1,1) or t == find_weekday(1,yy,2,3) 
    or t == e or t == e - relativedelta(days=2) or t == e - relativedelta(days=1) or t == dt.date(yy,6,19)
    or t == dt.date(yy,7,4) or t == find_weekday(1,yy,2,3) or t == find_weekday(1,yy,10,2)
    or t == dt.date(yy,11,11) or t == find_weekday(4,yy,11,4) or t == dt.date(yy,12,25)):
        return True
    else:
        return False
    
def date_roll(date: int, country: str): # Only US Holidays are inlcuded for now
    if country == 'US':
        while is_weekend(date): date += 1
        while is_USHoliday(exceldate_to_pydate(date)): date += 1
    return date

# Unit testing
class CalenderTests(unittest.TestCase):
    def test_is_weekend(self):
        date = pydate_to_exceldate(dt.date(2024, 3, 30))
        self.assertEqual(is_weekend(date), True)
        
    def test_find_weekday(self):
        MLK = find_weekday(1,2024,1,3)
        self.assertEqual(MLK, dt.date(2024, 1, 15))
    
    def test_isUSHoliday(self):
        self.assertEqual(is_USHoliday(dt.date(2024, 7, 4)), True)
        
    def test_date_roll(self):
        roll_this_date = pydate_to_exceldate(dt.date(2024, 1, 13)) # Should roll to 1/16 because of weekend and holiday
        self.assertEqual(date_roll(roll_this_date, 'US'), pydate_to_exceldate(dt.date(2024, 1, 16))), 
        
if __name__ == '__main__':
    unittest.main()
