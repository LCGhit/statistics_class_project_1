import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

########################################
########## DATAFRAMES CLEANUP ##########
########################################
# delete all entries but the latest - assumes entries may not be ordered
def getLatestEntries(dataframe, column):
    maxTime = 0
    maxTimeEntry = pd.DataFrame
    for entry in dataframe[column]:
        try:
            date, hour = entry.split(" ")
            year,month,day = date.split("-")
            h,m,s = hour.split(":")
            totalTime = int(year)*12*30+int(month)*30+int(day)+int(h)/24+int(m)/60/24+int(s)/60/60/24 #computed in days
        except:
            year,month,day = entry.split("-")
            totalTime = int(year)*12*30+int(month)*30+int(day) #computed in days
        if totalTime > maxTime:
            maxTime = totalTime
            maxTimeEntry = entry
    return(dataframe[dataframe[column] == maxTimeEntry])

overall_vote_count_pd = pd.DataFrame(pd.read_csv("Eleicoes/Legislativas2019/overall_results.csv"))
overall_vote_count_pd = getLatestEntries(overall_vote_count_pd,"time").drop(columns=["time", "territoryFullName", "territoryKey", "numParishesApproved", "availableMandates", "pre.availableMandates"], axis=1)  #columns that are mostly redundant/irrelevant

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
parishes_parties_result_pd.rename(columns = {"District":"Parish"}, inplace=True)

council_parties_result_pd = parishes_parties_result_pd.groupby(["District.1", "Council", "Party"]).sum(numeric_only=True).reset_index()
council_parties_result_pd = council_parties_result_pd[["Council", "Party", "Votes", "District.1"]]

previousYear_parties_result_pd = pd.DataFrame(pd.read_csv("Eleicoes/complementares/resultados-legislativas-1975-2011.csv"))
previousYear_parties_result_pd = getLatestEntries(previousYear_parties_result_pd, "data")


### translate columns names ###
overall_vote_count_pd.rename(columns={"territoryName":"Distrito", "totalMandates":"Mandatos", "numParishes":"Num de freguesias", "blankVotes":"Votos em branco", "blankVotesPercentage":"% de votos em branco", "nullVotes":"Votos nulos", "nullVotesPercentage":"% de votos nulos", "votersPercentage":"% de eleitores", "subscribedVoters":"Eleitores registados", "totalVoters":"Total de eleitores", "pre.totalMandates":"(legislativas prévias)Mandatos", "pre.blankVotes":"(legislativas prévias)Votos em branco", "pre.blankVotesPercentage":"(legislativas prévias)% de votos em branco", "pre.nullVotes":"(legislativas prévias)Votos nulos", "pre.nullVotesPercentage":"(legislativas prévias)% de votos nulos", "pre.votersPercentage":"(legislativas prévias)% de eleitores", "pre.subscribedVoters":"(legislativas prévias)Eleitores registados", "pre.totalVoters":"(legislativas prévias)Total de eleitores"}, inplace=True)

council_vote_count_pd.rename(columns={"Council":"Concelho", "numParishes":"Num de freguesias", "blankVotes":"Votos em branco", "blankVotesPercentage":"% de votos em branco", "nullVotes":"Votos nulos", "nullVotesPercentage":"% de votos nulos", "votersPercentage":"% de eleitores", "subscribedVoters":"Eleitores registados", "totalVoters":"Total de eleitores", "pre.blankVotes":"(legislativas prévias)Votos em branco", "pre.blankVotesPercentage":"(legislativas prévias)% de votos em branco", "pre.nullVotes":"(legislativas prévias)Votos nulos", "pre.nullVotesPercentage":"(legislativas prévias)% de votos nulos", "pre.votersPercentage":"(legislativas prévias)% de eleitores", "pre.subscribedVoters":"(legislativas prévias)Eleitores registados", "pre.totalVoters":"(legislativas prévias)Total de eleitores"}, inplace=True)

parishes_vote_count_pd.rename(columns={"territoryName":"Freguesia", "numParishes":"Num de freguesias", "blankVotes":"Votos em branco", "blankVotesPercentage":"% de votos em branco", "nullVotes":"Votos nulos", "nullVotesPercentage":"% de votos nulos", "votersPercentage":"% de eleitores", "subscribedVoters":"Eleitores registados", "totalVoters":"Total de eleitores", "pre.blankVotes":"(legislativas prévias)Votos em branco", "pre.blankVotesPercentage":"(legislativas prévias)% de votos em branco", "pre.nullVotes":"(legislativas prévias)Votos nulos", "pre.nullVotesPercentage":"(legislativas prévias)% de votos nulos", "pre.votersPercentage":"(legislativas prévias)% de eleitores", "pre.subscribedVoters":"(legislativas prévias)Eleitores registados", "pre.totalVoters":"(legislativas prévias)Total de eleitores", "Council":"Concelho", "District":"Distrito"}, inplace=True)
### translate columns names ###

########################################
########## DATAFRAMES CLEANUP ##########
########################################

def getBold(input):
    bold = "\033[1m"+input+"\033[0m"
    return bold

district = list(overall_vote_count_pd.loc[:, "Distrito"].drop_duplicates())
district.remove("Território Nacional")

def pickDistrict(exceptions):
    count = 1
    cleanDistrictList = district
    for item in exceptions:
        try:
            cleanDistrictList.remove(item)
        except:
            continue
    print(getBold("\n#####DISTRITO#####"))
    for item in cleanDistrictList:
        print("\033[1m",count,"\033[0m", item)
        count += 1
    pickedDistrict = ""
    while pickedDistrict not in cleanDistrictList:
        pickedDistrict = input("Escolha um distrito => ")
        try:
            pickedDistrict = cleanDistrictList[int(pickedDistrict)-1]
        except:
            print("----- \033[1m AVISO \033[0m: Valor inválido -----")
            pickedDistrict = ""
    return pickedDistrict

def pickCouncil(exceptions):
    district = pickDistrict(exceptions)
    while district == "Açores":
        print("----- \033[1m AVISO \033[0m: Não há informação sobre as subregiões dos Açores -----")
        district = pickDistrict(exceptions)
    filteredCouncil= list(parishes_vote_count_pd["Concelho"][parishes_vote_count_pd["Distrito"] == district].drop_duplicates())
    cleanCouncilList = filteredCouncil
    for item in exceptions:
        try:
            cleanCouncilList.remove(item)
        except:
            continue
    count = 1
    print(getBold("\n#####CONCELHO#####"))
    for item in cleanCouncilList:
        print("\033[1m",count,"\033[0m", item)
        count += 1
    pickedCouncil = ""
    while pickedCouncil not in cleanCouncilList:
        pickedCouncil = input("Escolha um concelho => ")
        try:
            pickedCouncil = cleanCouncilList[int(pickedCouncil)-1]
        except:
            print("----- \033[1m AVISO \033[0m: Valor inválido -----")
            pickedCouncil = ""
    return pickedCouncil

def pickParish(exceptions):
    council = pickCouncil(exceptions)
    filteredParish = list((parishes_vote_count_pd["Freguesia"][parishes_vote_count_pd["Concelho"] == council].drop_duplicates()))
    count = 1
    cleanParishList = filteredParish
    for item in exceptions:
        try:
            cleanParishList.remove(item)
        except:
            continue
    print(getBold("\n#####FREGUESIA#####"))
    for item in cleanParishList:
        print("\033[1m",count,"\033[0m",item)
        count += 1
    pickedParish = ""
    while pickedParish not in cleanParishList:
        pickedParish = input("Escolha uma freguesia => ")
        try:
            pickedParish = cleanParishList[int(pickedParish)-1]
        except:
            print("----- \033[1m AVISO \033[0m: Valor inválido -----")
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
    print(getBold("\n#####INFORMAÇÕES DISPONÍVEIS#####"))
    for col in columns:
        print("\033[1m",count,"\033[0m", col)
        count += 1
    pickedCol = ""
    while pickedCol not in columns:
        pickedCol = input("Qual a informação que pretende? => ")
        try:
            pickedCol = columns[int(pickedCol)-1]
        except:
            print("----- \033[1m AVISO \033[0m: Valor inválido -----")
            pickedCol = ""
    return pickedCol


def pickParty():
    partyList = list(council_parties_result_pd["Party"].drop_duplicates())
    pickedParty = ""
    while pickedParty not in partyList:
        count = 1
        for item in partyList:
            print("\033[1m",count,"\033[0m", item)
            count += 1
        try:
            pickedParty = int(input(" \033[1m0\033[0m Voltar\nEscolha um partido => "))-1
            if pickedParty == -1:
                return
            else:
                pickedParty = partyList[pickedParty]
        except:
            print("----- \033[1m AVISO \033[0m: Opção inválida -----")
    return pickedParty

def func_one():
    adminDivision = input("\033[1mQual a divisão administrativa de interesse?\033[0m\n\033[1m1\033[0m Distrito\n\033[1m2\033[0m Concelho\n\033[1m3\033[0m Freguesia\n\033[1m4\033[0m Cancelar operação\nDigite um número => ")
    while adminDivision not in ["1","2","3","4"]:
        adminDivision = input("\033[1mQual a divisão administrativa de interesse?\033[0m\n\033[1m1\033[0m Distrito\n\033[1m2\033[0m Concelho\n\033[1m3\033[0m Freguesia\n\033[1m4\033[0m Cancelar operação\nDigite um número => ")
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
            return

    territoryList = []
    pickRegionFlag = "s"
    territoryList.append(adminDivisionFun(territoryList))
    print("\n(\033[1mRegiões selecionadas ", territoryList, "\033[0m")
    while pickRegionFlag == "s":
        territoryList.append(adminDivisionFun(territoryList))
        print("\n(\033[1mRegiões selecionadas ", territoryList, "\033[0m")
        pickRegionFlag = input("Escolher outra região?(\033[1ms/n\033[0m) => ")
        while pickRegionFlag != "s" and pickRegionFlag != "n":
            print("----- \033[1m AVISO \033[0m: Valor inválido -----")
            pickRegionFlag = input("Escolher outra região?(\033[1ms/n\033[0m) => ")

    if adminDivision == "1":
        usedDataFrame = overall_vote_count_pd
        indexCol = "Distrito"
        column = []
        pickColumnFlag = "s"
        while pickColumnFlag == "s" or len(column) == 0:
            column.append(pickColumn(usedDataFrame.drop(columns=["Distrito"], axis=1), column))
            print("\n\033[1mInformações selecionadas ", column, "\033[0m")
            pickColumnFlag = input("Escolher mais informações?(\033[1ms/n\033[0m) => ")
            while pickColumnFlag != "s" and pickColumnFlag != "n":
                print("----- \033[1m AVISO \033[0m: Valor inválido -----")
                pickColumnFlag = input("Escolher mais informações?(\033[1ms/n\033[0m) => ")
    elif adminDivision == "2":
        usedDataFrame = council_vote_count_pd
        indexCol = "Concelho"
        column = []
        pickColumnFlag = "s"
        while pickColumnFlag == "s" or len(column) == 0:
            column.append(pickColumn(usedDataFrame.drop(columns=["Concelho"], axis=1), column))
            print("\n\033[1mInformações selecionadas ", column, "\033[0m")
            pickColumnFlag = input("Escolher mais informações?(\033[1ms/n\033[0m) => ")
            while pickColumnFlag != "s" and pickColumnFlag != "n":
                print("----- \033[1m AVISO \033[0m: Valor inválido -----")
                pickColumnFlag = input("Escolher mais informações?(\033[1ms/n\033[0m) => ")
    else:
        usedDataFrame = parishes_vote_count_pd
        indexCol = "Freguesia"
        column = []
        pickColumnFlag = "s"
        while pickColumnFlag == "s" or len(column) == 0:
            column.append(pickColumn(usedDataFrame.drop(columns=["Freguesia", "Concelho", "Distrito"], axis=1), column))
            print("\n\033[1mInformações selecionadas ", column, "\033[0m")
            pickColumnFlag = input("Escolher mais informações?(\033[1ms/n\033[0m) => ")
            while pickColumnFlag != "s" and pickColumnFlag != "n":
                print("----- \033[1m AVISO \033[0m: Valor inválido -----")
                pickColumnFlag = input("Escolher mais informações?(\033[1ms/n\033[0m) => ")

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


def func_two():
    partyList = list(council_parties_result_pd["Party"].drop_duplicates())
    pickedParty = pickParty()
    lostCouncils = []
    print("PARTIDO ESCOLHIDO: ", pickedParty, "\nAguarde por favor...")
    for item in list(council_parties_result_pd["Council"].drop_duplicates()):
        if pickedParty not in list(council_parties_result_pd["Party"][council_parties_result_pd["Votes"] == council_parties_result_pd["Votes"][council_parties_result_pd["Council"] == item].max()][council_parties_result_pd["Council"] == item]):
            lostCouncils.append(item)

    optimalCouncils = dict()
    for council in lostCouncils:

        # vote sum from the whole district of the council
        theDistrict = list(council_parties_result_pd["District.1"][council_parties_result_pd["Council"] == council].drop_duplicates())[0]

        # array with the district's total vote count for each party
        partiesTotalVotes = []
        for party in partyList:
            partiesTotalVotes.append(council_parties_result_pd["Votes"][council_parties_result_pd["District.1"] == theDistrict][council_parties_result_pd["Party"] == party].sum())

        districtTotalVotes = council_parties_result_pd["Votes"][council_parties_result_pd["District.1"] == theDistrict][council_parties_result_pd["Party"] == pickedParty].sum()

        if max(partiesTotalVotes) == districtTotalVotes:
            optimalCouncils.setdefault(theDistrict, [])
            optimalCouncils[theDistrict].append(council)
    if len(optimalCouncils) != 0:
        pick = -1
        while pick not in range(0, len(optimalCouncils)):
            print("\nConsulte os concelhos com maior probabilidade de serem recuperados pelo partido escolhido(" , pickedParty , ") nos distritos...")
            counter = 1
            for key in optimalCouncils:
                print(getBold(str(counter)) + " DISTRITO: " + key.upper())
                counter += 1
            print(getBold("0"), "Voltar")
            dicKeys = list(optimalCouncils.keys())
            pick = input("Escolha o distrito => ")
            if pick == "0":
                break
            try:
                district = dicKeys[int(pick)-1]
                print("\nOs concelhos do distrito de", district, ":")
                for value in optimalCouncils[district]:
                    print(value)
            except:
                pick = -1
                print("----- \033[1m AVISO \033[0m: Opção inválida -----")
    else:
        print("O seu partido não venceu em qualquer distrito.")


def func_three():
    thisYear = district_parties_result_pd
    previousYear = previousYear_parties_result_pd
    party = pickParty()
    territoryList = []
    pickRegionFlag = "s"
    territoryList.append(pickDistrict(territoryList))
    print("\n(\033[1mRegiões selecionadas ", territoryList, "\033[0m")
    while pickRegionFlag == "s":
        territoryList.append(pickDistrict(territoryList))
        print("\n(\033[1mRegiões selecionadas ", territoryList, "\033[0m")
        pickRegionFlag = input("Escolher outra região?(\033[1ms/n\033[0m) => ")
        while pickRegionFlag != "s" and pickRegionFlag != "n":
            print("----- \033[1m AVISO \033[0m: Valor inválido -----")
            pickRegionFlag = input("Escolher outra região?(\033[1ms/n\033[0m) => ")

    previousYear.rename(columns={"num_votos":"Votes", "partido":"Party", "nome":"District"}, inplace=True)
    # for item in territoryList:
    #     print(thisYear["validVotesPercentage"][thisYear["Party"] == party][thisYear["District"] == item])
    #     print(previousYear["validVotesPercentage"][previousYear["Party"] == party][previousYear["District"] == item])

    column = ["Votes"]
    ax = plt.subplot(111)
    ind = np.arange(len(territoryList))
    width = 0.15
    ax.bar(ind+(width*column.index("Votes")), thisYear["Votes"][thisYear["Party"] == party][thisYear["District"].isin(territoryList)], width)
    ax.set_xticks(ind+(width*column.index("Votes"))/2)
    ax.set_xticklabels(territoryList, rotation=45)

    ax.bar(ind+(width*column.index("Votes")), previousYear["Votes"][previousYear["Party"] == party][previousYear["District"].isin(territoryList)], width)
    ax.set_xticks(ind+(width*column.index("Votes"))/2)
    ax.set_xticklabels(territoryList, rotation=45)
    plt.show()

def mainMenu():
    option = ""
    print(getBold("MENSAGEM DE BOAS-VINDAS"))
    while option != "0":
        print(getBold("*MENU PRINCIPAL*"))
        print(getBold("O que pretende fazer?") + "\n\033[1m1\033[0m Comparar dados entre regiões\n\033[1m2\033[0m Determinar concelhos mais promissores para o partido\n\033[1m3\033[0m Determinar zonas mais voláteis\n\033[1m0\033[0m Sair")
        option = input("Escolha uma opção => ")
        match option:
            case "1":
                func_one()
            case "2":
                func_two()
            case "3":
                func_three()
            case "0":
                doubleCheck = ""
                while doubleCheck not in ["s", "n"]:
                    doubleCheck = input("Tem a certeza que pretende sair?(\033[1ms/n\033[0m) => ")
                    if doubleCheck == "s":
                        print(getBold("Até breve!"))
                        break
                    elif doubleCheck == "n":
                        option = ""
                    else:
                        print("----- \033[1m AVISO \033[0m: Opção inválida -----")
            case _:
                print("----- \033[1m AVISO \033[0m: Opção inválida -----")

# mainMenu()
func_three()
