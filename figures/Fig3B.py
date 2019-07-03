#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 14:19:08 2019

@author: hanaa
"""

from matplotlib import pyplot
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


pyplot.close('all')
pyplot.figure()

ax     = pyplot.axes()
ti.plot(facecolor='w', thresh_color='w', plot_ylabel = False)
ax.set_xlabel('Time (%)', fontsize= 18)

ax.axhline(ti.zstar, color='k', linestyle='--', lw =2, label =r'$t^*$ (RFT) = ± %.3f'%ti.zstar)
ax.axhline(- ti.zstar, color='k', linestyle='--', lw=2)

if tstar_fdr is not None:
 	ax.axhline(tstar_fdr, color='k', linestyle=':', lw=2, label =r'$t^*$ (FDR) = ± %.3f'%tstar_fdr)

    
if - tstar_fdr is not None:
	ax.axhline(-tstar_fdr, color='k', linestyle=':', lw=2)





ax.legend(loc =4, fontsize= 18)  
ax.text(-0.8, 8.2, 'b', color='k', fontsize= 24)

ax.set_ylim(-8,8)

ax2 = ax.twinx()



ax.set_yticklabels([])
ax2.set_yticklabels([])



ax.legend(loc =4, fontsize=18)   
pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)
ax.set_ylim(-8,8)

pyplot.rcParams['figure.facecolor'] = 'white'
pyplot.show()
    
