from operator import concat
import random
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )



import BudgetEngine as be
import BudgetEngine.data as d
from BudgetEngine.data import nm

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__))))
        import BudgetEngine as be
    
    value = 123.4
    print('Value before: ',value)
    value = nm(value)

    print('Value after NiceMoney: ',value)
    print(type(value))
    

    today_date = d.dtfunc('today','fulldate','dt')
    print(today_date)
    today_string = d.dtfunc('today','fulldate','str')
    print(today_string)
    
    print(type(today_date))
    print(type(today_string))

    test_run_id = concat(d.dtfunc('today','fulldate','str'),str(random.randrange(111,999)))
    print(type(random.randrange(111,999)))
    print(test_run_id)
    print(type(test_run_id))
    print(test_run_id)