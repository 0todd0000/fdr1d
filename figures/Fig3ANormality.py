#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:38:13 2019

@author: hanaa
"""

from matplotlib import pyplot
import spm1d
import fdr1d




#(0) Load data:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
YA,YB        = dataset.get_data()  #normal and fast walking



#(1) Conduct t test:

pyplot.close('all')
pyplot.figure(  )
ax     = pyplot.axes()

alpha      = 0.05
t          = spm1d.stats.ttest_paired(YA, YB)
ti         = t.inference(alpha, two_tailed=True, interp=True)
tstar_fdr  = fdr1d.inference(t, alpha=0.05, two_tailed= True)


n  = spm1d.stats.normality.k2.ttest_paired(YA, YB)



ni = n.inference(0.05)
ni.plot(plot_ylabel= False)



ax.set_ylabel('K2 value', fontsize=18)
ax.set_xlabel('Time (%)', fontsize=18)
ax.text(1, 12, 'A', color='k', fontsize= 20) 

pyplot.show()