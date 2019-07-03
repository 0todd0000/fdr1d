#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:26:50 2019

@author: hanaa
"""

import numpy as np 
 
from matplotlib import pyplot 
import spm1d 
import power1d 
import fdr1d 

def tstat_regress(Y, x):
	X      = np.ones((Y.shape[0],2))
	X[:,0] = x
	### assemble data:
	Y      = np.matrix(Y)
	X      = np.matrix(X)
	c      = np.matrix([1,0]).T
	### solve:
	b      = np.linalg.pinv(X)*Y            #parameters
	eij    = Y - X*b                        #residuals
	R      = eij.T*eij                      #residuals sum of squares
	df     = Y.shape[0] - 2                 #degrees of freedom
	sigma2 = np.diag(R)/df                  #variance
	### compute t statistic
	t = np.array(c.T*b).flatten()  /   np.sqrt(sigma2*float(c.T*(np.linalg.inv(X.T*X))*c))
	return t




#(0) Generate base signal:
Q         = 100 
q         = 17
sigma     = 19
amp       = 1.2
signal    = power1d.geom.GaussianPulse(Q=Q, q=q, sigma=sigma, amp=amp).toarray()



#(1) Create IV-dependent signal for regression analysis:
J         = 7
x         = np.arange(1, J+1)  
signal    = np.vstack( [signal]*J )  
ivsignal  = (x * signal.T).T         



#(2) Generate noise:
np.random.seed(200)
FWHM      = 7.94805
noise     = spm1d.rft1d.randn1d(J, Q, FWHM, pad=True)
noise     = 1.45* noise  



y         = ivsignal + noise



#(3) Calculate t statistic and conduct inference:
alpha     = 0.05 
df        = J-1
t         = tstat_regress(y, x)
tstar_rft = spm1d.rft1d.t.isf(alpha/2, df, Q, FWHM)
tstar_fdr = fdr1d.inference_manual(t,df,alpha=0.05, two_tailed=True, stat='T')



#(4) Plot:
pyplot.close('all')
ax     = pyplot.axes()




# plot statistical results:

ax.plot(t, 'k', lw=2)
ax.axhline(tstar_rft, color='k', ls='--', label =r'$t^*$ (RFT) = ± %.3f'%tstar_rft)
ax.axhline(tstar_fdr, color='k', ls=':', label =r'$t^*$ (FDR) = ± %.3f'%tstar_fdr)
ax.axhline(-tstar_rft, color='k', ls='--')
ax.axhline(-tstar_fdr, color='k', ls=':')
ax.legend(loc='upper right', fontsize=8)
ax.set_xlabel('Time (%)', fontsize =18)
ax.text(-1, 8.2, 'b', color='k', fontsize= 24)
#ax.set_ylabel('t value', fontsize = 18)

ax.set_xlim(0)
pyplot.ylim(-8, 8)

ax.axhline(0, color='black', ls=':', lw =0.9)

ax.legend(fontsize = 16)
ax.set_xlim(0, 100)
ax.legend(loc =4, fontsize=18) 
  
pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)
ax.set_ylim(-8,8)

ax2 = ax.twinx()



ax.set_yticklabels([])
ax2.set_yticklabels([])

pyplot.show()



