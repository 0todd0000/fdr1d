#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:28:49 2019

@author: hanaa
"""


from math import sqrt
import numpy as np
from matplotlib import pyplot
import fdr1d 
import spm1d
import power1d 


Q     = 101 
q     = 100
sigma = 3.0
amp   = 2.3
signal= power1d.geom.GaussianPulse(Q=Q, q=q, sigma=sigma, amp=amp).toarray()

np.random.seed(200)
J     = 10
FWHM  = 20.37196
noise = spm1d.rft1d.randn1d(J, Q, FWHM, pad=True)

y     = signal + noise

alpha = 0.05 
df    = J-1
sqrtJ  = sqrt(J)




y      = signal + noise #difference YA-YB
t      = y.mean(axis=0) / y.std(ddof =1, axis=0) *sqrtJ 
tstar_fdr = fdr1d.inference_manual(t,df,alpha=0.05, two_tailed=True, stat='T')




thresh_rft = spm1d.rft1d.t.isf(alpha/2, df, Q, FWHM)


pyplot.figure()
ax     = pyplot.axes()
ax.plot(t, color='k')

ax.axhline(thresh_rft, color='k', ls='--', label =r'$t^*$ (RFT) = ± %.3f'%thresh_rft)
ax.axhline(tstar_fdr, color='k', ls=':',  label =r'$t^*$ (FDR) = ± %.3f'%tstar_fdr)


ax.axhline(-tstar_fdr, color='k', ls=':')
ax.axhline(-thresh_rft, color='k', ls='--')
ax.plot(thresh_rft, '--', color='r')
#ax.text(1, 3, 'RFT ', color='k')
#ax.text(2, 4, 'FDR', color='k')
ax.set_xlabel('Time(%)', fontsize =18)
ax.set_ylabel('t value', fontsize=18)
ax.legend(loc =0, fontsize= 'large')  
#ax.set_title('Suprathreshold cluster "Dataset A"', fontsize=18)
ax.text(-1, 8.2, 'a', color='k', fontsize= 24)
pyplot.rc('axes', labelsize= 10)
pyplot.xlim(0, 100)

ax.axhline(0, color='black', ls=':', lw =0.9)

ax.legend(loc =4, fontsize=18)   


pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)
ax.set_ylim(-8,8)


pyplot.show()




