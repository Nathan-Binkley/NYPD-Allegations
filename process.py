import time
import math

'''
FORMAT:
# Police ID
# First Name
# Last Name
# Current precinct
# Complaint id
# Month recieved
# Year recieved
# Month closed
# Year Closed
# Command during incident
# Rank Abbreviation at incident
# Rank Abbreviation now
# Rank at incident
# Rank now
# Officer Ethnicity
# Officer Gender
# Officer Age
# Complaintant ethnicity
# Complaintant Gender
# Complaintant Age
# Allegation Type
# Allegation
# Precinct
# Contact Reason
# Outcome 
# Board Disposition
'''
f = 'Data/raw.csv'
data = ""

precincts = {}
officers = {}
outcomes = {}
totalCases = 0



def getPrecinct(info):
    # print("PRECINCT: " + info)
    if info not in precincts:
        precincts[info] = 1
    else:
        precincts[info] += 1

def getOfficerInfo(info):
    # print("OFFICER: " + ", ".join(info))
    if " ".join(info[1:3]) in officers:
        officers[" ".join(info[1:3])] += 1
    else:
        officers[" ".join(info[1:3])] = 1
    
def getOutcome(info):
    # print("OUTCOME: " + ", ".join(info))
    officerResult = info[-1]
    if officerResult in outcomes:
        outcomes[officerResult] += 1
    else:
        outcomes[officerResult] = 1

def getIncidentInfo(info):
    info = info.split(",")
    getOfficerInfo(info[:3] + info[14:17])
    getComplaintantInfo(info[17:20])
    getOutcome(info[-2:])
    getPrecinct(info[22])
    # print("\n")
    # time.sleep(1)

def getComplaintantInfo(info):
    # print("COMPLAINTANT: " + ", ".join(info))
    pass
    

def processData(data):
    global totalCases
    incidents = data.split("\n")
    totalCases = len(incidents)
    
    for incident in incidents:
        if incident:
            getIncidentInfo(incident)

def getTotalSubstantiated(dictionary):
    totalSub = 0
    for case in dictionary:
        if "Substantiated" in case:
            if "Un" in case:
                pass
            else:
                totalSub += dictionary[case]
    return totalSub + 1

with open(f,'r') as f:
    line = f.readline()
    # print(line) # throwaway line for headings
    line = f.readline()
    
    while line:
        data += line + "\n"
        line = f.readline()

processData(data)

sorted_Officers = sorted(officers.items(), key= lambda x: x[1], reverse=True)
sorted_Precincts = sorted(precincts.items(), key= lambda x: x[1], reverse=True)
sorted_Outcomes = sorted(outcomes.items(), key= lambda x: x[1], reverse=True)

for i in sorted_Officers:
    print(i[0],i[1])
for i in sorted_Precincts:
    print(i[0],i[1])
for i in sorted_Outcomes:
    print(i[0] + ":", i[1])

totalSubstantiated = getTotalSubstantiated(outcomes)

print("TOTAL CASES: " + str(totalCases))
print("TOTAL SUBSTANTIATED: " + str(totalSubstantiated))
totalUnsubstantiated = totalCases-totalSubstantiated
print("TOTAL UNSUBSTANTIATED: " + str(totalUnsubstantiated))

percentageSubstantiated = totalSubstantiated/totalCases * 100
percentageUnsubstantiated = totalUnsubstantiated/totalCases * 100

print("% SUBSTANTIATED: " + str(round(percentageSubstantiated,2)))
print("% UNSUBSTANTIATED: " + str(round(percentageUnsubstantiated,2)))

# print(data)

