# InputCheck
This project created with the intention to offer an automated and easy way for checking the validity of a function's arguments. The main purpose is to eliminate additional code, which is frequently used to check functions inputs and to enhance code safety. The main idea is to use decorators to check  both arguments types & values. Note that these checks add some time overhead in the overall run time. Thus, it is suggested to be used in Non Time-Critical algorithms. However,  I believe that could be great help during the development process. Furthermore, a control flag can be used to deactivate the arguments checks, when speed matters, significantly reducing the additional time overhead. 

## Getting Started

The only dependency of this project is the *numpy* package, since, initially was meant to be used in a signal processing library.

### Prerequisites

If you use Anaconda or Miniconda, you can install the numpy package using the following command line (*Recommended*):

> $ conda install numpy

or with the traditional pip command:

> $ pip install numpy

### Installing

To install this package just download this repository from GitHub or by using the following command line:

> $ git clone https://github.com/ekarakasis/InputCheck

Afterwards, go to the local root folder, open a command line and run:

> $ pip install .

and if you want to install it to a specific Anaconda environment then write:

> $ activate <Some_Environment_Name>
>
> $ pip install .

### Uninstalling

To uninstall the package just open a command and write:

> $ pip unistall InputCheck

To uninstall it from a specific conda environment write:

> $ activate <Some_Environment_Name>
>
> $ pip unistall InputCheck

## Running the tests

To run the tests just follow these steps:

- open the local root folder of the package, 

- go to the subfolder *test*,

- open a command line and write:

  > $ python test_InputCheckDecorators.py -v

In case you want to use a specific conda environment then write:

> $ activate <Some_Environment_Name>
>
> $ python test_InputCheckDecorators.py -v

Alternatively, except of the `python test_InputCheckDecorators.py -v` you can also run the following command:

> \$ python test_all.py

## Examples

### Example 1

Let us assume a function Func1, which use one input and does nothing. And let us further assume that we want this input to be a number (integer or float, not None) and that this number can only take values in the range [1,10].

```python
from InputCheck.InputCheckDecorators import acceptedTypes, acceptedValues

@acceptedTypes([int, float])
@acceptedValues({'range': [1, 10]})
def Func1(input1): 
    pass
                       
try:
    Func1(None)
except Exception as ex:
    print(ex)
                 
try:
    Func1(0)
except Exception as ex:
    print(ex)
                 
try:
    Func1(20)
except Exception as ex:
    print(ex)                 
```

**OUTPUT:**

> The type of the 1st argument of function Func1() does not belong in [<class 'int'>, <class 'float'>]
>
> The 1st argument of the function Func1() has value out of the accepted range: [1, 10].
>
> The 1st argument of the function Func1() has value out of the accepted range: [1, 10].

Here,  we catch type and value errors that could probably cause a bug by adding just two lines of code. For more examples on how to use this library go to the [InputCheck_Docs.md](InputCheck_Docs.md).

## License

This project is licensed under the MIT License.

## Acknowledgments

The specific implementation of decorator-based checks of functions arguments has been inspired from Jackson Cooper's online article entitled "*Validate Python Function Parameter & Return Types with Decorators*" (https://www.pythoncentral.io/validate-python-function-parameters-and-return-types-with-decorators/)

Thanks for this great idea!