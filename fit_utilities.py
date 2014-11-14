#!/usr/bin/python
#
# Fitting utilities
#

import numpy as np
from iminuit import Minuit
from probfit import Chi2Regression
from timing_utilities import *
from math import pi, sqrt, exp
from scipy.special import erf
sqrtpi = sqrt(pi)
sqrt2 = sqrt(2)


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

def fit_power_lawab(x, y, ey, **kwargs):
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

def fit_pulse_simple(x, y, ey, **kwargs):
    x2reg= Chi2Regression(pulse_shape_simple, x, y, ey)
    m= Minuit(x2reg, **kwargs)
    m.migrad()
    m.hesse()
    return x2reg, m

def GExp(x, x0, sigma, tau, N=1):
    '''
    An exponential convolved with a Gaussian
    The area is normalized to N.
    '''
    A = 0.5 * N * np.exp(0.5*(sigma/tau)**2) / tau
    z = -(x-x0)/sqrt2/sigma + sigma/sqrt2/tau
    return A * np.exp(-(x-x0)/tau) * (1 - erf(z))

def GExp2(x, x0, sigma, tau1, tau2, N=1):
    '''
    exp(-(x-x0)/tau1)-exp(-(x-x0)/tau2)   convolved with an unbiased Gaussian
    of width sigma.
    '''
    return N*(tau1*GExp(x,x0,sigma,tau1)-tau2*GExp(x,x0,sigma,tau2))/(tau1-tau2)

def fit_gexp(x, y, err=None, **kwargs):
    x2reg = Chi2Regression(GExp2, x, y, err)
    m= Minuit(x2reg, **kwargs)
    m.migrad()
    #m.hesse()
    return x2reg, m

