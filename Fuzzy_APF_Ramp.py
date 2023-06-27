import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def workAGC(gen, load, steps, costGen, per):
    #-----Initialize Values---------------------
    genTotal = 0
    for x in range (len(gen)):              #Record current power output
        genTotal += gen[x]
    imbalance = genTotal - load[0]          #Get imbalance between generation and demand
    index = [0]                             #Iteration number
    tGen = []                               #Generation values before change is applied
    par = []                                #Initial participation factors
    for x in range(len(gen)):
        tGen.append([gen[x]])
        par.append(per[x])
    genT = [genTotal]                       #Record of total power outputs
    balanceIndex = 0
    balance = 1000
    #-------------------------------------------
    
    for x in range(steps - 1):
        AGC.input['error'] = imbalance      #AGC takes imbalance as input
        AGC.compute()
        index.append(x+1)             
        Pdelta = AGC.output['power']        #Pdelta records total change in power output
        deltaG = []                         #deltaG records the contribution of each generator to the Pdelta total
        for y in range(len(gen)):
            deltaG.append(Pdelta*par[y])    #deltaG is a part of Pdelta based on partcipation factors

        #-----Ramp Rate limiter-------------------------------
        for y in range(len(deltaG)):        #Check if the change in output to be implemented for each
            if deltaG[y] > rampRate[y]:     #generator is less than the maximum ramp rate(bot + and -)
                deltaG[y] = rampRate[y]     #cap the change to max ramp rate if deltaG is too large
            elif deltaG[y] < rampDown[y]:
                deltaG[y] = rampDown[y]
        #-----------------------------------------------------

        #-----Adaptive Participation Factors (Ramp)-----------
        extraDelta = Pdelta
        for y in range(len(deltaG)):        #Compute for extra Pdelta 
            extraDelta -= deltaG[y]         # -> not produced due to ramp rate limits

        ADF = []                            #Check if changes in output is at ramp rate limit
        for y in range(len(deltaG)):
            if deltaG[y] == rampRate[y] or deltaG[y] == rampDown[y]:
                ADF.append(0)               #note all ramp rate limited changes using 0
            else:                         
                ADF.append(costGen[y])

        checkZero = 0
        for y in range(len(ADF)):
            if ADF[y] != 0:
                checkZero += 1
    
        if checkZero != 0:                  #Distribute extra Pdelta to generators which are
            ADF_par = computeParF(ADF)      #not ramp rate limited
            for y in range(len(deltaG)):
                deltaG[y] = deltaG[y] + (extraDelta*ADF_par[y])
        #-----------------------------------------------------

        #-----Ramp Rate limiter-------------------------------
        for y in range(len(deltaG)):        #Recheck ramp rate limits
            if deltaG[y] > rampRate[y]:
                deltaG[y] = rampRate[y]
            elif deltaG[y] < rampDown[y]:
                deltaG[y] = rampDown[y]
        #-----------------------------------------------------
        
        #-----Capacity Limiter--------------------------------
        cost = []
        for y in range(len(costGen)):
            cost.append(costGen[y])
        g = []
        for y in range(len(tGen)):
            temp = tGen[y][-1] + deltaG[y]
            g.append(temp)
        
        if Pdelta > 0:                      #Check if generators have reached their maximum
            cost = checkGenMax(g, cost)
        else:                               #or minimum capacity limits
            cost = checkGenMin(g, cost)
        #-----------------------------------------------------

        #-----Adaptive Participation Factors (Capacity)--------
        """ limit = 0
        for y in range(len(cost)):          #Recompute participation factors
            if cost[y] !=0 and limit == 0:  #Capacity limited generators have cost = 0
                par = computeParF(cost)     #and will not contribute to the next Pdelta
                limit = 1 """
        #-----------------------------------------------------

        for y in range(len(cost)):          #Record final generation values
            if cost[y] == 0:
                if Pdelta > 0 :
                    tGen[y].append(gMax[y])
                elif Pdelta < 0:
                    tGen[y].append(gMin[y])
                elif deltaG[y] == 0:
                    tGen[y].append(tGen[y][-1] + deltaG[y])
            else:
                tGen[y].append(tGen[y][-1] + deltaG[y])
        
        genTotal = 0
        for y in range(len(tGen)):          #Recompute total output generation
            genTotal += tGen[y][-1]
        genT.append(genTotal)               #Record
        imbalance = genTotal - load[x]      #Solve for next imbalance value
        if abs(imbalance) < 0.001:          #Record if balance is reached
            if index[-1] > 5 and balanceIndex == 0:
                balance = index[-1] - 5
                balanceIndex = 1

    returnArray = [tGen, index, genT, balance]
    return(returnArray)

def checkGenMax(g, cost):                   #If a generator is at max output,
    tCost = cost                            #set its cost to zero
    for x in range(len(tCost)):
        if g[x] >= gMax[x]:
            tCost[x] = 0

    return(tCost)

def checkGenMin(g, cost):                   #If a generator is at min output,
    tCost = cost                            #set its cost to zero
    for x in range(len(tCost)):
        if g[x] <= gMin[x]:
            tCost[x] = 0

    return(tCost)
    

def createLoadCurve(length, profile):       #Create array of numbers representing
    load = []                               #load demand
    val = -1
    for x in range(length):
        if x%6 == 0:
            val += 1
        load.append(profile[val])
    return(load)

def createLoadSpike(initial, final, length):
    load = []
    for x in range(length):
        if x > 3:
            load.append(final)
        else:
            load.append(initial)
    return(load)

def computeParF(cost):                      
    total = 0
    for x in range(len(cost)):              #Get total cost
        total += cost[x]
    part = []
    for x in range(len(cost)):              #Compute participation factors
        part.append(cost[x]/total)          
    return(part)

#-----Fuzzy Inference System-------------------------------------------------
error = ctrl.Antecedent(np.arange(-200, 201, 1), "error")   #Input
power = ctrl.Consequent(np.arange(-200, 201, 1), "power")   #Output

#Initialize input membership functions
error['snegative'] = fuzz.zmf(error.universe, -5, 4)
error['spositive'] = fuzz.smf(error.universe, -4, 5)
error['mnegative'] = fuzz.zmf(error.universe, -30, -10)
error['mpositive'] = fuzz.smf(error.universe, 10, 30)
error['lnegative'] = fuzz.zmf(error.universe, -100, -80)
error['lpositive'] = fuzz.smf(error.universe, 80, 100)

""" error.view()
input() """

#Initialize output membership functions
power['ns'] = fuzz.trapmf(power.universe, [ -10, -3, 0, 1])
power['ps'] = fuzz.trapmf(power.universe, [ -1, 0, 3, 10])
power['nm'] = fuzz.trapmf(power.universe, [ -60, -40, -20, -10])
power['pm'] = fuzz.trapmf(power.universe, [ 10, 20, 40, 60])
power['nl'] = fuzz.trapmf(power.universe, [ -110, -100, -60, -50])
power['pl'] = fuzz.trapmf(power.universe, [ 50, 60, 100, 110])

""" power.view()
input() """

#Initialize rule base
rule1 = ctrl.Rule(error['snegative'], power['ps'])
rule2 = ctrl.Rule(error['spositive'], power['ns'])
rule3 = ctrl.Rule(error['mnegative'], power['pm'])
rule4 = ctrl.Rule(error['mpositive'], power['nm'])
rule5 = ctrl.Rule(error['lnegative'], power['pl'])
rule6 = ctrl.Rule(error['lpositive'], power['nl'])

AGC_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
AGC = ctrl.ControlSystemSimulation(AGC_ctrl)
#----------------------------------------------------------------------------

#-----Set System Parameters----------------------------------
loadArray = [130, 160, 140, 140, 170, 170]       #Create demand profile
loadCurve = createLoadCurve(31,loadArray)
""" loadCurve = createLoadSpike(loadArray[0], loadArray[1], 35) """

costGen = [1/.022, 1/0.018, 1/.016]         #1/(incremental cost of generator)
per = computeParF(costGen)

gen = [22.454, 36.641, 72.471]              #Initial generator output powers

gMax = [85, 70, 80]                         #Maximum power output

gMin = [10, 10, 10]                         #Minimum power output

rampRate = [10, 5, 1]                       #Maximum + ramp rate (MW/interval)
                                            #   1 interval = 10 seconds
rampDown = [-5, -2.5, -.5]                  #Minimum - ramp rate (MW/interval)
#------------------------------------------------------------

genAGC = workAGC(gen, loadCurve, 31, costGen, per)  #Call function and record results



print(str(genAGC[3] * 10) + " seconds")     #Print time when balance is reached

figure, axis = plt.subplots(3, sharex=True) #Create plot with 3 subplots

axis[0].plot(genAGC[1], loadCurve)          #First plot is the load curve (demand)

axis[1].plot(genAGC[1], genAGC[2])          #Second plot is the total generator output

for x in range(len(genAGC[0])):             #Third plot is the individual power outputs of
    name = "Gen " + str(x +1)
    axis[2].plot(genAGC[1], genAGC[0][x], label = name)   # the generators
    print(name + ": " + str(genAGC[0][x][-1]))
axis[2].legend()

axis[0].set(ylabel = "Load Demand")         #Set plot labels
axis[1].set(ylabel = "Generation")
axis[2].set(ylabel = "Generator Values")
axis[0].grid(axis='both')
axis[1].grid(axis='both')
axis[2].grid(axis='both')
plt.xlabel("Interval")
plt.xticks(np.arange(0, 31, 6.0))
plt.show()
