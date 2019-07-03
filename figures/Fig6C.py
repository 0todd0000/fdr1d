#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 16:14:16 2019

@author: hanaa
"""

from math import sqrt
import numpy as np
from matplotlib import pyplot
import fdr1d 
import power1d
import spm1d 

def custom_legend(ax, colors=None, labels=None, linestyles=None, linewidths=None, markerfacecolors=None, **kwdargs):
	n      = len(colors)
	if linestyles is None:
		linestyles = ['-']*n
	if linewidths is None:
		linewidths = [1]*n
	if markerfacecolors is None:
		markerfacecolors = colors
	x0,x1  = ax.get_xlim()
	y0,y1  = ax.get_ylim()
	h      = [ax.plot([x1+1,x1+2,x1+3], [y1+1,y1+2,y1+3], ls, color=color, linewidth=lw, markerfacecolor=mfc)[0]   for color,ls,lw,mfc in zip(colors,linestyles,linewidths,markerfacecolors)]
	ax.set_xlim(x0, x1)
	ax.set_ylim(y0, y1)
	return ax.legend(h, labels, **kwdargs, fontsize =14)	



#(0) Set parameters:

np.random.seed(0)
J_sim         = np.arange(5, 51, 3)
nNodes        = 101
WW            = [10, 20, 30]
alpha         = 0.05
nIterations   = 100   #change this to 10000 to replicate the paper’s results
Q      = 101 
q      = 50
sigma  = 20 
amp    = 1.0 

FD1     = []

for J in J_sim:
    fp_fdr1 = []
    df     = J-1
    sqrtJ  = sqrt(J)
    for i in range(nIterations):
        signal = power1d.geom.GaussianPulse(Q=Q, q=q, sigma=sigma, amp=amp).toarray()
        noise  = spm1d.rft1d.randn1d(J, nNodes, FWHM= WW[0], pad=True)
        y = signal + noise
        t = y.mean(axis=0) / y.std(ddof =1, axis=0) *sqrtJ
        tstar_fdr = fdr1d.inference_manual(t,df,alpha=0.05, two_tailed=False, stat='T')
        if tstar_fdr is None:
            tstar_fdr = np.nan    
        fp_fdr1.append(tstar_fdr)
    FD1.append(fp_fdr1)
    
FD1     = np.asarray(FD1)
fp_fdr1 = np.nanmean(FD1,axis=1)

FD2     = []

for J in J_sim:
    fp_fdr2 = []
    df     = J-1
    sqrtJ  = sqrt(J)
    for i in range(nIterations):
        signal = power1d.geom.GaussianPulse(Q=Q, q=q, sigma=sigma, amp=amp).toarray()
        noise  = spm1d.rft1d.randn1d(J, nNodes, FWHM= WW[1], pad=True)
        y = signal + noise
        t = y.mean(axis=0) / y.std(ddof =1, axis=0) *sqrtJ
        tstar_fdr = fdr1d.inference_manual(t,df,alpha=0.05, two_tailed=False, stat='T')
        if tstar_fdr is None:
            tstar_fdr = np.nan    
        fp_fdr2.append(tstar_fdr)
    FD2.append(fp_fdr2)
    
FD2     = np.asarray(FD2)
fp_fdr2 = np.nanmean(FD2,axis=1)

FD3     = []

for J in J_sim:
    fp_fdr3 = []
    df     = J-1
    sqrtJ  = sqrt(J)
    for i in range(nIterations):
        signal = power1d.geom.GaussianPulse(Q=Q, q=q, sigma=sigma, amp=amp).toarray()
        noise  = spm1d.rft1d.randn1d(J, nNodes, FWHM= WW[2], pad=True)
        y = signal + noise
        t = y.mean(axis=0) / y.std(ddof =1, axis=0) *sqrtJ
        tstar_fdr = fdr1d.inference_manual(t,df,alpha=0.05, two_tailed=False, stat='T')
        if tstar_fdr is None:
            tstar_fdr = np.nan    
        fp_fdr3.append(tstar_fdr)
    FD3.append(fp_fdr3)
    
FD3     = np.asarray(FD3)
fp_fdr3 = np.nanmean(FD3,axis=1)



J_theor    = np.linspace(J_sim[0], J_sim[-1], 51)

ISF1     = []
for J in J_theor:
    y1 = spm1d.rft1d.t.isf(0.05, (J-1), nNodes, WW[0], withBonf = False )
    ISF1.append(y1)
ISF1   = np.asarray(ISF1)



ISF2     = []
for J in J_theor:
    y2 = spm1d.rft1d.t.isf(0.05, (J-1), nNodes, WW[1], withBonf = False )
    ISF2.append(y2)
ISF2   = np.asarray(ISF2)


ISF3     = []
for J in J_theor:
    y3 = spm1d.rft1d.t.isf(0.05, (J-1), nNodes, WW[2], withBonf = False )
    ISF3.append(y3)
ISF3   = np.asarray(ISF3)



#(3) Plot results:

pyplot.close('all')
ax            = pyplot.axes()
ax.plot(J_theor, ISF1, '-', color='k')
ax.plot(J_theor, ISF2, '-', color='0.5')
ax.plot(J_theor, ISF3, '-', color='0.7')

ax.plot(J_sim, fp_fdr1, 'o',color='k')
ax.plot(J_sim, fp_fdr2, 'o', color='0.5')
ax.plot(J_sim, fp_fdr3, 'o', color='0.7')

ax.set_xlabel('Sample size', size=18)
ax.text(4, 10.1, 'c', fontsize=20, color='k')


ax.set_ylim(1.5,10)
ax.set_xlim(4,52)




colors           = ['k', '0.5', '0.7','1', 'k', 'k']
labels           = ['FWHM = 10%', 'FWHM = 20%','FWHM = 30%','','RFT threshold', 'FDR threshold']
linestyles       = ['-','-','-','-','-','o']
linewidths       = [1,2,4,1,1,1]

legend_object    = custom_legend(ax, colors, labels, linestyles, linewidths)



ax.set_ylim(1.5,10)
ax.set_xlim(4,52)

pyplot.style.use('classic')
pyplot.rcParams['figure.facecolor'] = 'white'

pyplot.rc('xtick',labelsize=18)
pyplot.rc('ytick',labelsize=18)


pyplot.show()