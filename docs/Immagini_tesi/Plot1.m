clear all
close all
clc

labels_alphab = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V','W','X','Y'};
values_alphab=[8, 8, 0.5, 8, 8, 8.8, 4, 7, 2, 8.5, 1, 0.5, 6.5, 6.5, 8.5, 1, 7.5, 5, 7, 0.5, 5, 7.5, 4, 2, 8.8];


labels_shuff={'Y', 'J', 'D', 'A', 'Q', 'S', 'M', 'U', 'W', 'I', 'K', 'T', 'C', 'L', 'P', 'X', 'G', 'R', 'N', 'H', 'V', 'B', 'E', 'O', 'F'};
values_shuff = [8.8, 8.5, 8, 8, 7.5, 7, 6.5, 5, 4, 2 , 1 , 0.5, 0.5, 0.5, 1, 2, 4, 5, 6.5, 7, 7.5, 8, 8, 8.5, 8.8]; % Corresponding values

%% 


figure(1)
stem(values_alphab, 'filled'); % Create a stem plot
set(gca, 'xtick', 1:length(labels_alphab), 'xticklabel', labels_alphab); % Set x-axis labels
xlabel('Labels'); % x-axis label
ylabel('Values'); % y-axis label
grid on
title('Discrete Function Stem Plot with Labels'); % Title
hold on


figure(2)
stem(values_shuff, 'filled'); % Create a stem plot
set(gca, 'xtick', 1:length(labels_shuff), 'xticklabel', labels_shuff); % Set x-axis labels
xlabel('Labels'); % x-axis label
ylabel('Values'); % y-axis label
grid on
title('Discrete Function Stem Plot with Labels'); % Title
hold on

%% 

figure;

% Subplot 1: Plot with alphabetically ordered labels
subplot(2, 1, 1); % Defines a 2-row, 1-column grid of subplots and activates the first element
stem(values_alphab, 'filled'); % Create a stem plot for the alphabetically ordered data
set(gca, 'xtick', 1:length(labels_alphab), 'xticklabel', labels_alphab); % Set x-axis labels
xlabel('Input labels'); % x-axis label
ylabel('Mapped value'); % y-axis label
grid on; % Turn on the grid
title('Alphabetically Ordered Labels'); % Title

% Subplot 2: Plot with shuffled labels
subplot(2, 1, 2); % Activates the second element of the 2-row, 1-column grid
stem(values_shuff, 'filled'); % Create a stem plot for the shuffled data
set(gca, 'xtick', 1:length(labels_shuff), 'xticklabel', labels_shuff); % Set x-axis labels
xlabel('Input labels'); % x-axis label
ylabel('Mapped value'); % y-axis label
grid on; % Turn on the grid
title("Seemingly Random Label's Order"); % Title

% Use 'hold on' if you're adding more plots to the same subplot
% For clarity and simplicity in this example, 'hold on' might not be necessary unless you're adding more data to each subplot



















