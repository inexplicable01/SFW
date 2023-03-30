import unittest
from FlowCalculations import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        chambers =[]
        Chamber1 = Chamber(24, 276, 'Chamber1')
        Chamber4 = Chamber(14.7, None, 'Chamber4')
        # upstream3 = Chamber(None, 276, 'Chamber7')
        Chamber2 = Chamber(None, 273, 'Chamber2')

        Chamber3 = Chamber(None, 273, 'Chamber3')
        Chamber5 = Chamber(20, 500, 'Chamber5')
        Chamber6 = Chamber(8, 273, 'Chamber6')

        restrictors=[]
        restrictors.append(Restrictor(6.0,0, 'Restrictor1', 0.9, Chamber1 , Chamber2))

        restrictors.append(Restrictor(4.5, 0, 'Restrictor2', 0.8,Chamber2 ,Chamber3))
        restrictors.append(Restrictor(8.0, 0, 'Restrictor3', 0.8, Chamber3, Chamber4))
        restrictors.append(Restrictor(4.0, 0, 'Restrictor4', 0.8, Chamber5, Chamber6))

        # res5 = Restrictor(4.0, 0, 'Restrictor5', 0.9, upstream, midstream2)
        # res6 = Restrictor(2.0, 0, 'Restrictor6', 0.8, upstream3, midstream2)
        # res7 = Restrictor(2.0, 0, 'Restrictor7', 0.8, upstream, upstream3)

        ht_exchangers=[HT_Exchanger('Restrictor2', 'Restrictor4', restrictors, 'HT_One')]

        fm = FlowModel([Chamber1,Chamber2,Chamber3,Chamber4,Chamber5,Chamber6],restrictors,ht_exchangers)
        fm.InitialGuess()
        fm.Solve()
        fm.PrintResults()
        # self.assertEqual(Chamber)  # add assertion here


# if __name__ == '__main__':
#     # unittest.main()
#     ch = Chamber(14.7,276)
