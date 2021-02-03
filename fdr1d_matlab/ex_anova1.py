
from matplotlib import pyplot
import spm1d
import fdr1d


#(0) Load dataset:
dataset      = spm1d.data.uv1d.anova1.SpeedGRFcategorical()
dataset      = spm1d.data.uv1d.anova1.Weather()
Y,A          = dataset.get_data()



#(1) Run ANOVA:
alpha        = 0.05
F            = spm1d.stats.anova1(Y, A, equal_var=True)
Fi           = F.inference(alpha, interp=True, circular=False)
print( Fi )
fstar_fdr    = fdr1d.inference(F, alpha=alpha)
### alternative syntax:
# Y0,Y1,Y2     = [Y[A==u] for u in np.unique(A)]
# F            = spm1d.stats.anova1((Y0,Y1,Y2), equal_var=False)


#(2) Plot results:
pyplot.close('all')
ax           = pyplot.axes()
Fi.plot(ax=ax)
Fi.plot_threshold_label(bbox=dict(facecolor='w'))
# pyplot.ylim(-1, 500)
pyplot.xlabel('Time (%)', size=20)
pyplot.title(r'Critical threshold at $\alpha$=%.2f:  $F^*$=%.3f' %(alpha, Fi.zstar))

if fstar_fdr is not None:
	ax.axhline(fstar_fdr, color='b', linestyle='--')
	ax.text(50, fstar_fdr-0.3, r'$t^*$ (FDR) = %.3f' %fstar_fdr, color='b', size=8)

pyplot.show()





