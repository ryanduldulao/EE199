% EE 199 - Duldulao and Palicos
% Loss - Increased Generation Limits

clear; close all; clc;

%Bus Data, Line Data, Cost function, and capacity limits initialization. 
basemva = 100;  accuracy = 0.001; accel = 1.7; maxiter = 200;

%        Bus Bus  Voltage Angle   ---Load---- -------Generator----- Static Mvar
%        No  code Mag.    Degree  MW    Mvar  MW  Mvar Qmin Qmax    +Qc/-Ql
busdata=[1   1    1.06    0.0     0.0   0.0    0.0   0.0  10  50       0
         2   2    1.045   0.0    20.0  10.0   40.0  30.0  10  50       0
         3   2    1.03    0.0    20.0  15.0   30.0  10.0  10  40       0
         4   0    1.00    0.0    40.0  30.0    0.0   0.0   0   0       0
         5   0    1.00    0.0    50.0  40.0    0.0   0.0   0   0       0];
     
%                                        Line code
%         Bus bus   R      X     1/2 B   = 1 for lines
%         nl  nr  p.u.   p.u.   p.u.     > 1 or < 1 tr. tap at bus nl
linedata=[1   2   0.02   0.06   0.030    1
          1   3   0.08   0.24   0.025    1
          2   3   0.06   0.18   0.020    1
          2   4   0.06   0.18   0.020    1
          2   5   0.04   0.12   0.015    1
          3   4   0.01   0.03   0.010    1
          4   5   0.08   0.24   0.025    1];

  cost = [200 7.0 0.011   
          180 6.8 0.009   
          140 6.3 0.008]; 
 
 %Increased generation maximum limits compared to the base case. Base
 %values are commented to the side.
 mwlimits = [10 95      %10 85
             10 80      %10 90
             10 90];    %10 70 

%Execution of base data for the system using the base newton raphson. Slack
%bus still provides most of the power. Generation is not yet distributed.
lfybus                    
lfnewton
busout
lineflow
dispatch

%Initialization of main container for needed data. This will be saved in a
%.mat file later. Don't forget to change the accompanying number to the 
%bus number being tested.
incgen_2 = zeros(136,8);

%Individual containers for data which will be forwarded to the main
%container later.
TotalDemand = zeros(136,1);
DeltaLoad = zeros(136,1);
TotalLoss = zeros(136,1);
DeltaLoss = zeros(136,1);
Gen1values = zeros(136,1);
Gen2values = zeros(136,1);
Gen3values = zeros(136,1);
TotalGeneration = zeros(136,1);

%Counter for loop
counter = 1;

%Counter limit is also increased by the total amount added to the maximum 
%limits.
while counter < 137
%This will distribute the demand to the generators based on the dispatch
%calculated earlier and will continue to do so until the loop finishes.
lfnewton     
busout       
dispatch
lfnewton
lineflow

%Recording of Total Demand, Delta Load from 130 MW, and Total Generation of
%the system
TotalDemand(counter) = Pdt;
DeltaLoad(counter) = counter - 1;
TotalGeneration(counter) = Pgt;

%Recording of Loss and Delta Loss. Delta Loss was is obtained by
%subtracting the first value of loss with after the dispatch distributed
%the load on the generators.
TotalLoss(counter) = real(SLT);
DeltaLoss(counter) = real(SLT) - 1.60356350615089;

%Recording of generation values
Gen1values(counter) = busdata(1,7);
Gen2values(counter) = busdata(2,7);
Gen3values(counter) = busdata(3,7);

%Increment of 1 MW to the load P (MW) of bus of interest. 
%In this case it is set to Bus 2. Changing the row value (n , 5) from 2-5 
%will access the bus that we are incrementing the load. DON'T  forget to 
%change the row value to the corresponding bus you are testing.
busdata(2,5) = busdata(2,5) + 1;

%Saving the values of the individual containers into a single big container
incgen_2(counter, 1) = TotalDemand(counter);
incgen_2(counter, 2) = DeltaLoad(counter);
incgen_2(counter, 3) = TotalLoss(counter);
incgen_2(counter, 4) = DeltaLoss(counter);
incgen_2(counter, 5) = Gen1values(counter);
incgen_2(counter, 6) = Gen2values(counter);
incgen_2(counter, 7) = Gen3values(counter);
incgen_2(counter, 8) = TotalGeneration(counter);

%counter increment
counter = counter + 1;
end

%Saving the big container into a .mat file for plotting the consolidated
%result. DON'T forget to change the accompanying number to the bus number 
%being tested.
save incgen_2.mat incgen_2

%Optional figure position upon display
%set(0,'defaultfigureposition',[550 250 800 600])

%Plot of the individual bus result. %Change to the current bus number as
%needed as well as the markers based on the gathered data.
figure
plot(DeltaLoad, DeltaLoss, '-o', 'MarkerIndices', [47 98], 'MarkerFaceColor', 'red', 'MarkerSize', 8);
title('DeltaLoad vs. DeltaLoss (Increase Gen Limits - Bus 2)')
xlabel('Delta Load (MW)')
ylabel('Delta Loss (MW)')
grid on
xline(46, '-b', 'Gen 3 Max Cap @ x = 46');
xline(97, '-m', 'Gen 2 Max Cap @ x = 97');



 