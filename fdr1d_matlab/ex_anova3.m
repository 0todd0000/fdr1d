    

clear;  clc



%(0) Load data:
dataset    = spm1d.data.uv1d.anova3.SPM1D_ANOVA3_2x2x2();
% dataset    = spm1d.data.uv1d.anova3.SPM1D_ANOVA3_2x3x4();
[Y,A,B,C]  = deal(dataset.Y, dataset.A, dataset.B, dataset.C);


%(1) Conduct SPM analysis:
alpha      = 0.05;
two_tailed = false;
spmlist    = spm1d.stats.anova3(Y, A, B, C);
spmilist   = spmlist.inference(0.05);
fstar      = inference_fdr(spmlist, alpha, two_tailed);
disp_summ(spmilist)


%(2) Plot:
close all
spmilist.plot('plot_threshold_label',false, 'plot_p_values',true, 'autoset_ylim',true);

