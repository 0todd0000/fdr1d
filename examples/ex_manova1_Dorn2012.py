
from matplotlib import pyplot
import spm1d
import fdr1d



#(0) Load data:
dataset      = spm1d.data.mv1d.manova1.Dorn2012()
Y,A          = dataset.get_data()  #A:slow, B:fast
print( dataset )



#(1) Conduct test:
alpha        = 0.05
X2           = spm1d.stats.manova1(Y, A)
X2i          = X2.inference(0.05)
zstar_fdr    = fdr1d.inference(X2, alpha=0.05)



#(2) Plot:
pyplot.close('all')
X2i.plot()
X2i.plot_p_values()

ax           = pyplot.gca()
if zstar_fdr is not None:
	ax.axhline(zstar_fdr, color='b', linestyle='--')
	ax.text(50, zstar_fdr-0.3, r'$t^*$ (FDR) = %.3f' %zstar_fdr, color='b', size=8)

pyplot.show()

