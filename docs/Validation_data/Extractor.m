clear all
close all
clc

% Gur=zeros(4,5,20);
% Bou=zeros(4,5,20);
% Gre=zeros(4,5,20);
% Swa=zeros(4,5,20);
% Sli=zeros(4,5,20);
% Gsl=zeros(4,5,20);
% G2K2=zeros(4,5,20);
% G4K2=zeros(4,5,20);
G3K3=zeros(4,5,20);


% Define the file path
filePath = 'G3K3.txt';

% Open the file for reading
fileID = fopen(filePath, 'r');

% Check if the file was opened successfully
if fileID == -1
    error('Failed to open the file.');
end


% Read the file line by line
while ~feof(fileID)
    line = fgetl(fileID);
    % Parse the current line
    parsed = sscanf(line, '%d - %d - %d : %f ');
    
    if length(parsed) == 4
        G3K3(parsed(1)+1,(parsed(2)-9)/2,parsed(3))=parsed(4);
    else
        warning('Invalid line format: %s', line);
    end
end

% Close the file
fclose(fileID);
























