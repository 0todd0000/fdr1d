#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 13:43:17 2019

@author: hanaa
"""

from matplotlib import pyplot
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


#(2) Plot:

pyplot.close('all')
pyplot.figure(  )
ax     = pyplot.axes()

ti.plot(facecolor='w', thresh_color='w')

ax.axhline(ti.zstar, color='k', linestyle='--', lw=2, label =r'$t^*$ (RFT) = ± %.3f'%ti.zstar)
ax.axhline(- ti.zstar, color='k', linestyle='--', lw=2)


ax.set_xlabel('Time (%)', fontsize=18)

if tstar_fdr is not None:
 	ax.axhline(tstar_fdr, color='k', linestyle=':', lw=2, label =r'$t^*$ (FDR) = ± %.3f'%tstar_fdr)

    
if - tstar_fdr is not None:
	ax.axhline(-tstar_fdr, color='k', linestyle=':', lw=2)


ax.text(-1, 8.2, 'a', color='k', fontsize= 24) 
ax.set_xlabel('Time (%)', fontsize=18)
ax.legend(loc =4, fontsize=18)   
ax.set_ylim(-8,8)


pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)

pyplot.show()