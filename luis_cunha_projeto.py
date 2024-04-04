import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from pandas.compat import pickle_compat
# from pandas.core.generic import pickle

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

council_vote_count_pd = parishes_vote_count_pd.groupby("Council").sum(numeric_only=True).reset_index() # group info by council based on the parishes info dataframe
councilPercentagesColumns = ["blankVotesPercentage", "nullVotesPercentage", "votersPercentage", "pre.blankVotesPercentage", "pre.nullVotesPercentage", "pre.votersPercentage"]

councils = (list(council_vote_count_pd["Council"]))
for item in councils:
    for subitem in councilPercentagesColumns:
        council_vote_count_pd[subitem][council_vote_count_pd["Council"] == item] = parishes_vote_count_pd[subitem][parishes_vote_count_pd["Council"] == item].mean()

district_parties_result_pd = pd.DataFrame(pd.read_csv("Eleicoes/Legislativas2019/votes.csv"))
district_parties_result_pd = getLatestEntries(district_parties_result_pd,"time").drop("time", axis=1)

parishes_parties_result_pd = pd.DataFrame(pd.read_csv("Eleicoes/Legislativas2019/votes_parishes.csv"))

########################################
########## DATAFRAMES CLEANUP ##########
########################################

district = list(overall_vote_count_pd.loc[:, "territoryName"].drop_duplicates())
district.remove("Território Nacional")

def pickDistrict(exceptions):
    count = 1
    cleanDistrictList = district
    for item in exceptions:
        try:
            cleanDistrictList.remove(item)
        except:
            continue
    print("\n#####DISTRITOS#####")
    for item in cleanDistrictList:
        print(count, item)
        count += 1
    pickedDistrict = ""
    while pickedDistrict not in cleanDistrictList:
        pickedDistrict = input("Escolha um distrito => ")
        try:
            pickedDistrict = cleanDistrictList[int(pickedDistrict)-1]
        except:
            print("----- AVISO\": Valor inválido -----")
            pickedDistrict = ""
    return pickedDistrict

def pickCouncil(exceptions):
    district = pickDistrict(exceptions)
    while district == "Açores":
        print("----- AVISO\": Não há informação sobre as subregiões dos Açores -----")
        district = pickDistrict(exceptions)
    filteredCouncil= list(parishes_vote_count_pd["Council"][parishes_vote_count_pd["District"] == district].drop_duplicates())
    cleanCouncilList = filteredCouncil
    for item in exceptions:
        try:
            cleanCouncilList.remove(item)
        except:
            continue
    count = 1
    print("\n#####CONCELHOS#####")
    for item in cleanCouncilList:
        print(count, item)
        count += 1
    pickedCouncil = ""
    while pickedCouncil not in cleanCouncilList:
        pickedCouncil = input("Escolha um concelho => ")
        try:
            pickedCouncil = cleanCouncilList[int(pickedCouncil)-1]
        except:
            print("----- AVISO\": Valor inválido -----")
            pickedCouncil = ""
    return pickedCouncil

def pickParish(exceptions):
    council = pickCouncil(exceptions)
    filteredParish = list((parishes_vote_count_pd["territoryName"][parishes_vote_count_pd["Council"] == council].drop_duplicates()))
    count = 1
    cleanParishList = filteredParish
    for item in exceptions:
        try:
            cleanParishList.remove(item)
        except:
            continue
    print("\n#####FREGUESIAS#####")
    for item in cleanParishList:
        print(count,item)
        count += 1
    pickedParish = ""
    while pickedParish not in cleanParishList:
        pickedParish = input("Escolha uma freguesia => ")
        try:
            pickedParish = cleanParishList[int(pickedParish)-1]
        except:
            print("----- AVISO\": Valor inválido -----")
            pickedParish = ""
    return pickedParish

def pickColumn(table, exceptions):
    count = 1
    columns = list((table.columns))
    # delete columns of non quantitative variables and already selected columns
    columnsToRemove = list(["territoryName","Council", "District"])
    columnsToRemove = columnsToRemove + exceptions
    for item in columnsToRemove:
        try:
            columns.remove(item)
        except:
            continue
    print("#####INFORMAÇÕES DISPONÍVEIS#####")
    for col in columns:
        print(count, col)
        count += 1
    pickedCol = ""
    while pickedCol not in columns:
        pickedCol = input("Qual a informação que pretende? => ")
        try:
            pickedCol = columns[int(pickedCol)-1]
        except:
            print("----- AVISO: Valor inválido -----")
            pickedCol = ""
    return pickedCol


def func_one():
    adminDivision = input("1 Distrito\n2 Concelho\n3 Freguesia\n4 Cancelar operação\nQual a divisão administrativa de interesse?\nDigite um número => ")
    while adminDivision not in ["1","2","3","4"]:
        adminDivision = input("\n1 Distrito\n2 Concelho\n3 Freguesia\n4 Cancelar operação\nQual a divisão administrativa de interesse?\nDigite um número => ")
    match adminDivision:
        case "1":
            def adminDivisionFun(array): return pickDistrict(array)
        case "2":
            def adminDivisionFun(array): return pickCouncil(array)
        case "3":
            def adminDivisionFun(array): return pickParish(array)
        case "4":
            print("Operação cancelada")
            return
        case _:
            print("----- AVISO: Valor inválido -----")

    territoryList = []
    pickRegionFlag = "s"
    territoryList.append(adminDivisionFun(territoryList))
    while pickRegionFlag == "s":
        print("Regiões selecionadas ", territoryList)
        territoryList.append(adminDivisionFun(territoryList))
        pickRegionFlag = input("Escolher outra região?(s/n) => ")
        while pickRegionFlag != "s" and pickRegionFlag != "n":
            print("----- AVISO: Valor inválido -----")
            pickRegionFlag = input("Escolher outra região?(s/n) => ")

    if adminDivision == "1":
        usedDataFrame = overall_vote_count_pd
        indexCol = "territoryName"
        column = []
        pickColumnFlag = "s"
        while pickColumnFlag == "s" or len(column) == 0:
            column.append(pickColumn(usedDataFrame, column))
            print("Informações selecionadas ", column)
            pickColumnFlag = input("Escolher mais informações?(s/n) => ")
            while pickColumnFlag != "s" and pickColumnFlag != "n":
                print("----- AVISO: Valor inválido -----")
                pickColumnFlag = input("Escolher mais informações?(s/n) => ")
    elif adminDivision == "2":
        usedDataFrame = council_vote_count_pd
        indexCol = "Council"
        column = []
        pickColumnFlag = "s"
        while pickColumnFlag == "s" or len(column) == 0:
            column.append(pickColumn(usedDataFrame, column))
            print("Informações selecionadas ", column)
            pickColumnFlag = input("Escolher mais informações?(s/n) => ")
            while pickColumnFlag != "s" and pickColumnFlag != "n":
                print("----- AVISO: Valor inválido -----")
                pickColumnFlag = input("Escolher mais informações?(s/n) => ")
    else:
        usedDataFrame = parishes_vote_count_pd
        indexCol = "territoryName"
        column = []
        pickColumnFlag = "s"
        while pickColumnFlag == "s" or len(column) == 0:
            column.append(pickColumn(usedDataFrame, column))
            print("Informações selecionadas ", column)
            pickColumnFlag = input("Escolher mais informações?(s/n) => ")
            while pickColumnFlag != "s" and pickColumnFlag != "n":
                print("----- AVISO: Valor inválido -----")
                pickColumnFlag = input("Escolher mais informações?(s/n) => ")

    ax = plt.subplot(111)
    ind = np.arange(len(territoryList))
    width = 0.15
    rects = []
    usedDataFrame = usedDataFrame.groupby(indexCol).sum().reset_index() #required for councils, which have multiple entries in the dataset
    for item in column:
        rects.append(ax.bar(ind+(width*column.index(item)), usedDataFrame[item][usedDataFrame[indexCol].isin(territoryList)], width))
        ax.set_xticks(ind+(width*column.index(item))/2)
        ax.set_xticklabels(territoryList, rotation=45)
    graphBars = []
    for item in rects:
        graphBars.append(item[0])
    ax.legend(graphBars,column)
    plt.show()


func_one()
