#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 14:19:08 2019

@author: hanaa
"""

from matplotlib import pyplot
import spm1d
import fdr1d
from scipy import stats
import numpy as np 

def fdr_warwick(p, q, df):
    '''
    Translated from fdr.m:
    
    https://warwick.ac.uk/fac/sci/statistics/staff/academic-research/nichols/software/fdr/
    '''
    
    p    = p[ np.isfinite(p) ]
    p    = np.sort(p)
    V    = p.size 
    I    = np.arange(V) + 1
    cVID = 1
    cVN  = np.sum( 1. / I  )
    pID  = 0
    pN   = 0
    ind  = np.argwhere(  p <= I / V * alpha / cVID ).flatten()
    if ind.size > 0:
        pID = p[ ind[-1] ] 
        zstarID = stats.t.isf(pID, df)
        
    ind  = np.argwhere(  p <= I / V * alpha / cVN  ).flatten()
    if ind.size > 0:
        pN = p[ ind[-1] ] 
        zstarN = stats.t.isf(pN, df)
    
    return pID,  zstarID, pN, zstarN



#(0) Load dataset:
dataset      = spm1d.data.mv1d.cca.Dorn2012()
Y,x          = dataset.get_data()  

#(1) Conduct test:
alpha        = 0.05
two_tailed   = True
mu           = 0
y            = Y[:,:,2]

t          = spm1d.stats.regress(y, x)
ti         = t.inference(alpha, two_tailed=two_tailed, interp=True, circular=False)
tstar_fdr  = fdr1d.inference(t, alpha= alpha, two_tailed=two_tailed)


#(2) Compute point-wise, uncorrected p values:
z          = t.z
df         = t.df[1]
p          = stats.t.sf(z, df)


#(3) FDR critical p values:
q          = 0.05
pID, zstarID, pN, zstarN  = fdr_warwick(p, q, df)
print( 'pID (fdr_warwick): %.6f' %pID )
print( 'pN  (fdr_warwick): %.6f' %pN )
print()
print( 'zstarID (fdr_warwick): %.6f' %zstarID )
print( 'zstarN (fdr_warwick): %.6f' %zstarN )
print()




#(2) Plot:

pyplot.close('all')
pyplot.figure(  )
ax     = pyplot.axes()

ti.plot(plot_ylabel= False, facecolor='w', thresh_color='w')

#ax.axhline(ti.zstar, color='k', linestyle='--', lw=2, label =r'$t^*$ (RFT) = ± %.3f'%ti.zstar)
#ax.axhline(- ti.zstar, color='k', linestyle='--', lw=2)


ax.set_xlabel('Time (%)', fontsize=18)

if zstarID is not None: 
    ax.axhline(zstarID, color='0.8', linestyle ='--', lw=2)
    ax.axhline(-zstarID, color='0.8', linestyle ='--', lw=2)
    

#if tstar_fdr is not None:
# 	ax.axhline(tstar_fdr, color='k', linestyle='-.', lw=2, label =r'$t^*$ (FDR) = ± %.3f'%tstar_fdr)

    
if zstarN is not None:
    ax.axhline(zstarN, color='0.8', linestyle='-.', lw=4)
    
if zstarN is not None:
    ax.axhline(-zstarN, color='0.8', linestyle='-.', lw=4)
    
#if - tstar_fdr is not None:
#	ax.axhline(-tstar_fdr, color='k', linestyle='-.', lw=2)


ax.text(0.3, 8.3, 'B', color='k', fontsize= 20) 
ax.set_xlabel('Time (%)', fontsize=18)
#ax.legend(loc =4, fontsize=18)  
ax.text(60, 5.3, 'FDR-no-ind', color='k', fontsize= 12) 
ax.text(60, 3.2, 'FDR-ind', color='k', fontsize= 12) 
ax.text(60, -5.8, 'FDR-no-ind', color='k', fontsize= 12) 
ax.text(60, -2.8, 'FDR-ind', color='k', fontsize= 12)

ax2 = ax.twinx()



ax.set_yticklabels([])
ax2.set_yticklabels([])


pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)
ax.set_ylim(-8,8)

pyplot.rcParams['figure.facecolor'] = 'white'
pyplot.show()