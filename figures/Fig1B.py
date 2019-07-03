#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 14:23:59 2019

@author: hanaa
"""

from matplotlib import pyplot
import spm1d
import fdr1d

dataset      = spm1d.data.mv1d.cca.Dorn2012()
#RFT=14.97 and FDR=8.95
Y,x          = dataset.get_data()  #A:slow, B:fast 

#(1) Conduct test:
alpha        = 0.05
two_tailed   = True
mu           = 0
y            = Y[:,:,2]
y1           = y[0:2].mean(axis=0) 
y2           = y[2:4].mean(axis=0)
y3           = y[4:6].mean(axis=0)
y4           = y[6:8].mean(axis=0)

t          = spm1d.stats.regress(y, x)
ti         = t.inference(alpha, two_tailed=two_tailed, interp=True, circular=False)
tstar_fdr  = fdr1d.inference(t, alpha= alpha, two_tailed=two_tailed)


pyplot.close('all')
pyplot.figure()

ax     = pyplot.axes()

pyplot.plot(y1, color='k', lw =2,  label = '3.56 m/s')
pyplot.plot(y2, color='0.5', lw =3,  label = '5.20 m/s')
pyplot.plot(y3, color='0.7',  lw=4, label = '7.00 m/s')
pyplot.plot(y4, color = '0.9',lw=5, label = '9.49 m/s')
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Time (%)', fontsize = 18)
ax.set_ylabel('Force (N)', fontsize = 18) 
pyplot.rcParams.update({'font.size': 16}) 
ax.text(-0.8, 310, 'b', color='k', fontsize= 24)
ax.set_ylim(-300,300)

ax.legend(loc =4, fontsize= 18)  


ax.legend(loc =4, fontsize=18)   
pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)

pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'
pyplot.show()