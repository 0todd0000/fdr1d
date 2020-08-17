classdef SPMfdr < matlab.mixin.CustomDisplay
    properties
        STAT        %test statistic ("T", "F", "X2" or "T2")
        Q           %number of field nodes
        dim = 1;    %data dimensionality
        z           %test statistic continuum
        nNodes      %number of field nodes
        df          %degrees of freedom
        fwhm        %field smoothness (full width at half maximum)
        resels      %"resolution element" counts (equivalent to: [1 (nNodes-1)/fwhm] if the field is continuous across all nodes)
        sigma2      %field variance
        r           %correlation coefficient (regression only)
        isregress   %boolean flag:  true if regression analysis
        beta        %fitted model parameters (usually means or slopes)
        R           %fitted model residuals
        residuals   %fitted model residuals (same as R;  R also retained for legacy purposes)
        isparametric = true;
    end
    
    methods
        
        function [spmi] = fdr_inference(self, alpha, varargin)
            %parse inputs
            default2tailed = isequal(self.STAT,'T');
            parser         = inputParser;
            addOptional(parser, 'two_tailed', default2tailed, @islogical);
            addOptional(parser, 'withBonf', true, @islogical);
            addOptional(parser, 'interp', true, @islogical);
            addOptional(parser, 'circular', false, @(x)islogical(x) && isscalar(x) );
            parser.parse(varargin{:});
            two_tailed     = parser.Results.two_tailed;
            withBonf       = parser.Results.withBonf;
            interp         = parser.Results.interp;
            circular       = parser.Results.circular;
            %check: two-tailed and test statistic
            if two_tailed && ~isequal(self.STAT, 'T')
                error('Two-tailed inference can only be used for t tests and regression.')
            end
            check_neg      = two_tailed;
            %check: two-tailed and ROI
            if ~isempty(self.roi) && isnumeric(self.roi)
                if two_tailed
                    error('Two-tailed inference can only be used with logical ROIs. Use true and false to define the ROI rather than -1, 0 and +1')
                else
                    check_neg = any(self.roi==-1);
                end
            end
            %correct for two-tailed inference
            if two_tailed
                pstar = 0.5 * alpha;
            else
                pstar = alpha;
            end
            % zstar        = self.get_critical_threshold(pstar, withBonf); % <- old
            zstar        = inference_manual(self.z, self.df(2), alpha, self.STAT, two_tailed);%<- ADD FDR INFERENCE HERE
            clusters     = self.get_clusters(zstar, check_neg, interp, circular);  % supra-threshold clusters
            [clusters,p] = self.cluster_inference(clusters, two_tailed, withBonf);
            p_set        = self.set_inference(zstar, clusters, two_tailed, withBonf);
            if self.STAT=='F'
                spmi     = spm1d.stats.spm.SPMi_F(self, alpha, zstar, p_set, p, two_tailed, clusters);
            else
                spmi     = spm1d.stats.spm.SPMi(self, alpha, zstar, p_set, p, two_tailed, clusters);
            end
        end
    end

    methods (Access=private)
        
        function [clusters] = get_clusters(self, zstar, check_neg, interp, circular)
            clusters = spm1d.geom.cluster_geom(self.z, zstar, interp, circular, 'csign',+1);
            if check_neg
                clustersn = spm1d.geom.cluster_geom(-self.z, zstar, interp, circular, 'csign',-1);
                clusters  = [clusters clustersn];
            end
        end 
        
        
       function [clusters,p] = cluster_inference(self, clusters, two_tailed, withBonf)
            n = numel(clusters);
            if n==0
                p = [];
            else
                p = zeros(1,n);
                for i = 1:n
                    clusters{i} = clusters{i}.inference(self.STAT, self.df, self.fwhm, self.resels, two_tailed, withBonf, self.nNodes);
                    p(i) = clusters{i}.P;
                end
                %re-order clusters left-to-right:
                x = zeros(1,n);
                for i = 1:n
                    if iscell(clusters{i}.xy)
                        x(i) = clusters{i}.xy{1}(1);
                    else
                        x(i) = clusters{i}.xy(1);
                    end
                end
                [~,ind] = sort(x);
                [clusters,p] = deal( clusters(ind), p(ind) );
            end
       end
       
       
       function [P] = set_inference(self, zstar, clusters, two_tailed, withBonf)
            [v,res,n] = deal(self.df, self.resels, self.nNodes);
            c = numel(clusters);
            k = inf;
            for i = 1:c
                k = min(k, clusters{i}.extentR);
            end
            switch self.STAT
                case 'T'
                    P = spm1d.rft1d.t.p_set_resels(c, k, zstar, v(2), res, 'withBonf',withBonf, 'nNodes',n);
                    if two_tailed
                        P = min(1, 2*P);
                    end
                case 'X2'
                    P= spm1d.rft1d.chi2.p_set_resels(c, k, zstar, v(2), res, 'withBonf',withBonf, 'nNodes',n);
                case 'F'
                    P = spm1d.rft1d.f.p_set_resels(c, k, zstar, v, res, 'withBonf',withBonf, 'nNodes',n);
                case 'T2'
                    P = spm1d.rft1d.T2.p_set_resels(c, k, zstar, v, res, 'withBonf',withBonf, 'nNodes',n);
            end
       end
    end
end