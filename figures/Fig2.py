#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 19:11:06 2019

@author: hanaa
"""

import numpy as np

from matplotlib import pyplot
import spm1d    
import power1d  



Q       = 101  
q       = 50   
sigma   = 20   
amp     = 3.0  
signal  = power1d.geom.GaussianPulse(Q=Q, q=q, sigma=sigma, amp=amp).toarray()


pyplot.figure()
ax      = pyplot.axes()
ax.plot( signal, color='k', ls = '-' )
ax.axhline(0, color='k', ls=':')
ax.axvline(q, color='k', ls=':')
ax.set_xlabel('Continuum position (%)', fontsize =18)
ax.set_ylabel('DV value', fontsize = 18)
ax.set_title('Signal', fontsize =18)
ax.text(-1, 3.05, 'a', color='k', fontsize= 24)
ax.set_xlim(0)

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)


pyplot.plot([50, 50], [0, 3],color= '0.7', linestyle='-', linewidth=5)
pyplot.plot([50, 79], [1, 1],color= 'k', linestyle='-', linewidth=5)
ax.text(43, 2, 'amp', color='0.7', rotation = 'vertical', fontsize= 24)
ax.text(61, 1.1, 'σ', color='k', fontsize= 24)
pyplot.plot([0, 49], [0, 0],color= 'k', linestyle='-', linewidth=15)
ax.text(25, 0.2, 'q', color='k', fontsize= 24)
ax.set_xlim(0)
ax.set_ylim(0)

pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)

pyplot.show()

np.random.seed(200)
J     = 8               
FWHM  = 20              
noise = spm1d.rft1d.randn1d(J, Q, FWHM, pad=True) 
y     = signal + noise  


pyplot.figure()
ax      = pyplot.axes()
ax.plot( noise.T, color= 'k', ls = '-')
ax.axhline(0, color='k', ls=':')
ax.axvline(q, color='k', ls=':')
ax.set_xlabel('Continuum position (%)', fontsize=18)
ax.set_ylabel('DV value', fontsize = 18)
ax.set_title('Noise', fontsize =18)
ax.text(-1, 3.1, 'b', color='k', fontsize= 24) 
ax.set_xlim(0)

pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)

pyplot.show()


pyplot.figure()
ax      = pyplot.axes()
ax.plot( y.T, color= 'k')
ax.axhline(0, color='k', ls=':')
ax.axvline(q, color='k', ls=':')
ax.set_xlabel('Continuum position (%)', fontsize =18)
ax.set_ylabel('DV value', fontsize = 18)
ax.set_title('Simulated dataset', fontsize = 18)
pyplot.rc('axes', labelsize= 10)
ax.text(-1, 6.2, 'c', color='k', fontsize= 24)
ax.set_xlim(0)
ax.set_ylim(-3, 6)
pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)

pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)

pyplot.show()

