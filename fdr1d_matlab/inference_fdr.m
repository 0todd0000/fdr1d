function zstar = inference_fdr(spm, alpha, varargin)


switch class(spm)
    case 'spm1d.stats.spm.SPM'
        if nargin == 3
            two_tailed = varargin{1};
        else
            two_tailed = true;
        end
        zstar = inference_manual(spm.z, spm.df(2), alpha, 'T', two_tailed);

    case 'spm1d.stats.spm.SPM_X2'
        zstar = inference_manual(spm.z, spm.df(2), alpha, 'X2', false);
    
    case 'spm1d.stats.spm.SPM_F'
        zstar = inference_manual(spm.z, spm.df, alpha, 'F', false);
        
    case 'spm1d.stats.spm.SPMFList'
        n     = spm.nEffects;
        zstar = zeros(1, n);
        for i = 1:n
            zstar(i) = inference_fdr(spm(i), alpha);
        end
    otherwise
        error('Input "spm" must be an SPM, SPM_X2, SPM_F or SPMFList object')
end



% try
%     if spm.STAT == 'T' || strcmp(spm.STAT, 'X2') == 1
%         stat = spm.STAT;
%         df   = spm.df(2);
%     else
%         stat = spm.STAT;
%         df   = spm.df;
%     end
% catch
%     stat = spm.SPMs{1}.STAT;
%     df   = spm.SPMs{1}.df;
% end
% 
% zstar = inference_manual(spm.z, df, alpha, stat, two_tailed);