#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 18:06:55 2019

@author: hanaa
"""

from matplotlib import pyplot
from scipy import stats 
import spm1d
import fdr1d



#(0) Load data:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
YA,YB        = dataset.get_data()  #normal and fast walking



#(1) Conduct t test:
alpha      = 0.05
t          = spm1d.stats.ttest_paired(YA, YB)
ti         = t.inference(alpha, two_tailed=True, interp=True)
tstar_fdr  = fdr1d.inference(t, alpha=0.05, two_tailed= True)


t_0D       = spm1d.rft1d.t.isf0d(alpha/2,9)

p_Bonfe = spm1d.util.p_critical_bonf(alpha,101)

t_Bonfe = stats.t.isf(p_Bonfe/2, 9)

#(2) Plot:

pyplot.close('all')
pyplot.figure(  )
ax     = pyplot.axes()

ti.plot(plot_ylabel= False, facecolor='w', thresh_color='w')


ax.axhline(- ti.zstar, color='k', linestyle='--', lw=2)
ax.axhline(t_Bonfe, color='0.7', linestyle=':', lw=5)
ax.axhline(-t_Bonfe, color='0.7', linestyle=':', lw=5)
ax.axhline (t_0D, color='0.7', linestyle ='--', lw=2)
ax.axhline (-t_0D, color='0.7', linestyle ='--', lw=2)




if tstar_fdr is not None:
 	ax.axhline(tstar_fdr, color='k', linestyle='-.', lw=2, label =r'$t^*$ (FDR) = ± %.3f'%tstar_fdr)

    
if - tstar_fdr is not None:
	ax.axhline(-tstar_fdr, color='k', linestyle='-.', lw=2)

ax.axhline(ti.zstar, color='k', linestyle='--', lw=2, label =r'$t^*$ (RFT) = ± %.3f'%ti.zstar)

ax.text(-1, 8.2, 'a', color='k', fontsize= 24)
ax.text(30, 4.4, 'FDR', color='k', fontsize= 12) 
ax.text(30, - 4.7, 'FDR', color='k', fontsize= 12)
ax.text(30, 3.2, 'RFT', color='k', fontsize= 12) 
ax.text(30, -3.6, 'RFT', color='k', fontsize= 12) 
ax.text(60, 4.7, 'Bonferroni', color='k', fontsize= 12) 
ax.text(60, - 5, 'Bonferroni', color='k', fontsize= 12) 
ax.text(60, 1.7, 'Uncorrected', color='k', fontsize=12) 
ax.text(60, -2, 'Uncorrected', color='k', fontsize=12) 
ax.set_xlabel('Time (%)', fontsize=18)
ax.set_ylabel('t value', fontsize=18)   
ax.set_ylim(-8,8)

#ax.legend(loc =4, fontsize=18) 

pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)

pyplot.show()