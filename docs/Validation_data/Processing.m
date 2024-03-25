clear all
close all
clc

load Results.mat

%% Normalization

Norm_Gur=(Gur-Bou)./Bou;
Norm_Gre=(Gre-Bou)./Bou;
Norm_Gsl=(Gsl-Bou)./Bou;
Norm_Sli=(Sli-Bou)./Bou;
Norm_Swa=(Swa-Bou)./Bou;
Norm_G2K2=(G2K2-Bou)./Bou;
Norm_G4K2=(G4K2-Bou)./Bou;
Norm_G3K3=(G3K3-Bou)./Bou;

%% Averaging over test 

for c=1:1:4
    for N=1:1:5
        Avg_Norm_Gur(c,N)=mean(Norm_Gur(c,N,:));
        Avg_Norm_Gre(c,N)=mean(Norm_Gre(c,N,:));
        Avg_Norm_Gsl(c,N)=mean(Norm_Gsl(c,N,:));
        Avg_Norm_Sli(c,N)=mean(Norm_Sli(c,N,:));
        Avg_Norm_Swa(c,N)=mean(Norm_Swa(c,N,:));
        Avg_Norm_G2K2(c,N)=mean(Norm_G2K2(c,N,:));
        Avg_Norm_G4K2(c,N)=mean(Norm_G4K2(c,N,:));
        Avg_Norm_G3K3(c,N)=mean(Norm_G3K3(c,N,:));
        Var_Norm_Gur(c,N)=var(Norm_Gur(c,N,:));
        Var_Norm_Gre(c,N)=var(Norm_Gre(c,N,:));
        Var_Norm_Gsl(c,N)=var(Norm_Gsl(c,N,:));
        Var_Norm_Sli(c,N)=var(Norm_Sli(c,N,:));
        Var_Norm_Swa(c,N)=var(Norm_Swa(c,N,:));
        Var_Norm_G2K2(c,N)=var(Norm_G2K2(c,N,:));
        Var_Norm_G4K2(c,N)=var(Norm_G4K2(c,N,:));
        Var_Norm_G3K3(c,N)=var(Norm_G3K3(c,N,:));
    end
end











