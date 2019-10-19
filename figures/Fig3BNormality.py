#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:55:22 2019

@author: hanaa
"""


from matplotlib import pyplot
import spm1d
import fdr1d


#(0) Load dataset:
dataset      = spm1d.data.mv1d.cca.Dorn2012()
Y,x          = dataset.get_data()  



#(1) Conduct test:

pyplot.close('all')
pyplot.figure(  )
ax     = pyplot.axes()


alpha        = 0.05
two_tailed   = True
mu           = 0
y            = Y[:,:,2]

t          = spm1d.stats.regress(y, x)
ti         = t.inference(alpha, two_tailed=two_tailed, interp=True, circular=False)

n  = spm1d.stats.normality.k2.regress(y, x)
ni = n.inference(0.05)
ni.plot()

ax.set_ylabel('K2 value', fontsize=18)
ax.set_xlabel('Time (%)', fontsize=18)
ax.text(1, 14, 'B', color='k', fontsize= 20) 

pyplot.show()