#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:23:05 2019

@author: hanaa
"""

from matplotlib import pyplot
from scipy import stats 
import spm1d
import fdr1d




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



t_0D       = spm1d.rft1d.t.isf0d(alpha/2,6)

p_Bonfe = spm1d.util.p_critical_bonf(alpha,100)

t_Bonfe = stats.t.isf(p_Bonfe/2, 6)



pyplot.close('all')
pyplot.figure()

ax     = pyplot.axes()
ti.plot(facecolor='w', thresh_color='w', plot_ylabel = False)
ax.set_xlabel('Time (%)', fontsize= 18)


ax.axhline(ti.zstar, color='k', linestyle='--', lw =2)
ax.axhline(- ti.zstar, color='k', linestyle='--', lw=2)
ax.axhline(t_Bonfe, color='0.7', linestyle=':', lw=5)
ax.axhline(-t_Bonfe, color='0.7', linestyle=':', lw=5)
ax.axhline (t_0D, color='0.7', linestyle ='--', lw=2)
ax.axhline (-t_0D, color='0.7', linestyle ='--', lw=2)


if tstar_fdr is not None:
 	ax.axhline(tstar_fdr, color='k', linestyle='-.', lw=2)

    
if - tstar_fdr is not None:
	ax.axhline(-tstar_fdr, color='k', linestyle='-.', lw=2)






ax.text(-0.8, 8.2, 'b', color='k', fontsize= 24)
ax.text(48, 6.2, 'Bonferroni', color='k', fontsize= 12) 
ax.text(48, -7.4, 'Bonferroni', color='k', fontsize= 12) 
ax.text(48, 5.4, 'RFT', color='k', fontsize= 12)
ax.text(48, - 5.7, 'RFT', color='k', fontsize= 12)
ax.text(48, 2.9, 'FDR', color='k', fontsize= 12)
ax.text(48, - 3.3, 'FDR', color='k', fontsize= 12)
ax.text(25, 1.9, 'Uncorrected', color='k', fontsize= 12)
ax.text(25, - 2.2, 'Uncorrected', color='k', fontsize= 12)

ax.set_ylim(-8,8)

ax2 = ax.twinx()



ax.set_yticklabels([])
ax2.set_yticklabels([])


#ax.legend(loc =4, fontsize=18) 
  
pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)
ax.set_ylim(-8,8)

pyplot.rcParams['figure.facecolor'] = 'white'
pyplot.show()