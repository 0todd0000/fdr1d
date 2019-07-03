#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 13:41:21 2019

@author: hanaa
"""

from matplotlib import pyplot
import spm1d
import fdr1d



#(0) Load data:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
YA,YB        = dataset.get_data()  #slow and fast walking



#(1) Conduct t test:

alpha      = 0.05
t          = spm1d.stats.ttest_paired(YA, YB)
ti         = t.inference(alpha, two_tailed=True, interp=True)
tstar_fdr  = fdr1d.inference(t, alpha=0.05, two_tailed= True)


#(2) Plot:

pyplot.close('all')

### plot mean and SD:

pyplot.figure(  )
ax     = pyplot.axes()
spm1d.plot.plot_mean_sd(YA, linestyle ='-', label = 'Fast walking')
spm1d.plot.plot_mean_sd(YB, linestyle = ':', facecolor='k', label ='Slow walking')
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Time (%)', fontsize = 17)
ax.set_ylabel('Plantar arch angle  (deg)', fontsize = 17)
ax.text(-1, 9.3, 'a', color='k', fontsize= 24) 
ax.legend(loc =3, fontsize=18)   


pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)

pyplot.show()
