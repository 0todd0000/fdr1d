
from matplotlib import pyplot
import spm1d
import fdr1d



#(0) Load dataset:
dataset    = spm1d.data.uv1d.regress.SimulatedPataky2015c()
dataset    = spm1d.data.uv1d.regress.SpeedGRF()
Y,x        = dataset.get_data()



#(1) Conduct regression:
alpha      = 0.05
two_tailed = False
t          = spm1d.stats.regress(Y, x)
ti         = t.inference(alpha, two_tailed=two_tailed, interp=True)
tstar_fdr  = fdr1d.inference(t, alpha=0.05, two_tailed=two_tailed)



#(2) Plot:
pyplot.close('all')
ax     = pyplot.axes()
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offsets=[(0,0.3)])
ax.set_xlabel('Time (%)')

if tstar_fdr is not None:
	ax.axhline(tstar_fdr, color='b', linestyle='--')
	ax.text(50, tstar_fdr-0.3, r'$t^*$ (FDR) = %.3f' %tstar_fdr, color='b', size=8)

pyplot.show()


