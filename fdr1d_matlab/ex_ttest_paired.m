

clear;  clc


%(0) Load dataset:
dataset = spm1d.data.uv1d.tpaired.PlantarArchAngle();
[YA,YB] = deal(dataset.YA, dataset.YB);


%(1) Conduct SPM analysis:
alpha      = 0.05;
two_tailed = false;
spm       = spm1d.stats.ttest_paired(YA, YB);
spmi      = spm.inference(alpha, 'two_tailed', two_tailed, 'interp',true);
% FDR analysis
zstar      = inference(spmi, alpha, two_tailed);


%(2) Plot:
close all
figure('position', [0 0 1000 300])
%%% plot mean and SD:
subplot(121)
spm1d.plot.plot_meanSD(YA, 'color','k');
hold on
spm1d.plot.plot_meanSD(YB, 'color','r');
xlabel('Time (%)')
ylabel('Plantar arch angle (°)')
title('Mean and SD')
%%% plot SPM results:
subplot(122)
spmi.plot();
spmi.plot_threshold_label();
spmi.plot_p_values();
xlabel('Time (%)')
title('Hypothesis test')

line( xlim, [zstar zstar], 'color', 'blue', 'linestyle', '--');
text( mean(xlim), zstar, sprintf('t* (FDR) = %.3f', zstar), 'color', 'blue')