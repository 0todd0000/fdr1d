
from matplotlib import pyplot
import spm1d
import fdr1d



#(0) Load data:
dataset      = spm1d.data.uv1d.t2.PlantarArchAngle()
# dataset      = spm1d.data.uv1d.t2.SimulatedTwoLocalMax()
YA,YB        = dataset.get_data()



#(1) Conduct t test:
alpha      = 0.05
two_tailed = False
t          = spm1d.stats.ttest2(YB, YA, equal_var=True)
ti         = t.inference(alpha, two_tailed=two_tailed, interp=True)
tstar_fdr  = fdr1d.inference(t, alpha=0.05, two_tailed=two_tailed)
print( ti )



#(2) Plot:
pyplot.close('all')
### plot mean and SD:
pyplot.figure( figsize=(8, 3.5) )
ax     = pyplot.axes( (0.1, 0.15, 0.35, 0.8) )
spm1d.plot.plot_mean_sd(YA)
spm1d.plot.plot_mean_sd(YB, linecolor='r', facecolor='r')
ax.axhline(y=0, color='k', linestyle=':')
ax.set_xlabel('Time (%)')
ax.set_ylabel('Plantar arch angle  (deg)')
### plot SPM results:
ax     = pyplot.axes((0.55,0.15,0.35,0.8))
ti.plot()
ti.plot_threshold_label(fontsize=8)
ti.plot_p_values(size=10, offset_all_clusters=(0,0.9))
ax.set_xlabel('Time (%)')

if tstar_fdr is not None:
	ax.axhline(tstar_fdr, color='b', linestyle='--')
	ax.text(50, tstar_fdr-0.3, r'$t^*$ (FDR) = %.3f' %tstar_fdr, color='b', size=8)

pyplot.show()
