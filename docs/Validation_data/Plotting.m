clear all
close all
clc

load Averaged_Normalized_results.mat Avg_Norm_G3K3
load Averaged_Normalized_results.mat Avg_Norm_Gur
load Variance_Normalized_results.mat Var_Norm_G3K3
load Variance_Normalized_results.mat Var_Norm_Gur


% Number of plots to generate
numPlots = size(Avg_Norm_G3K3, 1); % 4 in your case
conditionLabels = {11, 13, 15, 17, 19};
titles={'Average Gap for case N1 with standard deviation','Average Gap for case N2 with standard deviation','Average Gap for case N3 with standard deviation','Average Gap for case N4 with standard deviation'};
% Preparing to plot
figure(1);
for i = 1:2
    subplot(2, 1, i); % Change to subplot(2, 2, i) if you prefer a 2x2 layout
    errorbar(Avg_Norm_Gur(i, :), sqrt(Var_Norm_Gur(i, :)), 'LineWidth', 1);
    hold on
    errorbar(Avg_Norm_G3K3(i, :), sqrt(Var_Norm_G3K3(i, :)), 'LineWidth', 1);

    xticks(1:length(conditionLabels)); % Ensure there's a tick for each label
    xticklabels(conditionLabels); % Assign the custom labels
   
    grid on
    
    % Optional: Add labels/titles if necessary
    xlabel('Number of patients');
    ylabel('Gap');
    title(titles(i));
end
figure(2);
for i = 3:numPlots
    subplot(2, 1, i-2); % Change to subplot(2, 2, i) if you prefer a 2x2 layout
    errorbar(Avg_Norm_Gur(i, :), sqrt(Var_Norm_Gur(i, :)), 'LineWidth', 1);
    hold on
    errorbar(Avg_Norm_G3K3(i, :), sqrt(Var_Norm_G3K3(i, :)), 'LineWidth', 1);

    xticks(1:length(conditionLabels)); % Ensure there's a tick for each label
    xticklabels(conditionLabels); % Assign the custom labels
    
    grid on
    
    % Optional: Add labels/titles if necessary
    xlabel('Number of patients');
    ylabel('Gap');
    title(titles(i));
end
figure(1);
f1=figure(1);
f1.Position = [100 100 700 450]
subplot(2, 1, 1);
legend('Gurobi','SNKSA','Location','northwest')
xlim([0.8, length(conditionLabels)+0.2]); % Adds whitespace by extending limits
ylim([-0.01 0.055]); % Adds whitespace by extending limits
figure(1);
subplot(2, 1, 2);
legend('Gurobi','SNKSA','Location','northwest')
xlim([0.8, length(conditionLabels)+0.2]); % Adds whitespace by extending limits
ylim([-0.01 0.04]); % Adds whitespace by extending limits
figure(2);
f2=figure(2);
f2.Position = [100 100 700 450]
subplot(2, 1, 1);
legend('Gurobi','SNKSA','Location','northwest')
xlim([0.8, length(conditionLabels)+0.2]); % Adds whitespace by extending limits
ylim([-0.01 0.045]); % Adds whitespace by extending limits
figure(2);
subplot(2, 1, 2);
legend('Gurobi','SNKSA','Location','northwest')
xlim([0.8, length(conditionLabels)+0.2]); % Adds whitespace by extending limits
ylim([-0.01 0.08]); % Adds whitespace by extending limits




    
