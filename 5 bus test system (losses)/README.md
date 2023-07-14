# EE 199 - 5 bus test system for losses

### 5 bus test system

![5bustestsystem](https://github.com/ryanduldulao/EE199/blob/main/5%20bus%20test%20system%20(losses)/5%20bus%20test%20system.png)

* **FEATURES**
  1. Used to simulate a 5 bus transmission test system.
  2. Losses are the primary concern in this project and the code is optimized for the different cases explored.
 
* **CASE STUDIES EXPLORED**
  1. Base case
  2. Increased generator limits case
  3. Modified generator locations case

### Files Included
* **MATLAB SCRIPTS**
  1. busout.m
  2. dispatch.m
  3. lfnewton.m
  4. lfybus.me
  5. lineflow.m

These MATLAB scripts were developed by Saadat in order to test transmission systems given their bus data, line data etc. Please make sure to always have these files in your folder while using the main case study files. DO NOT edit these files.

* **CASE STUDY SCRIPTS**
  1. TS5_base.m
  2. TS5_incgen.m
  3. TS5_modgen.m
  4. TS5_PlotConsolidation.m
 
These are the main case study files that will be tweaked to execute the study. Files 1 to 3 are the case study files while the 4th one is a script to consolidate the data from the different buses per case study. Each file also has instructions on how to use it.

### Instructions
Simply download all the files into a single folder. Open in MATLAB. Set the path to the current folder in order to run the code. Files were made using MATLAB R2021a.
