#  ==================================================================================
#  
#  Copyright (c) 2018, Evangelos G. Karakasis 
#  
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#  
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#  
#  ==================================================================================

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#                   Unit testing
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

import sys
sys.path.append('../')
sys.path.append('../../')

from InputCheck.InputCheckDecorators import acceptedTypes, acceptedValues
from InputCheck import np
import unittest

# NOTE : the tests are not exhaustive, more test should be designed to check every known possible situation, 
#        nevertheless, are enough to ensure the correctness of the code ( at least I hope so :) )

class Tests_acceptedTypes(unittest.TestCase):

    def test_acceptedTypes_01_number(self):
        @acceptedTypes([int, float], [int, float], typesCheckEnabled = True, ObjectConsistencyCheck = False)
        def func(input1, input2):
            pass

        @acceptedTypes([int, float], [int, float], typesCheckEnabled = False, ObjectConsistencyCheck = False)
        def func2(input1, input2):
            pass

        @acceptedTypes(int, float, float, typesCheckEnabled = True, ObjectConsistencyCheck = False)
        def func3(input1, input2=2.0, input3=3.0):
            pass

        @acceptedTypes(float, float, float, typesCheckEnabled = True, ObjectConsistencyCheck = False)
        def func4(input1, input2=int(2), input3=3.0):
            pass

        func(1, 1.0)
        with self.assertRaises(TypeError):
            func('some text', 1)
        with self.assertRaises(TypeError):
            func(2.0, [])
        with self.assertRaises(TypeError):
            func(2, ())
        with self.assertRaises(TypeError):
            func(2, True)        
        # it is not expected to raise any exception since the type checks have been disabled
        func2('some text', ())

        func3(1)
        func3(1, input2=5.0)
        func3(1, input2=5.0, input3=10.0)
        func3(1, input3=10.0)
        func3(input3=2.0, input1=1) 

        with self.assertRaises(ValueError):
            func3()
        with self.assertRaises(TypeError):
            func3(input1=1.0, input3=2)
        with self.assertRaises(TypeError):
            func4(input1=1.0)


    def test_acceptedTypes_02_string(self):
        @acceptedTypes(str, typesCheckEnabled = True, ObjectConsistencyCheck = False)
        def func(input1):
            pass

        @acceptedTypes(str, typesCheckEnabled = False, ObjectConsistencyCheck = False)
        def func2(input1):
            pass

        func('some text')
        with self.assertRaises(TypeError):
            func(1)
        with self.assertRaises(TypeError):
            func([])
        with self.assertRaises(TypeError):
            func(())
        with self.assertRaises(TypeError):
            func(True)
        # it is not expected to raise any exception since the type checks have been disabled
        func2(())


    def test_acceptedTypes_03_object(self):
        @acceptedTypes([list, tuple, dict], typesCheckEnabled = True, ObjectConsistencyCheck = False)
        def func(input1):
            pass

        @acceptedTypes([list, tuple, dict], typesCheckEnabled = False, ObjectConsistencyCheck = False)
        def func2(input1):
            pass

        typeCheck = {
            'type': [list, tuple],  
            'command': {
                'checkConsistency': True
            }
        }
        @acceptedTypes(typeCheck)
        def func3(intput1):
            pass

        typeCheck2 = {
            'type': [list, tuple],  
            'command': {
                'checkConsistency': True,        # <-- here we declare than we want all the elements of the list/tuple to have the same type
                'consistencyType' : [int, float] # <-- and here we declare that we want this type to be either an int or float
            }
        }
        @acceptedTypes(typeCheck2)
        def func4(intput1):
            pass

        func([])
        func(())
        func({})
        with self.assertRaises(TypeError):
            func(1)
        with self.assertRaises(TypeError):
            func(2.0)
        with self.assertRaises(TypeError):
            func('some text')
        with self.assertRaises(TypeError):
            func(True)
        # it is not expected to raise any exception since the type checks have been disabled
        func2('some text')

        func3([1,2,3,4,5])
        with self.assertRaises(TypeError):
            func3(100)
        with self.assertRaises(TypeError):
            func3(100)
        with self.assertRaises(TypeError):
            func3((1,2,3,4,'some text'))

        with self.assertRaises(TypeError):
            func4(['a', 'b', 'c'])


    def test_acceptedTypes_04_array(self):
        @acceptedTypes(np.ndarray, typesCheckEnabled = True, ObjectConsistencyCheck = False)
        def func(input1):
            pass

        @acceptedTypes(np.ndarray, typesCheckEnabled = False, ObjectConsistencyCheck = False)
        def func2(input1):
            pass

        func(np.array([]))
        func(np.array(()))
        with self.assertRaises(TypeError):
            func(1)
        with self.assertRaises(TypeError):
            func(2.0)
        with self.assertRaises(TypeError):
            func('some text')
        with self.assertRaises(TypeError):
            func(True)
        # it is not expected to raise any exception since the type checks have been disabled
        func2('some text')


class Tests_acceptedValues(unittest.TestCase):

    def test_acceptedValues_01_number(self):
        # @acceptedTypes([int, float], [int, float], typesCheckEnabled = True, ObjectConsistencyCheck = False)
        @acceptedValues({'range': [1,10], 'command': 'allowNone'}, {'minValue': 5}, {'maxValue': 100, 'command': 'noCheck'}, valueCheckEnabled = True)
        def func(input1, input2, input3):
            pass

        # @acceptedTypes([int, float], [int, float], typesCheckEnabled = False, ObjectConsistencyCheck = False)
        @acceptedValues({'range': [1,10]}, {'minValue': 5}, valueCheckEnabled = False)
        def func2(input1, input2):
            pass

        @acceptedValues({'range': [1,10]}, {'minValue': 5}, {'maxValue': 100}, valueCheckEnabled = True)
        def func3(input1, input2=7.0, input3=3.0):
            pass

        @acceptedValues({'range': [1,10]}, {'minValue': 5}, {'maxValue': 100}, valueCheckEnabled = True)
        def func4(input1, input2=1.0, input3=3.0):
            pass

        func(5, 10, 2000)
        func(None, 10, 2000)
        with self.assertRaises(ValueError):
            func(5, None, 10)
        with self.assertRaises(ValueError):
            func(0, 10, 10)
        with self.assertRaises(ValueError):
            func(15, 10, 10)
        with self.assertRaises(ValueError):
            func(5, 1, 10)        
        # it is not expected to raise any exception since the type checks have been disabled
        func2('some text', ())

        func3(2.0)
        func3(2.0, input2=6.0)
        func3(2.0, input2=6.0, input3=10.0)
        func3(2.0, input3=10.0)
        func3(input3=2.0, input1=1)
        with self.assertRaises(ValueError):
            func3()
        with self.assertRaises(ValueError):
            func3(input1=1.0, input3=101)
        with self.assertRaises(ValueError):
            func4(input1=1.0)


    def test_acceptedValues_02_string(self):
        @acceptedValues({'rangeLength': [1,10]}, valueCheckEnabled = True)
        def func1(input1):
            pass

        @acceptedValues({'minLength': 5}, valueCheckEnabled = True)
        def func2(input1):
            pass

        @acceptedValues({'maxLength': 10}, valueCheckEnabled = True)
        def func3(input1):
            pass

        @acceptedValues({'set': ['a', 'b', 'c']}, valueCheckEnabled = True)
        def func4(input1):
            pass

        @acceptedValues({'set': ['a', 'b', 'c']}, valueCheckEnabled = False)
        def func5(input1):
            pass

        func1('asd')
        func2('asddsaasd')
        func3('asddsa')
        func4('b')
        with self.assertRaises(ValueError):
            func1('asdasddsaasddsa')
        with self.assertRaises(ValueError):
            func1('')
        with self.assertRaises(ValueError):
            func2('asd')
        with self.assertRaises(ValueError):
            func3('asdasddsaasd')
        with self.assertRaises(ValueError):
            func4('g')    
        # it is not expected to raise any exception since the type checks have been disabled
        func5(123)


    def test_acceptedValues_03_object(self):
        @acceptedValues({'rangeLength': [1,10]}, valueCheckEnabled = True)
        def func1(input1):
            pass

        @acceptedValues({'minLength': 5}, valueCheckEnabled = True)
        def func2(input1):
            pass

        @acceptedValues({'maxLength': 10}, valueCheckEnabled = True)
        def func3(input1):
            pass

        @acceptedValues({'maxLength': 10}, valueCheckEnabled = False)
        def func4(input1):
            pass

        func1([1,2,3])
        func1({'f1':1, 'f2':2, 'f3':3})
        func2([1,2,3,4,5,6,7,8])
        func3([1,2,3,4,5,6,7,8])
        with self.assertRaises(ValueError):
            func1((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
        with self.assertRaises(ValueError):
            func1([])
        with self.assertRaises(ValueError):
            func2((1,2,3))
        with self.assertRaises(ValueError):
            func2({'f1':1, 'f2':2, 'f3':3})
        with self.assertRaises(ValueError):
            func3((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
        # it is not expected to raise any exception since the type checks have been disabled
        func4(123)


    def test_acceptedValues_04_array(self):
        @acceptedValues({'rangeLength': [1,10]}, valueCheckEnabled = True)
        def func1(input1):
            pass

        @acceptedValues({'minLength': 5}, valueCheckEnabled = True)
        def func2(input1):
            pass

        @acceptedValues({'maxLength': 10}, valueCheckEnabled = True)
        def func3(input1):
            pass

        @acceptedValues({'maxLength': 10}, valueCheckEnabled = False)
        def func4(input1):
            pass

        @acceptedValues({'rowsMax': 10}, valueCheckEnabled = True)
        def func5(input1):
            pass

        @acceptedValues({'colsMin': 3}, valueCheckEnabled = True)
        def func6(input1):
            pass

        @acceptedValues({'colsRange': [2, 5]}, valueCheckEnabled = True)
        def func7(input1):
            pass

        @acceptedValues({'rowsRange': [2, 5], 'colsRange': [2, 5], 'command': 'allowNone'}, valueCheckEnabled = True)
        def func8(input1):
            pass

        func1(np.array([1,2,3]))
        func2(np.array([1,2,3,4,5,6,7,8]))
        func3(np.array([1,2,3,4,5,6,7,8]))
        with self.assertRaises(ValueError):
            func1(np.ones((2, 3, 5)))       
        with self.assertRaises(ValueError):
            func1(np.ones((1, 25)))
        with self.assertRaises(ValueError):
            func1(np.array([]))
        with self.assertRaises(ValueError):
            func2(np.array([1,2,3]))
        with self.assertRaises(ValueError):
            func3(np.ones((1, 25)))
        # it is not expected to raise any exception since the type checks have been disabled
        func4(123)
        with self.assertRaises(ValueError):
            func5(np.ones((20, 5)))
        with self.assertRaises(ValueError):
            func6(np.ones((2, 2)))
        with self.assertRaises(ValueError):
            func7(np.ones((3, 6)))
        with self.assertRaises(ValueError):
            func8(np.ones((3, 6)))
        with self.assertRaises(ValueError):
            func8(np.ones((6, 3)))
        func8(None)


if __name__ == '__main__':
    unittest.main()