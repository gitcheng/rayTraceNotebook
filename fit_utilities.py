#!/usr/bin/python
#
# Fitting utilities
#

import numpy as np
from iminuit import Minuit
from probfit import Chi2Regression

def poly1(x, a, b):
    return x*a + b

def powerlaw(x, a, b):
    '''
    y = b * x^a
    '''
    return b * np.power(x, a)

def fit_power_law(x, y, ey):
    '''
    Use chisq regression to fit for y = exp(b) * x^a
    Return two dictionaries: one for the values of a and b.
    and the second for the errors.
    '''
    x2reg= Chi2Regression(poly1, np.log(x), np.log(y), error= ey/y)
    m = Minuit(x2reg, print_level=0, a= -0.5, error_a= 1, b=1, error_b=1)
    m.migrad()
    m.hesse()
    return m.values, m.errors

def fit_power_lawab(x, y, ey):
    '''
    Use chisq regression to fit for y = b * x^a
    Return two dictionaries: one for the values of a and b.
    and the second for the errors.
    '''
    x2reg= Chi2Regression(powerlaw, x, y, ey)
    m = Minuit(x2reg, print_level=0, a= -0.5, error_a= 0.1, b=10, error_b=1)
    m.migrad()
    m.hesse()
    return m.values, m.errors
