	
from matplotlib import pyplot
import spm1d
import fdr1d



#(0) Load data:
dataset      = spm1d.data.mv1d.hotellings2.Besier2009muscleforces()
YA,YB        = dataset.get_data()  #A:slow, B:fast
print( dataset )



#(1) Conduct test:
alpha        = 0.05
T2           = spm1d.stats.hotellings2(YA, YB)
T2i          = T2.inference(0.05)
zstar_fdr    = fdr1d.inference(T2, alpha=0.05)
print( T2i )


#(2) Plot:
pyplot.close('all')
T2i.plot()

ax           = pyplot.gca()
if zstar_fdr is not None:
	ax.axhline(zstar_fdr, color='b', linestyle='--')
	ax.text(50, zstar_fdr-0.3, r'$t^*$ (FDR) = %.3f' %zstar_fdr, color='b', size=8)

pyplot.show()


