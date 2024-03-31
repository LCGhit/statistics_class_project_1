import pandas as pd
import matplotlib.pyplot as plt

########################################
########## DATAFRAMES CLEANUP ##########
########################################
# delete all entries but the latest - assumes entries may not be ordered
def getLatestEntries(dataframe, column):
    maxTime = 0
    maxTimeEntry = pd.DataFrame
    for entry in dataframe[column]:
        date, hour = entry.split(" ")
        year,month,day = date.split("-")
        h,m,s = hour.split(":")
        totalTime = int(year)*12*30+int(month)*30+int(day)+int(h)/24+int(m)/60/24+int(s)/60/60/24 #computed in days
        if totalTime > maxTime:
            maxTime = totalTime
            maxTimeEntry = entry
    return(dataframe[dataframe[column] == maxTimeEntry])

overall_vote_count_pd = pd.DataFrame(pd.read_csv("Eleicoes/Legislativas2019/overall_results.csv"))
overall_vote_count_pd = getLatestEntries(overall_vote_count_pd,"time").drop(columns=["time", "territoryFullName", "territoryKey", "numParishesApproved"], axis=1)  #columns that are mostly redundant/irrelevant

parishes_vote_count_pd = pd.DataFrame(pd.read_csv("Eleicoes/Legislativas2019/parishes.csv")).drop(columns=["time", "territoryFullName", "territoryKey", "totalMandates", "pre.totalMandates", "numParishes", "numParishesApproved", "availableMandates", "pre.availableMandates"], axis=1) #numParishes and numParishesApproved is obviously always 1, availableMandates always 0

county_parties_result_pd = pd.DataFrame(pd.read_csv("Eleicoes/Legislativas2019/votes.csv"))
county_parties_result_pd = getLatestEntries(county_parties_result_pd,"time").drop("time", axis=1)

parishes_parties_result_pd = pd.DataFrame(pd.read_csv("Eleicoes/Legislativas2019/votes_parishes.csv"))

########################################
########## DATAFRAMES CLEANUP ##########
########################################

def list_entries(column, table):
    try:
        return (sorted(list((table.loc[:, column].drop_duplicates()))))
    except:
        print("erro")
        return

def menuShowOptions(options):
    optionNum = 1
    for item in options:
        print(optionNum, ". ", item)
        optionNum += 1

district = list_entries("territoryName", overall_vote_count_pd)
district.remove("Território Nacional")

# council has district as key and its councils as values
council = dict()
for item in district:
    council[item] = list(parishes_vote_count_pd["Council"][parishes_vote_count_pd["District"] == item].drop_duplicates())

# parish has council as key and its parishes as values
parish = dict()
for key, value in council.items():
    for item in value:
        parish[item] = list(parishes_vote_count_pd["territoryName"][parishes_vote_count_pd["Council"] == item].drop_duplicates())

def retrieveRegion(option):
        match option:
            case "1":
                return pickDistrict()
            case "2":
                return pickCouncil()
            case "3":
                return pickParish()
            case _:
                return -1

def pickDistrict():
    count = 1
    for item in district:
        print(count, item)
        count += 1
    pickedDistrict = input("Escolha o distrito => ")
    return district[int(pickedDistrict)-1]

def pickCouncil():
    district = pickDistrict()
    filteredCouncil= list(parishes_vote_count_pd["Council"][parishes_vote_count_pd["District"] == district].drop_duplicates())
    count = 1
    for item in filteredCouncil:
        print(count, item)
        count += 1
    pickedCouncil = input("Escolha o concelho => ")
    return filteredCouncil[int(pickedCouncil)-1]

def pickParish():
    council = pickCouncil()
    filteredParish = list((parishes_vote_count_pd["territoryName"][parishes_vote_count_pd["Council"] == council].drop_duplicates()))
    count = 1
    for item in filteredParish:
        print(count,item)
        count += 1
    pickedParish = input("Escolha a freguesia => ")
    print(filteredParish[int(pickedParish)-1])
    return filteredParish[int(pickedParish)-1]

def pickColumn(table):
    count = 1
    for col in table.columns:
        print(count, col)
        count += 1
    pickedCol = input("Qual a informação que pretende? => ")
    while int(pickedCol) not in range(0, count):
        pickedCol = input("Opção inexistente.\nQual a informação que pretende? => ")
    return table.columns.tolist()[int(pickedCol)-1]


def func_one():
    territoryList = []
    pickRegionFlag = "s"
    adminDivision = input("Qual é a divisão administrativa que lhe interessa?\n1 Distrito\n2 Concelho\n3 Freguesia\nDigite um número => ")
    territoryList.append(retrieveRegion(adminDivision))
    while pickRegionFlag == "s":
        print("Escolha região para comparar")
        territoryList.append(retrieveRegion(adminDivision))
        print("Regiões selecionadas ", territoryList)
        pickRegionFlag = input("Escolher outra região?(s/n) => ")
    if adminDivision == "1":
        column = pickColumn(overall_vote_count_pd)
        plt.bar(list(overall_vote_count_pd["territoryName"][overall_vote_count_pd["territoryName"].isin(territoryList)]), overall_vote_count_pd[column][overall_vote_count_pd["territoryName"].isin(territoryList)])
        plt.ylabel(column)
        plt.show()
    elif adminDivision == "2":
        column = pickColumn(parishes_vote_count_pd)
        plt.bar(list(parishes_vote_count_pd["Council"][parishes_vote_count_pd["Council"].isin(territoryList)]), parishes_vote_count_pd[column][parishes_vote_count_pd["Council"].isin(territoryList)])
        plt.ylabel(column)
        plt.show()
    else:
        column = pickColumn(parishes_vote_count_pd)
        plt.bar(list(parishes_vote_count_pd["Parish"][parishes_vote_count_pd["Parish"].isin(territoryList)]), parishes_vote_count_pd[column][parishes_vote_count_pd["Parish"].isin(territoryList)])
        plt.ylabel(column)
        plt.show()

func_one()
