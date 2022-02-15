import random
import operator

class locale(object):
    """Holds the characteristics of a state or district ("locale")
    
    All margins are assumed to be Democratic % - Republican %
    I chose this semi-arbitrarily, on the basis that Biden was leading in most polls, so using positive 
    Democratic margins would reduce the likelihood of an error caused by a missing "-"
    
    abbr is the abbreviation for the locale
    pollQuality is a subjective assessment of the quality of polls available, if any
    polls is the current average margin in the available polls MINUS the average national polling margin
    prior is the margin in 2016
    evs is the value in electoral votes
    demMargin is the predicted margin of victory for a given simulation
    demWins is the percentage of simulations in which Biden won the locale
    demAvg is the average margin of victory acrosss all simulations for a locale
    tip is the likelihood that the locale would be the tipping point in the Electoral College
    sm is the likelihood that the state would have the smallest margin of victory (districts excluded)
    
    actual_dem_margin was added in 2022 when this code was uploaded and represents the actual margin of victory
    """
    
    def __init__(self, abbr, pollQuality, polls, prior, evs, demMargin, demWins, demAvg, tip, sm):
        self.abbr = abbr
        self.pollQuality = pollQuality
        self.polls = polls
        self.prior = prior
        self.evs = evs
        self.demMargin = demMargin
        self.demWins = demWins
        self.demAvg = demAvg
        self.tip = tip
        self.sm = sm
        
        # Added in 2022
        self.actual_dem_margin = 0
        
        
# The locales are separated into those for which polling data is available and those without it

# "polledEVs" are the electoral votes for each state; polledPriors were the margins of victory in 2016

polledAbbrs = ["NV","AZ","TX","IA","MN","WI","MI","OH","GA","FL","NC","VA","PA","NH","NM","SC","ME"]
polledEVs = [6,11,38,6,10,10,16,18,16,29,15,13,20,4,5,9,2]
polledPriors = [2.42,-3.55,-8.99,-9.41,1.52,-0.77,-0.23,-8.13,-5.13,-1.2,-3.66,5.32,-0.72,0.37,8.21,-14.27,2.96]


# These are the polling margins for the states which have polling data available, taken from RealClearPolitics. 
# Note that they are relative to the national polling margin, not absolute

# Also note that these were last updated sometime in the early fall of 2020, a month or two prior to the
# election; thus, they represent my prediction of the results as of that time

polledPolls = [
    # Nevada:
    2.3,
    # Arizona:
    -4.8,
    # Texas:
    -10.2,
    # Iowa:
    -8.6,
    # Minnesota:
    -1.2,
    # Wisconsin:
    -1.7,
    # Michigan:
    -0.5,
    # Ohio:
    -6.3,
    # Georgia:
    -9.6,
    # Florida:
    -3.1,
    # North Carolina:
    -7,
    # Virginia:
    4.9,
    # Pennsylvania:
    -0.4,
    # New Hampshire:
    1.8,
    # New Mexico:
    4.1,
    # South Carolina:
    -13.1,
    # Maine:
    3.2]


# These are subjective assessments of the quality and quantity of the polls in each state

polledPollsQuality = [
    # Nevada:
    "Low",
    # Arizona:
    "High",
    # Texas:
    "High",
    # Iowa:
    "High",
    # Minnesota:
    "High",
    # Wisconsin:
    "High",
    # Michigan:
    "High",
    # Ohio:
    "High",
    # Georgia:
    "High",
    # Florida:
    "High",
    # North Carolina:
    "High",
    # Virginia:
    "High",
    # Pennsylvania:
    "High",
    # New Hampshire:
    "High",
    # New Mexico:
    "Low",
    # South Carolina:
    "Low",
    # Maine:
    "High"]


# "trailingDemMargin" is the average margin in recent national polls, taken from RealClearPolitics. As with the
# state polling data, this was last updated several months before the election

# "natMarginEDSTD" is the expected standard deviation of the difference between the national polling
# average at the point in time in which the simulation was run and the actual national polling margin on 
# Election Day. It was estimated from past recent presidential elections and is semi-subjective

# "stateMarginEDModifierSTD" is the expected standard deviation of the difference between the current polls
# for a locale and the polls on Election Day, after accounting for the change in the national average. Like 
# "natMarginEDSTD" it was estimated from past elections and is semi-subjective

trailingDemMargin = 6.33
natMarginEDSTD = 2.5
stateMarginEDModifierSTD = 4

nonPolledAbbrs = ["NE2","ME2","CO","OR","DE","AK","MS","UT","MO","IN","CT","NJ","ME1","RI","WA","IL","NY","VT",
                  "MD","MA","CA","HI","LA","MT","KS","NE1","TN","AR","AL","SD","KY","ID","ND","OK","WV","WY",
                  "NE3","DC","NE"]
nonPolledPriors = [-2.24,-10.29,4.91,10.98,11.37,-14.73,-17.83,-18.08,-18.64,-19.17,13.64,14.1,14.81,15.51,15.71,
                   17.06,22.49,26.41,26.42,27.2,30.11,32.18,-19.64,-20.42,-20.6,-20.72,-26.01,-26.92,-27.73,
                   -29.79,-29.84,-31.77,-35.73,-37.08,-42.07,-46.3,-54.19,86.78,0]
nonPolledEVs = [1,1,9,7,3,3,6,6,10,11,7,14,1,4,12,20,29,3,10,11,55,4,8,3,6,1,11,6,9,3,8,4,3,7,5,3,1,3,2]

allStates = []


# Initializing the locales and adding them to the working list allStates

for x in range(len(polledAbbrs)):
    allStates.append(locale(polledAbbrs[x],polledPollsQuality[x],polledPolls[x],polledPriors[x],polledEVs[x],
                            0,0,0,0,0))
for x in range(len(nonPolledAbbrs)):
    allStates.append(locale(nonPolledAbbrs[x],"None",0,nonPolledPriors[x],nonPolledEVs[x],0,0,0,0,0))

    
# These are the average number of Democratic and Republican electoral votes across all the simulations

avgDemEVs = 0
avgGOPEVs = 0


# This is the percentage of simulations won by Biden, Trump, or tied

demWins = 0
GOPWins = 0
ties = 0


# This tracks the likelihood that the Electoral College margin of victory will fall into a given bin. The bins 
# are taken from a PredictIt market

outcomes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


# This tracks the likelihood that the popular vote winner will lose the Electoral College

PVWinnerLoses = 0


# This code runs 100,000 simulations of Election Day. I chose not to parameterize the number of simulations,
# although in retrospect it would probably have saved time during testing

for y in range(100000):
    
    # "natMarginED" represents a randomly generated polling margin on Election Day
    
    # "avgPolledPollError" represents a randomly generated average error in the state polls. 3.17 is the standard
    # devation of the value from recent previous elections. Positive values represent Biden being underestimated,
    # negative values represent Biden being overestimated
    
    # "avgNationalPollError" represents a randomly generated average margin of error in the national polls, also
    # estimated using values from previous elections
    
    natMarginED = trailingDemMargin + random.gauss(0, natMarginEDSTD)
    avgPolledPollError = random.gauss(0,3.17)
    avgNationalPollError = avgPolledPollError + random.gauss(0,2.22)
    
    
    # demEVs and GOPEVs are the number of electoral votes obtained by each party in this iteration of the
    # simulation
    
    demEVs = 0
    GOPEVs = 0
    
    
    # Maine and Nebraska had to be treated separately from the others due to their unique methods of allocating 
    # electoral votes
    # "maineMargin" is the simulated margin of victory in Maine across the entire state and will be used to
    # calculate the margins of victory in its two congressional districts later in the program
    
    maineMargin = 0
    
    
    # Resetting the margins in each state for the simulation
    
    for x in range(len(allStates)):
        allStates[x].demMargin = 0
        
        
    for x in range(len(allStates)):
        
        # Locales are divided into those with high poll quality, those with low quality, and those with none
        
        if allStates[x].pollQuality == "High":
            
            # "stateMarginEDModifier" is the difference between the expected polling margin on Election Day
            # and the actual polling margin on Election Day in this locale for this simulation
            
            stateMarginEDModifier = random.gauss(0,stateMarginEDModifierSTD)
            
            
            # "stateMarginED" is the actual polling margin on Election Day in this locale for this simulation
            
            stateMarginED = natMarginED + allStates[x].polls + stateMarginEDModifier
            
            
            # "demMargin" is the actual simulated margin in the locale. It is calculated by applying an average
            # polling error ("avgPolledPollError") to the locale polling margin on Election Day ("stateMarginED")
            # and then a further locale-specific polling error (the random Gaussian element). The standard 
            # deviation for this locale-specific error is estimated based on previous elections
            
            demMargin = stateMarginED + avgPolledPollError * random.gauss(0,1)

            allStates[x].demMargin = demMargin
            
        elif allStates[x].pollQuality == "Low":
            stateMarginEDModifier = random.gauss(0,stateMarginEDModifierSTD)
            
            
            # The Election Day poll margin for locales with low quality polls is simulated differently than for
            # those with high quality. The margin in the locale in the 2016 election and the current polls are 
            # averaged. Note that the former is adjusted to cancel out the nationwide Democratic margin in 2016
            # by subtracting 2.1
            
            stateMarginED = natMarginED + 0.5 * allStates[x].polls + 0.5 * (allStates[x].prior - 2.1) 
            + stateMarginEDModifier
            
            demMargin = stateMarginED + avgPolledPollError * random.gauss(0,1)

            allStates[x].demMargin = demMargin
        
        elif allStates[x].pollQuality == "None" and allStates[x].abbr != "NE" and allStates[x].abbr != "ME1" \
        and allStates[x].abbr != "ME2":
            
            # Since there is no polling data for these locales, their results are simulated solely from 2016
            # results and national polls. 5.59 is the standard deviation of the change in each state's margin
            # between 2012 and 2016, after adjusting for the change in the national margin of victory. Here,
            # the simulated 2020 margin of victory is natMarginED + avgNationalPollError, so subtracting 2.1
            # (the national Democratic margin of victory in 2016) gives us the change in the margin
            
            stateMarginEDModifier = random.gauss(0,5.59)

            demMargin = allStates[x].prior - 2.1 + natMarginED + stateMarginEDModifier + avgNationalPollError

            allStates[x].demMargin = demMargin
            
            
            # The special case of Nebraska is dealt with here. The margin of victory in each congressional 
            # district is calculated above, and the MOV for the whole state is then calculated as the average of 
            # the MOV in the 3 districts. Since their populations are roughly equal, this is assumed to be an
            # acceptable approximation
            
            if allStates[x].abbr == "NE1" or allStates[x].abbr == "NE2" or allStates[x].abbr == "NE3":
                for z in allStates:
                    if z.abbr == "NE":
                        z.demMargin = z.demMargin + demMargin / 3

        if allStates[x].abbr == "ME":
            maineMargin = allStates[x].demMargin
            
            
    # "districtDiff" is the difference in margins of victory between the 1st and 2nd Maine congressional
    # districts. 19.0% was the average for 2012 and 2016; 8.7 was the standard deviation. Unfortunately, this 
    # method involves extrapolating from a very small sample size. There were likely better ways to approach it
    # but the small number of electoral votes involved and the fact that only ME2 (1 EV) was seriously contested
    # made them not worth the time

    districtDiff = random.gauss(19.0,8.7)
    ME1margin = maineMargin + districtDiff / 2
    ME2margin = 2 * maineMargin - ME1margin
    for x in allStates:
        if x.abbr == "ME1":
            x.demMargin = ME1margin
        elif x.abbr == "ME2":
            x.demMargin = ME2margin
            
            
        # Here, the Democratic margin is added to the average across all simulations and, if the locale was won
        # by Biden, the win is added to the overall Dem win percentage for that locale. Note that this involves
        # dividing by 1,000 rather than 100,000 since it is a percentage. Additionally, the electoral vote totals
        # for each party for this simulation are updated

        x.demAvg = x.demAvg + x.demMargin / 100000

        if x.demMargin > 0:
            demEVs = demEVs + x.evs
            x.demWins = x.demWins + 1 / 1000
        else:
            GOPEVs = GOPEVs + x.evs
            
            
    # The number of electoral votes for each party is added to the running average of EVs for each party across 
    # all simulations

    avgDemEVs = avgDemEVs + demEVs / 100000
    avgGOPEVs = avgGOPEVs + GOPEVs / 100000
    
    
    # The Electoral College winner has their % likelihood of winning the EC (or tying) updated

    if demEVs > GOPEVs:
        demWins = demWins + 1 / 1000
    elif GOPEVs > demEVs:
        GOPWins = GOPWins + 1 / 1000
    else:
        ties = ties + 1 / 1000
        
    
    # Each of the electorla vote total bins is updated

    if demEVs - GOPEVs < -279:
        outcomes[0] = outcomes[0] + 0.001
    elif demEVs - GOPEVs < -209:
        outcomes[1] = outcomes[1] + 0.001
    elif demEVs - GOPEVs < -149:
        outcomes[2] = outcomes[2] + 0.001
    elif demEVs - GOPEVs < -99:
        outcomes[3] = outcomes[3] + 0.001
    elif demEVs - GOPEVs < -59:
        outcomes[4] = outcomes[4] + 0.001
    elif demEVs - GOPEVs < -29:
        outcomes[5] = outcomes[5] + 0.001
    elif demEVs - GOPEVs < -9:
        outcomes[6] = outcomes[6] + 0.001
    elif demEVs - GOPEVs < 1:
        outcomes[7] = outcomes[7] + 0.001
    elif demEVs - GOPEVs < 10:
        outcomes[8] = outcomes[8] + 0.001
    elif demEVs - GOPEVs < 30:
        outcomes[9] = outcomes[9] + 0.001
    elif demEVs - GOPEVs < 60:
        outcomes[10] = outcomes[10] + 0.001
    elif demEVs - GOPEVs < 100:
        outcomes[11] = outcomes[11] + 0.001
    elif demEVs - GOPEVs < 150:
        outcomes[12] = outcomes[12] + 0.001
    elif demEVs - GOPEVs < 210:
        outcomes[13] = outcomes[13] + 0.001
    elif demEVs - GOPEVs < 280:
        outcomes[14] = outcomes[14] + 0.001
    else:
        outcomes[15] = outcomes[15] + 0.001
        
    
    # If a locale was the tipping point of the election, defined as the one which gave the winner their 270th
    # electoral vote, that locale's % odds of being the tipping point are updated

    tipCount = 0
    statesPos = 0
    allStates = sorted(allStates, key=operator.attrgetter('demMargin'))
    if demEVs > GOPEVs:
        allStates.reverse()
        while tipCount < 270:
            tipCount = tipCount + allStates[statesPos].evs
            statesPos = statesPos + 1
    elif GOPEVs > demEVs:
        while tipCount < 270:
            tipCount = tipCount + allStates[statesPos].evs
            statesPos = statesPos + 1
    allStates[statesPos - 1].tip = allStates[statesPos - 1].tip + 1 / 1000

    
    # If a state had the smallest margin (ME and NE congressional districts excluded), its % odds of having the
    # smallest margin are updated
    
    for x in allStates:
        x.demMargin = abs(x.demMargin)
    allStates = sorted(allStates, key=operator.attrgetter('demMargin'))
    smAssigned = False
    smCount = 0
    while smAssigned == False:
        if allStates[smCount].abbr in ["ME1","ME2","NE1","NE2","NE3"]:
            smCount = smCount + 1
        else:
            allStates[smCount].sm = allStates[smCount].sm + 1 / 1000
            smAssigned = True
            
    
    # If the popular vote winner lost the electoral college, the odds of this occurring are updated

    if (natMarginED + avgNationalPollError > 0 and GOPEVs > demEVs) or (natMarginED + avgNationalPollError < 0 
        and GOPEVs < demEVs):
        PVWinnerLoses = PVWinnerLoses + 1 / 1000
        

# The locales are sorted back into alphabetical order of abbreviation and their average Democratic margin of
# victory is changed to a string with a positive or negative sign, both in preparation for printing the overall
# results

allStates = sorted(allStates, key=operator.attrgetter('abbr'))

for x in allStates:
    x.demAvg = round(x.demAvg,1)
    if x.demAvg > 0:
        x.demAvg = "+" + str(x.demAvg)
    else:
        x.demAvg = str(x.demAvg)

        
# The results are printed

print("Win %:",round(demWins,1),"Democratic,",round(GOPWins,1),"Republican,",round(ties,1),"Ties")
print()
print("Average electoral votes: ", int(round(avgDemEVs,0)), "Democratic,",int(round(avgGOPEVs,0)),"Republican")
print()
print("EC winner loses PV, %:", round(PVWinnerLoses,1))
print()
print("Locale","\t","Dem win %","\t","GOP win %","\t","Avg dem margin, %","\t", "Tip %", "\t", "\t", 
      "Smallest margin %")
for x in allStates:
    print(x.abbr,"\t",int(round(x.demWins,0)),"\t","\t",int(round(100-x.demWins,0)),"\t","\t",x.demAvg,"\t","\t",
          "\t",round(x.tip,1),"\t","\t",round(x.sm,1))
print()
print("GOP win by 280+, %:", "\t", round(outcomes[0],1))
print("GOP win by 210-279, %:", "\t", round(outcomes[1],1))
print("GOP win by 150-209, %:", "\t", round(outcomes[2],1))
print("GOP win by 100-149, %:", "\t", round(outcomes[3],1))
print("GOP win by 60-99, %:", "\t", round(outcomes[4],1))
print("GOP win by 30-59, %:", "\t", round(outcomes[5],1))
print("GOP win by 10-29, %:", "\t", round(outcomes[6],1))
print("GOP win by 0-9, %:", "\t", round(outcomes[7],1))
print("Dem win by 1-9, %:", "\t", round(outcomes[8],1))
print("Dem win by 10-29, %:", "\t", round(outcomes[9],1))
print("Dem win by 30-59, %:", "\t", round(outcomes[10],1))
print("Dem win by 60-99, %:", "\t", round(outcomes[11],1))
print("Dem win by 100-149, %:", "\t", round(outcomes[12],1))
print("Dem win by 150-209, %:", "\t", round(outcomes[13],1))
print("Dem win by 210-279, %:", "\t", round(outcomes[14],1))
print("Dem win by 280+, %:", "\t", round(outcomes[15],1))


# Everything from here on was added in February 2022 to compare the model's predicitons with the actual election 
# results

from matplotlib import pyplot as plt

actual_margins = [-10.0, -25.5, -27.6, 0.3, 29.2, 13.5, 20.1, 86.8, 19.0, -3.4, 0.2, 29.5, -8.2, -30.8, 17.0, 
                  -16.1, -14.7, -25.9, -18.6, 33.5, 33.2, 9.1, 23.1, -7.4, 2.8, 7.1, -15.4, -16.6, -16.4, 1.4, 
                  -33.4, -19.1, -14.9, 6.5, -53, 7.4, 15.9, 10.8, 2.4, 23.1, -8.0, -33.1, 16.1, 1.2, 20.1, -11.7,
                  -26.2, -23.2, -5.6, -20.5, 10.1, 35.4, 19.2, 0.6, -38.9, -43.4]
for i, state in enumerate(allStates):
    state.actual_dem_margin = actual_margins[i]
        
    
    # While adding the actual election results to each state, the predicted Democratic margins are converted 
    # back from signed strings to floats
        
    if state.demAvg[0] == "-":
        state.demAvg = -float(state.demAvg[1:len(state.demAvg)])
    else:
        state.demAvg = float(state.demAvg[1:len(state.demAvg)])
    
allStates = sorted(allStates, key=operator.attrgetter('demAvg'))

print()
print()
print("------------------------")
print('{:^24s}'.format("ACTUAL RESULTS"))
print("------------------------")

# Plotting the predicted margin in each state against the actual result:

predicted_plot_points = [state.demAvg for state in allStates]
actual_plot_points = [state.actual_dem_margin for state in allStates]
num_locales = len(allStates)

plt.scatter(predicted_plot_points, range(num_locales), marker="^", label='Predicted')
plt.scatter(actual_plot_points, range(num_locales), marker="x", label='Actual')
plt.plot([0, 0], [0, num_locales], color='gray', linestyle='-', linewidth=1)
for i, state in enumerate(allStates):
    plt.plot([state.demAvg, state.actual_dem_margin], [i, i], color='gray', linestyle='-', linewidth=0.5)
    plt.text(state.demAvg - 5, i - 0.3, state.abbr, fontsize=8)

plt.rcParams["figure.figsize"] = (15,12)
plt.title("Predicted vs actual Democratic margin by state")
plt.xlim([-105,105])
plt.yticks([])
plt.legend()

plt.show()


# Calculating and printing some details of the results

correct_calls = 0
avg_miss = 0
for state in allStates:
    
    # Note: the simulation usually gives Ohio as a 0.0 Dem margin tie in demAvg, which will throw a 
    # divide-by-zero error below, so I just arbitrarily change it to an 0.1 margin. This will result in Ohio
    # being designated as incorrectly called, but since I (and the pollsters, circa fall 2020) missed it by a 
    # full 8 points, I'll accept the loss
    
    if state.demAvg == 0:
        state.demAvg += 0.1
    
    if state.demAvg / abs(state.demAvg) == state.actual_dem_margin / abs(state.actual_dem_margin):
        correct_calls += 1
    avg_miss += abs(state.demAvg - state.actual_dem_margin) / len(allStates)
    
print("States and districts correctly called: ", 
    correct_calls, 
    "/", 
    num_locales, 
    "\t",
    str(round(100 * correct_calls / num_locales, 0)) + "%"
    )
print("Average % margin miss: ", 
    '\t',
    '\t',
    str(round(avg_miss, 0)) + "%"
    )
print("Predicted electoral votes: ",
    "\t",
    "\t",
    int(round(avgDemEVs,0)), 
    "Democratic,",
    int(round(avgGOPEVs,0)),
    "Republican"
    )
print("Actual electoral votes: ",
    "\t",
    "\t",
    306,
    "Democratic,",
    232,
    "Republican"
    )
