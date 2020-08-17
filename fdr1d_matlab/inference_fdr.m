function zstar = inference_fdr(spm, alpha, two_tailed)

if spm.STAT == 'T' || strcmp(spm.STAT, 'X2') == 1 
    df  = spm.df(2);
else
    df  = spm.df;
end
zstar = inference_manual(spm.z, df, alpha, spm.STAT, two_tailed);