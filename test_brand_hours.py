import unittest
import csv
from framework.helpers.brand_hours_helper import *

class BrandHoursTests(unittest.TestCase):

    def test_brands_hours_comparison(self):

      brand_hours_dict = {}

      with open('brand_hours.csv', 'wb') as output:

          ids =[35,24,25,2,3,1,523,282,8,48,38,28,97,7,10,88,72,6,314,17,79,2023,2126,141,32,15]
          for i in ids:
             writer = csv.writer(output)
             val = get_hours_for_brand(i)
             writer.writerow([i,val])
             brand_hours_dict[i] = val

      # wb = xlrd.open_workbook('expected_hours.xlsx')
      # sh = wb.sheet_by_index(0)
      # for i in range(684):
      #   cell_1 = sh.cell(i,0).value
      #   cell_2 = sh.cell(i,1).value
      #   brand_hours_final[str(cell_1)]=str(cell_2)
      #
      # # Compare the hours value for every brand from the two dictionaries
      # for key in brand_hours_dict:
      #     val = brand_hours_dict[key]
      #     key = str(key)+".0"
      #     val1 = brand_hours_final[key]
      #     val1_string = "{"+str(val1)+"}"
      #     d=json.dumps(val1_string)
      #     print d












































if __name__ == '__main__':
    unittest.main()