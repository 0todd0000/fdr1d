function [zstar] = inference_manual(z, df, alpha, stat, two_tailed)
% def inference_manual(z, df, alpha=0.05, two_tailed=True, stat='T'):
% Compute the critical test statistic value using false discovery rate (FDR)-based inference.
% -INPUTS-
% z       : test statistic (one-dimensional numpy arrray)
% df      : degrees of freedom (scalar for the T statistic, two-tuple for the F statistic)
% alpha   : Type I error rate (scalar between 0 and 1)
% stat    : type of test statistic ("T" or "F")
% two_tld : two-tailed (True) or one-tailed (False) inference
%
% -OUTPUTS-
% zstar   : critical test statistic value [None is returned if the test fails to reach significance]
%
% -EXAMPLE-
% J     = 12   #sample size (number of 1D continua)
% Q     = 101  #number of continuum nodes
% y     = np.random.randn(J, Q)   #random sample of 1D continua
% t     = y.mean(axis=0) / (  y.std(ddof=1, axis=0)/ (J**0.5)  )  #1D t statistic
% tstar = fdr_inference(t, J-1, alpha=0.05, stat='T')
% print('Critical FDR threshold: %s'%tstar)
	
z         = abs(z);

%%% compute uncorrected p values:
if stat == 'T'
    p     = 1 - spm_Tcdf(z, df);
elseif stat == 'F'
    p     = 1 - spm_Fcdf(z, df);
elseif stat == 'T2'
    p     = 1 - spm_Tcdf(z, df);
elseif stat == 'X2'
    p     = spm_Xcdf(z, df);
else
    disp('"stat" must be one of: "T", "F", "T2", "X2"')
end

if stat ~= 'T' && two_tailed == 1
    str = sprintf('The input variable "two_tailed" must be ''False'' when the test statistic is %s', stat);
    disp(str);
    zstar     = nan;
else
    %%% sort p values:
    [psorted,ind] = sort(p);
    zsorted       = z(ind);

    %%% compute sorted p value threshold:
    Q             = numel(z);
    if two_tailed
        alpha     = alpha / 2; %ok<UNRCH>
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
    
end

