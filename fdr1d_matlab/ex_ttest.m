clearvars
%addpath
addpath('C:\Users\s5001683\Documents\MATLAB\spm1d');
addpath('C:\Users\s5001683\Documents\MATLAB\spm1d\spm8');

%(0) Load dataset:
dataset    = spm1d.data.uv1d.t1.Random();
[Y,mu]     = deal( dataset.Y, dataset.mu );
stat       = 'T';


%(1) Conduct SPM analysis:
alpha         = 0.05;
two_tailed    = false;
spm           = spm1d.stats.ttest(Y - mu);
spmi          = spm.inference(alpha, 'two_tailed', two_tailed);
zstar         = inference_fdr(spm, alpha, two_tailed);
% zstar         = inference_manual(spm.z, spm.df(2), alpha, stat, two_tailed);


%(2) Plot:
close all
spmi.plot();
spmi.plot_threshold_label();
spmi.plot_p_values();


line( xlim, [zstar zstar], 'color', 'blue', 'linestyle', '--');
text( mean(xlim), zstar, sprintf('t* (FDR) = %.3f', zstar), 'color', 'blue')