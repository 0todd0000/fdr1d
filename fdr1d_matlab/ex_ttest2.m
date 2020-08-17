
    
clear;  clc


%(0) Load data:
dataset = spm1d.data.uv1d.t2.PlantarArchAngle();
% dataset = spm1d.data.uv1d.t2.SimulatedTwoLocalMax();
[YA,YB] = deal(dataset.YA, dataset.YB);



%(1) Conduct SPM analysis:
alpha      = 0.05;
two_tailed = true;
spm        = spm1d.stats.ttest2(YA, YB);
spmi       = spm.inference(alpha, 'two_tailed', two_tailed, 'interp',true);
% FDR analysis
zstar      = inference(spmi, alpha, two_tailed);



%(2) Plot:
close all
spmi.plot();
spmi.plot_threshold_label();
spmi.plot_p_values();


line( xlim, [zstar zstar], 'color', 'blue', 'linestyle', '--');
text( mean(xlim), zstar, sprintf('t* (FDR) = %.3f', zstar), 'color', 'blue')
line( xlim, [-zstar -zstar], 'color', 'blue', 'linestyle', '--');
text( mean(xlim), -zstar, sprintf('t* (FDR) = %.3f', zstar), 'color', 'blue')