#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:00:55 2019

@author: hanaa
"""

from math import sqrt
import numpy as np
from matplotlib import pyplot
import fdr1d 
import spm1d
import power1d 



#(0) Set parameters:
np.random.seed(0)
S_sim         = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4]

J             = 8
alpha         = 0.05
nIterations   = 100   #change this to 10000 to replicate the paper’s results
Q       = 101 
q       = 50
FWHM    = 20 
### derived parameters:
df     = J - 1
sqrtJ  = sqrt(J)
alpha  = 0.05    
sigma  = 20

ISF     = []
for S in S_sim:
    y1 = spm1d.rft1d.t.isf(0.05, (J-1), Q, FWHM, withBonf = False )
    ISF.append(y1)
ISF   = np.asarray(ISF)

FD     = []

for S in S_sim:
    fp_fdr = []
    for i in range(nIterations):
        signal = power1d.geom.GaussianPulse(Q =Q, q= q, sigma = sigma, amp=S).toarray()
        noise  = spm1d.rft1d.randn1d(J, Q, FWHM, pad=True)
        y = signal + noise 
        t = y.mean(axis=0) / y.std(ddof =1, axis=0) *sqrtJ
        tstar_fdr = fdr1d.inference_manual(t,df,alpha=0.05, two_tailed=False, stat='T')
        if tstar_fdr is None:
            tstar_fdr = np.nan    
        fp_fdr.append(tstar_fdr)
    FD.append(fp_fdr)
    
FD     = np.asarray(FD)
fp_fdr = np.nanmean(FD,axis=1)

pyplot.close('all')
ax            = pyplot.axes()
ax.plot(S_sim, ISF, '-', color='k', linewidth= 2, label = 'RFT threshold')
ax.plot(S_sim, fp_fdr, 'o',color='k', linewidth= 2, label = 'FDR threshold')
ax.set_xlabel('Signal amplitude (amp) ', size=18)

ax.legend(fontsize = 14)
pyplot.rcParams.update({'font.size': 18})
ax.text(0.2, 10.1, 'b', fontsize=20, color='k')

ax2 = ax.twinx()

ax.set_yticklabels([])
ax2.set_yticklabels([])

ax.set_xlim(0, 4.2)
ax.set_ylim(1.5,10)


pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)

pyplot.show()