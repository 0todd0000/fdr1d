
__version__ = '0.01'  #2019.02.12


import numpy as np
from scipy import stats


eps    = np.finfo(float).eps  #smallest floating number greater than zero


def fpnp(z, zstar, signal):
	'''
	Compute the false positive node proportion (fpnp), where fpnp is defined as:
	
	fpnp = (num. false positives) / (num. positives)

	INPUTS:

	z : 1D test statistic continuum (one-dimensional numpy arrray)

	zstar : critical threshold

	signal : 1D binary continuum defining true signal nodes


	OUTPUTS:

	p : false positive node proportion
	'''
	pdefault      = 0
	if zstar is None:
		return pdefault
	z             = np.abs(z)
	b_trueneg     = signal == 0
	b_pos         = z > zstar
	npos          = b_pos.sum()
	if npos==0:
		p         = pdefault
	else:
		nfalsepos = b_pos[b_trueneg].sum()
		p         = nfalsepos / npos   #false positive node proportion
	return p



def inference(z, df, alpha=0.05, stat='T'):
	'''
	Compute the critical test statistic value using false discovery rate (FDR)-based inference.

	INPUTS:

	z : test statistic (one-dimensional numpy arrray)

	df : degrees of freedom (scalar for the T statistic, two-tuple for the F statistic)

	alpha : Type I error rate (scalar between 0 and 1)

	stat : type of test statistic ("T" or "F")


	OUTPUTS:

	zstar : critical test statistic value [None is returned if the test fails to reach significance]


	EXAMPLE:

	J     = 12   #sample size (number of 1D continua)
	Q     = 101  #number of continuum nodes
	y     = np.random.randn(J, Q)   #random sample of 1D continua
	t     = y.mean(axis=0) / (  y.std(ddof=1, axis=0)/ (J**0.5)  )  #1D t statistic
	tstar = fdr_inference(t, J-1, alpha=0.05, stat='T')
	print('Critical FDR threshold: %s'%tstar)
	'''
	
	z         = np.abs(z)
	
	# compute uncorrected p values:
	if stat=='T':
		p     = stats.t.sf(z, df)
	elif stat=='F':
		p     = stats.f.sf(z, *df)
	else:
		raise ValueError('"stat" must be "T" or "F"')

	# sort p values:
	i         = np.argsort(p)
	psorted   = p[i]

	#compute sorted p value threshold:
	Q         = z.size
	psortedth = alpha / Q * (np.arange(Q) + 1)

	#compute test statistic threshold
	b         = psorted < psortedth
	if np.any(b):
		istar = np.argwhere(b).flatten()[-1]
		zstar = z[i][istar] + eps
	else:
		zstar = None

	return zstar



