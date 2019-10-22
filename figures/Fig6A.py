#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:25:39 2019

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
S_sim         = [0, 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
nNodes        = 101
J             = 8
alpha         = 0.05
nIterations   = 10
Q       = 101
q       = 50
amp     = 3
FWHM    = 20 
### derived parameters:
df     = J - 1
sqrtJ  = sqrt(J)
alpha  = 0.05    



ISF     = []
for S in S_sim:
    y1 = spm1d.rft1d.t.isf(0.05, (J-1), nNodes, FWHM, withBonf = False )
    ISF.append(y1)
ISF   = np.asarray(ISF)



FD     = []

for S in S_sim:
    fp_fdr = []
    for i in range(nIterations):
        signal = power1d.geom.GaussianPulse(Q =Q, q= q, sigma = S, amp=amp).toarray()
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
ax      = pyplot.axes()
ax.plot(S_sim, ISF, '-', color='k', linewidth= 1, label = 'RFT threshold')
ax.plot(S_sim, fp_fdr, '--',color='k', linewidth= 1, label = 'FDR threshold')
ax.set_xlim(0,20)
ax.set_ylim(1.5,10)
ax.set_xlabel('σ (%)', size=18)
ax.set_ylabel('Critical t value', size=18)
ax.legend(fontsize = 14)

ax.text(0, 10.1, 'a', fontsize=20, color='k')

pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)

pyplot.show()