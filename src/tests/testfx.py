"""
Functions for unit testing
"""
from termcolor import cprint

def test(name: str, test: int, outcome: False):
    """
    Output test outcome to console
        [name]      (str): name of test
        [test]      (int): outcome type
            [1: Should Pass]
            [2: Should Fail]
        [outcome]   (bool): True/False = Pass/Fail
    """
    if outcome==True:
        outcome="[*Test Passed*]"
        color='on_green'
        if test==1:
            test=("%s successful" % name)
        if test==2:
            test=("%s failed" % name)
    if outcome==False:
        outcome="[#Test Failed#]"
        color='on_red'
        if test==1:
            test=("%s failed" % name)
        if test==2:
            test=("%s successful" % name)
    cprint("%s %s" % (outcome, test),'white',color)