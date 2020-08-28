function zstar = inference_fdr(spm, alpha, two_tailed)

try
    if spm.STAT == 'T' || strcmp(spm.STAT, 'X2') == 1
        stat = spm.STAT;
        df   = spm.df(2);
    else
        stat = spm.STAT;
        df   = spm.df;
    end
catch
    stat = spm.SPMs{1}.STAT;
    df   = spm.SPMs{1}.df;
end

zstar = inference_manual(spm.z, df, alpha, stat, two_tailed);