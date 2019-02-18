
from matplotlib import pyplot
import spm1d
import fdr1d



#(0) Load dataset:
dataset    = spm1d.data.uv1d.t1.Random()
Y,mu       = dataset.get_data()



#(1) Conduct t test:
alpha      = 0.05
two_tailed = False
t          = spm1d.stats.ttest(Y, mu)
ti         = t.inference(alpha, two_tailed=two_tailed, interp=True, circular=False)
tstar_fdr  = fdr1d.inference(t, alpha=0.05, two_tailed=two_tailed)




#(2) Plot:
pyplot.close('all')
### plot mean and SD:
pyplot.figure( figsize=(8, 3.5) )
ax     = pyplot.axes( (0.1, 0.15, 0.35, 0.8) )
spm1d.plot.plot_mean_sd(Y)
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Measurement domain (%)')
ax.set_ylabel('Dependent Variable')
### plot SPM results:
ax     = pyplot.axes((0.55,0.15,0.35,0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offsets=[(0,0.3)])
ax.set_xlabel('Measurement domain (%)')

if tstar_fdr is not None:
	ax.axhline(tstar_fdr, color='b', linestyle='--')
	ax.text(50, tstar_fdr-0.3, r'$t^*$ (FDR) = %.3f' %tstar_fdr, color='b', size=8)

pyplot.show()