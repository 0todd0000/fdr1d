clear;  clc


%(0) Load data:
% dataset = spm1d.data.uv1d.regress.SimulatedPataky2015c();
dataset = spm1d.data.uv1d.regress.SpeedGRF();
[Y,x]  = deal(dataset.Y, dataset.x);



%(1) Conduct SPM analysis:
alpha      = 0.05;
two_tailed = false;
spm        = spm1d.stats.regress(Y, x);
spmi       = spm.inference(0.05, 'two_tailed', false);
zstar      = inference_fdr(spm, alpha, two_tailed);



%(2) Plot:
close all
spmi.plot();
spmi.plot_threshold_label();
spmi.plot_p_values();

line( xlim, [zstar zstar], 'color', 'blue', 'linestyle', '--');
text( mean(xlim), zstar, sprintf('t* (FDR) = %.3f', zstar), 'color', 'blue')