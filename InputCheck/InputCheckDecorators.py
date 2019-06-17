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

# ----------
# The current implementation of decorator-based check of functions inputs types and values has been inspired from 
# Jackson Cooper's online article entitled "Validate Python Function Parameter & Return Types with Decorators" 
# (https://www.pythoncentral.io/validate-python-function-parameters-and-return-types-with-decorators/)
# ----------

# ----------
# This code is written with the intention to offer an automated and easy way 
# of checking the validity of a function's inputs. The main purpose is to 
# eliminate additional code, which is frequently used to check the inputs validity 
# and to enhance code safety. However, it adds some time overhead in the overall run 
# time. Thus, it is suggested to be used in Non Time Critical algorithms or you 
# can always use a control flag in order to deactivate the checks when speed matters. 
# ----------

# NOTE : a tree describing the data structure scheme and the kind of functionality that will be provided through this library
#  - I am not sure if it has some meaning for anyone else though :) -
# ============================
# python data structure scheme
# ----------------------------
# - DataStructure
#   - name
#   - type
#       - number 
#           - int
#           - float       
#       - string
#       - object
#           - list
#           - tuple
#           - dictionary
#           - other (e.g. np.ndarray)
#   - value
# ============================
# functionality per category
# ----------------------------
# - number value (a number can have continuous ((-Inf, Inf)) or discrete (set) domain)
#   - minValue (e.g. x belongs in [minValue, Inf) -- continuous)
#   - maxValue (e.g. x belongs in (-Inf, maxValue] -- continuous)
#   - range    (e.g. x belongs in [minValue, maxValue] -- continuous)
#   - set      (e.g. x belongs in [1,2,3,4,5] -- discrete)
#
# - string value
#   - length
#       - minLength
#       - maxLength
#       - rangeLength
#   - set
#
# - list or tuple or dictionary value
#   - length
#       - minLength
#       - maxLength
#       - rangeLength
#
# - numpy.ndarray
#   - numOfDimensions (currently only 1D array will be supported, since, this library is meant to serve mainly 1D signal processing)
#   - length
#       - minLength
#       - maxLength
#       - rangeLength
# ============================

import sys
sys.path.append('../')
sys.path.append('../../')

from InputCheck import functools, np
import inspect

def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }

numberTypes = [int, float]
stringTypes = [str]
boolTypes   = [bool]
objectTypes = [list, tuple, dict]
noneTypes   = [type(None)]
arrayType   = [np.ndarray]


def ordinal(num):
    """
    Returns the ordinal number of a given integer, as a string.
    eg. 1 -> 1st, 2 -> 2nd, 3 -> 3rd, etc.
    """
    if 10 <= num % 100 < 20:
        return '{0}th'.format(num)
    else:
        ord = {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(num % 10, 'th')
        return '{0}{1}'.format(num, ord)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# TYPE CHECKS
# ------------

# TODO : change the usage of ObjectConsistencyCheck so as to be passed to each separate input (if needed) 
#        as a command. Stop using it as a generic flag to start/stop consistency checks globaly.
def CheckTypes(arg_num, actual_arg, accepted_arg_type, validate_function):
    """
    This is the main way for checking the validity of the inputs TYPES of a function.
    It can handle types like: int, float, str, bool, list, tuple, dict and others
    """
    ObjectConsistencyCheck = False
    DisiredConsistencyTypes = None
    ArgType = type(actual_arg)
    ord_num = ordinal(arg_num + 1)
    
    if type(accepted_arg_type) is list:
        # here we check for multiple allowed input types (e.g. a number could be integer of real)
        if ArgType not in accepted_arg_type:            
            raise TypeError('The type of the {0} argument of function {1}() does not belong in {2}'.format(ord_num, validate_function.__name__, accepted_arg_type))
    elif type(accepted_arg_type) is dict:
        Keys = accepted_arg_type.keys()        

        # check for commands first
        if 'command' in Keys:
            cmd = accepted_arg_type['command']
            
            if type(cmd) is dict:
                for key in cmd:
                    if key == 'checkConsistency':
                        if cmd[key] in [True, False]:
                            ObjectConsistencyCheck = cmd[key]
                    elif key == 'consistencyType' and 'checkConsistency' in cmd:
                        if type(cmd[key]) is not list:
                            cmd[key] = [cmd[key]]
                        DisiredConsistencyTypes = cmd[key]

        if 'type' in Keys:
            accepted_Type = accepted_arg_type['type']
            if type(accepted_Type) is list:
                if ArgType not in accepted_Type:            
                    raise TypeError('The type of the {0} argument of function {1}() does not belong in {2}'.format(ord_num, validate_function.__name__, accepted_Type))
            else: 
                if ArgType != accepted_Type:            
                    raise TypeError('The {0} argument of the function {1}() is not a {2}'.format(ord_num, validate_function.__name__, accepted_Type))

    else: 
        # here we check if an input belongs to a specific allowed type (e.g. we want the input1 to be an integer value)
        if ArgType != accepted_arg_type:            
            raise TypeError('The {0} argument of the function {1}() is not a {2}'.format(ord_num, validate_function.__name__, accepted_arg_type))

    # here, and only for list and tuple variables, we can check for an element-wise type consistency
    # e.g. we want to be sure that a list contains only float numbers
    # NOTE: 
    #  - that the <ObjectConsistencyCheck> flag can disable this check (to disable this feature set ObjectConsistencyCheck = False)
    #  - currently this check can ensure the consistency of lists or tuples with elements that have int or float types
    #    NOTE : this check needs to be extended to handle more types
    if ObjectConsistencyCheck and ArgType in [list, tuple]:  
        tp = []
        tpa = tp.append                  
        [tpa(type(item)) for item in actual_arg if type(item) not in tp]

        if len(tp) > 1:
            raise TypeError('Each element of the {0} variable must have the same type.'.format(ord_num))
        elif len(tp) == 1:
            if DisiredConsistencyTypes is not None:
                if tp[0] not in DisiredConsistencyTypes:
                    raise TypeError('Each element of the {0} variable must have the same type. Allowed types: {1}.'.format(ord_num, DisiredConsistencyTypes))            

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# VALUE CHECKS
# ------------

def CheckRange(ord_num, value, rng, validate_function, textTemplate):
    if value < rng[0] or value > rng[1]:            
        raise ValueError('The {0} argument of the function {1}() has {2} out of the accepted range: {3}.'.format(ord_num, validate_function.__name__, textTemplate, rng))


def CheckMin(ord_num, value, minval, validate_function, textTemplate):
    if value < minval:            
        raise ValueError('The {0} argument of the function {1}() has lower {2} than the accepted: {3}.'.format(ord_num, validate_function.__name__, textTemplate, minval))


def CheckMax(ord_num, value, maxval, validate_function, textTemplate):
    if value > maxval:            
        raise ValueError('The {0} argument of the function {1}() has higher {2} than the accepted: {3}.'.format(ord_num, validate_function.__name__, textTemplate, maxval))


def CheckValueInSet(ord_num, value, vset, validate_function):
    if value not in vset:            
        raise ValueError('The {0} argument of the function {1}() does not belong to the set {2}.'.format(ord_num, validate_function.__name__, vset))


def CheckValueNone(ord_num, value, validate_function):
    if value is None:            
        raise ValueError('The {0} argument of the function {1}() must not be <None>.'.format(ord_num, validate_function.__name__))


def CheckNumber(arg_num, actual_arg, accepted_arg_types, validate_function):
    accepted_arg_type = accepted_arg_types[arg_num]
    Keys = accepted_arg_type.keys()
    ord_num = ordinal(arg_num + 1)

    # check for commands first
    if 'command' in Keys:
        cmd = accepted_arg_type['command']
        if cmd == 'noCheck':
            return
        elif cmd == 'allowNone':
            if actual_arg is None:
                return

    CheckValueNone(ord_num, actual_arg, validate_function)
    
    for Key in Keys:
        checkVal = accepted_arg_type[Key]

        if Key == 'range':
            CheckRange(ord_num, actual_arg, checkVal, validate_function, 'value')

        elif Key == 'minValue':
            CheckMin(ord_num, actual_arg, checkVal, validate_function, 'value')

        elif Key == 'maxValue':
            CheckMax(ord_num, actual_arg, checkVal, validate_function, 'value')

        elif Key == 'set':
            CheckValueInSet(ord_num, actual_arg, checkVal, validate_function)


def CheckString(arg_num, actual_arg, accepted_arg_types, validate_function):
    accepted_arg_type = accepted_arg_types[arg_num]
    Keys = accepted_arg_type.keys()
    ord_num = ordinal(arg_num + 1)

    # check for commands first
    if 'command' in Keys:
        cmd = accepted_arg_type['command']
        if cmd == 'noCheck':
            return
        elif cmd == 'allowNone':
            if actual_arg is None:
                return

    CheckValueNone(ord_num, actual_arg, validate_function)

    for Key in Keys:
        checkVal = accepted_arg_type[Key]

        if Key == 'minLength':
            CheckMin(ord_num, len(actual_arg), checkVal, validate_function, 'length')

        elif Key == 'maxLength':
            CheckMax(ord_num, len(actual_arg), checkVal, validate_function, 'length')

        elif Key == 'rangeLength':
            CheckRange(ord_num, len(actual_arg), checkVal, validate_function, 'length')
        
        elif Key == 'set':
            CheckValueInSet(ord_num, actual_arg, checkVal, validate_function)


def CheckObject(arg_num, actual_arg, accepted_arg_types, validate_function):
    accepted_arg_type = accepted_arg_types[arg_num]
    Keys = accepted_arg_type.keys()
    ord_num = ordinal(arg_num + 1)

    # check for commands first
    if 'command' in Keys:
        cmd = accepted_arg_type['command']
        if cmd == 'noCheck':
            return
        elif cmd == 'allowNone':
            if actual_arg is None:
                return

    CheckValueNone(ord_num, actual_arg, validate_function)
    
    for Key in Keys:
        checkVal = accepted_arg_type[Key]

        if Key == 'minLength':
            CheckMin(ord_num, len(actual_arg), checkVal, validate_function, 'length')

        elif Key == 'maxLength':
            CheckMax(ord_num, len(actual_arg), checkVal, validate_function, 'length')

        elif Key == 'rangeLength':
            CheckRange(ord_num, len(actual_arg), checkVal, validate_function, 'length')


def CheckArray(arg_num, actual_arg, accepted_arg_types, validate_function):
    accepted_arg_type = accepted_arg_types[arg_num]
    Keys = accepted_arg_type.keys()
    ord_num = ordinal(arg_num + 1)

    # check for commands first
    if 'command' in Keys:
        cmd = accepted_arg_type['command']
        if cmd == 'noCheck':
            return
        elif cmd == 'allowNone':
            if actual_arg is None: # the None values are allowed here: if None then do no checks
                return

    # if the value is None then raise an ValueError exception
    CheckValueNone(ord_num, actual_arg, validate_function)

    arg_shape = actual_arg.shape
    ndims = len(arg_shape)
    if ndims > 2: # currently only arrays up to 2 dimensions are supported
        raise ValueError(f"""The {ord_num} variable of function {validate_function.__name__}() has more than 2 dimensions. Currently only 1D and 2D arrays are supported. If the usage of a high dimensional array is in your intension, then it is suggested to deactivate the value check for this input by using this parameter:""" + "{'noCheck': ''}")                     
    elif ndims == 2:
        # if 2D array has shape (1, N) or (N, 1) then turn it to a column vector (N, 1)
        if 1 in arg_shape:
            ndims = 1
            L = np.max(arg_shape)
            actual_arg.resize((L, 1))
            arg_shape = actual_arg.shape
    
    for Key in Keys:
        # the minLength, maxLength and rangeLength params can deal only with vector like arrays of shape: (N, 1), (1, N) & (N,)
        checkVal = accepted_arg_type[Key]

        if ndims == 1:
            if Key == 'minLength':
                CheckMin(ord_num, len(actual_arg), checkVal, validate_function, 'length')

            elif Key == 'maxLength':
                CheckMax(ord_num, len(actual_arg), checkVal, validate_function, 'length')

            elif Key == 'rangeLength':
                CheckRange(ord_num, len(actual_arg), checkVal, validate_function, 'length')

        if ndims == 1 or ndims == 2:
            if Key == 'rowsMin':
                CheckMin(ord_num, actual_arg.shape[0], checkVal, validate_function, 'number of rows')

            elif Key == 'rowsMax':
                CheckMax(ord_num, actual_arg.shape[0], checkVal, validate_function, 'number of rows')

            elif Key == 'rowsRange':
                CheckRange(ord_num, actual_arg.shape[0], checkVal, validate_function, 'number of rows')

            elif Key == 'colsMin':
                CheckMin(ord_num, actual_arg.shape[1], checkVal, validate_function, 'number of columns')

            elif Key == 'colsMax':
                CheckMax(ord_num, actual_arg.shape[1], checkVal, validate_function, 'number of columns')

            elif Key == 'colsRange':
                CheckRange(ord_num, actual_arg.shape[1], checkVal, validate_function, 'number of columns')

    # this case has been managed earlier
    # elif ndims > 2:
    #     pass


def CheckValues(arg_num, actual_arg, accepted_arg_types, validate_function):
    """
    This is the main way for checking the correctness of the inputs VALUES of a function.
    In fact this function checks if a number belongs to the desired domain/range or 
    whether a string, list or tuple length is higher/lower than a predefined threshold or even    
    if a number or string belongs to set of allowed values.
    """

    if type(actual_arg) in numberTypes + noneTypes:
        CheckNumber(arg_num, actual_arg, accepted_arg_types, validate_function)

    elif type(actual_arg) in stringTypes + noneTypes:
        CheckString(arg_num, actual_arg, accepted_arg_types, validate_function)

    elif type(actual_arg) in objectTypes + noneTypes:
        CheckObject(arg_num, actual_arg, accepted_arg_types, validate_function)

    elif type(actual_arg) in arrayType + noneTypes:        
        CheckArray(arg_num, actual_arg, accepted_arg_types, validate_function)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# DECORATORS
# ----------

def acceptedTypes(*accepted_arg_types, **args_dict):
    """
    A decorator which is used to check a function's inputs types.
    
    Arguments:
        *accepted_arg_types -- a tuple of types e.g. (<type 'list'>, <type 'str'>)
        **args_dict         -- a dictionary with additional arguments used mainly for activate/deactivate the
                               decorators functionality e.g. {'typesCheckEnabled': False}
                               currently, the supported dictionary fields are:
                               {'typesCheckEnabled': <bool>} --> this field enables/disables the type checks
    """
     
    def accept_decorator(validate_function):
        # check whether to apply the decoration functionality or not
        if 'typesCheckEnabled' in args_dict:
            if args_dict['typesCheckEnabled'] == False:
                return validate_function

        ObjectConsistencyCheck = True    
        if 'ObjectConsistencyCheck' in args_dict:
            ObjectConsistencyCheck = args_dict['ObjectConsistencyCheck']

        @functools.wraps(validate_function)
        def decorator_wrapper(*function_args, **function_args_dict):   
            function_args_default = get_default_args(validate_function)
            argNms = inspect.getfullargspec(validate_function)[0] # argument names (all names: vars and default values)

            if 'removeChecks' in function_args_dict:
                if function_args_dict['removeChecks'] == True:
                    return validate_function(*function_args, **function_args_dict)            

            # checks the number of the given types
            if len(accepted_arg_types) != len(function_args)+len(function_args_dict):
                K = function_args_dict.keys()
                for key in function_args_default.keys():
                    if key not in K:
                        function_args_dict.update({key: function_args_default[key]})

            if len(accepted_arg_types) != len(function_args)+len(function_args_dict):
                raise ValueError('Invalid number of arguments for {0}()'.format(validate_function.__name__))  
                         
            # checks the validity of the examined function's types
            for arg_num, actual_arg in enumerate(function_args):
                accepted_arg_type = accepted_arg_types[arg_num]            
                
                CheckTypes(arg_num, actual_arg, accepted_arg_type, validate_function) #, ObjectConsistencyCheck)


            for idx, arg_key in enumerate(function_args_dict):                
                arg_num           = argNms.index(arg_key) 
                accepted_arg_type = accepted_arg_types[arg_num]
                actual_arg        = function_args_dict[arg_key]

                CheckTypes(arg_num, actual_arg, accepted_arg_type, validate_function) #, ObjectConsistencyCheck)
 
            return validate_function(*function_args, **function_args_dict)
        return decorator_wrapper
    return accept_decorator


def acceptedValues(*accepted_arg_types, **args_dict):
    """
    A decorator which is used to check a function's inputs values.
    
    Arguments:
        *accepted_arg_types -- a tuple of dicts e.g. ({'range': [1, 10]}, {'set': [1,2,3,4,5]})
        **args_dict         -- a dictionary with additional arguments used mainly for activate/deactivate the
                               decorators functionality e.g. {'valueCheckEnabled': False}
                               currently, the supported dictionary fields are:
                               {'valueCheckEnabled': <bool>} --> this field enables/disables the type checks
    """

    def accept_decorator(validate_function):
        # check whether to apply the decoration functionality or not
        if len(args_dict) > 0:  
            if args_dict['valueCheckEnabled'] == False:
                return validate_function
                
        @functools.wraps(validate_function)
        def decorator_wrapper(*function_args, **function_args_dict):
            function_args_default = get_default_args(validate_function)
            argNms = inspect.getfullargspec(validate_function)[0] # argument names (all names: vars and default values)

            # =========== 1st WAY ===================================
            # sig = inspect.signature(validate_function)
            # ba = sig.bind(*function_args, **function_args_dict)
            # for param in sig.parameters.values():
            #     if param.name not in ba.arguments:
            #         ba.arguments[param.name] = param.default
            # BA = ba.arguments

            # if 'removeChecks' in function_args_dict:
            #     if function_args_dict['removeChecks'] == True:
            #         return validate_function(*function_args, **function_args_dict)

            # if len(accepted_arg_types) != len(BA): 
            #     raise ValueError('Invalid number of arguments for {0}()'.format(validate_function.__name__))  

            # for idx, arg_key in enumerate(BA.keys()):                
            #     arg_num = argNms.index(arg_key) # find the correct index
            #     actual_arg = BA[arg_key]

            #     CheckValues(arg_num, actual_arg, accepted_arg_types, validate_function)
            # =========== END OF 1st WAY =============================



            # =========== 2nd WAY ===================================
            if 'removeChecks' in function_args_dict:
                if function_args_dict['removeChecks'] == True:
                    return validate_function(*function_args, **function_args_dict)

            # checks the number of the given types
            if len(accepted_arg_types) != len(function_args)+len(function_args_dict):
                K = function_args_dict.keys()
                for key in function_args_default.keys():
                    if key not in K:
                        function_args_dict.update({key: function_args_default[key]})

            if len(accepted_arg_types) != len(function_args)+len(function_args_dict):
                raise ValueError('Invalid number of arguments for {0}()'.format(validate_function.__name__))  

            # checks the validity of the examined function's values
            for arg_num, actual_arg in enumerate(function_args):
                CheckValues(arg_num, actual_arg, accepted_arg_types, validate_function)                    


            for idx, arg_key in enumerate(function_args_dict):                
                arg_num = argNms.index(arg_key)
                actual_arg = function_args_dict[arg_key]

                CheckValues(arg_num, actual_arg, accepted_arg_types, validate_function)  
            # =========== END OF 2nd WAY =============================          

            return validate_function(*function_args, **function_args_dict)
        return decorator_wrapper
    return accept_decorator
