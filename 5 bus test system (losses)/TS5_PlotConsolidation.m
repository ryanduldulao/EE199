% EE 199 - Duldulao and Palicos
% Loss - Plot Consolidation

clear; close all; clc;

%Load all previously saved .mat files of the same case for each bus
load incgen_2.mat;
load incgen_3.mat;
load incgen_4.mat;
load incgen_5.mat;

%Settin the x value to reflect the delta generation from 130 MW to the
%maximum capacity of all generators     
x = incgen_2(:,2);

%Change the source of the data for the y values to the 4th column which is
%delta loss and it must be from the .mat files loaded above. Change markers
%as needed depending on the data.
figure
plot(x, incgen_2(:,4), '-o', 'MarkerIndices', [47 98], 'MarkerFaceColor', 'red', 'MarkerSize', 8);
hold on
plot(x, incgen_3(:,4), '-o', 'MarkerIndices', [47 98], 'MarkerFaceColor', 'red', 'MarkerSize', 8);
plot(x, incgen_4(:,4), '-o', 'MarkerIndices', [47 98], 'MarkerFaceColor', 'red', 'MarkerSize', 8);
plot(x, incgen_5(:,4), '-o', 'MarkerIndices', [47 98], 'MarkerFaceColor', 'red', 'MarkerSize', 8);

%Change title and labels as needed according to the case being presented.
title('DeltaLoad vs. DeltaLoss (Modified Generation - Consolidated)')
xlabel('Delta Load (MW)')
ylabel('Delta Loss (MW)')
grid on
xline(46, '-b', 'Gen 3 Max Cap @ x = 46');
xline(97, '-m', 'Gen 2 Max Cap @ x = 97');

legend('Bus 2', 'Bus 3', 'Bus 4', 'Bus 5', 'Location', 'southeast');