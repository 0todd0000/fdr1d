

%addpath
addpath('C:\Users\s5001683\Documents\MATLAB\spm1d');
addpath('C:\Users\s5001683\Documents\MATLAB\spm1d\spm8');

%(0) Load dataset:
dataset    = spm1d.data.uv1d.t1.Random();
[Y,mu]     = deal( dataset.Y, dataset.mu );



%(1) Conduct SPM analysis:
alpha         = 0.05;
two_tailed    = false;
spm           = spm1d.stats.ttest(Y - mu);
spmi          = spm.inference(0.05, 'two_tailed',two_tailed);



%(2) Conduct FDR inference:

%%% calculate then sort uncorrected p values:
z             = abs( spm.z );
df            = spm.df(2);
p             = 1 - spm_Tcdf(z,df);
[psorted,ind] = sort(p);
zsorted       = z(ind);

%%% compute p threshold:
Q             = numel(z);
if two_tailed
    alpha     = alpha / 2; %#ok<UNRCH>
end
pth           = alpha/Q * (1:Q);

%%% compute test statistic threshold
i             = psorted < pth;
if any(i)
    istar     = find(i, 1, 'last');
    zstar     = zsorted(istar);
else
    zstar     = nan;
end






%(3) Plot:
close all
spmi.plot();
spmi.plot_threshold_label();
spmi.plot_p_values();


line( xlim, [zstar zstar], 'color', 'blue', 'linestyle', '--');
text( mean(xlim), zstar, sprintf('t* (FDR) = %.3f', zstar), 'color', 'blue')

