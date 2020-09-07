
import numpy as np
from matplotlib import pyplot
import spm1d
import fdr1d



#(0) Load data:
dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x2()
dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_2x3()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_3x3()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_3x4()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_3x5()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_4x4()
# dataset      = spm1d.data.uv1d.anova2.SPM1D_ANOVA2_4x5()
Y,A,B        = dataset.get_data()



#(1) Conduct ANOVA:
alpha        = 0.05
FF           = spm1d.stats.anova2(Y, A, B, equal_var=True)
FFi          = FF.inference(alpha)
fstars_fdr   = [fdr1d.inference(F, alpha=0.05)  for F in FF]
print( FFi )



#(2) Plot results:
pyplot.close('all')
FFi.plot(plot_threshold_label=True, plot_p_values=True)

for ax,z in zip(pyplot.gcf().axes, fstars_fdr):
	if z is not None:
		ax.axhline(z, color='b', linestyle='--')
		ax.text(50, z-0.3, r'$t^*$ (FDR) = %.3f' %z, color='b', size=8)

pyplot.show()





