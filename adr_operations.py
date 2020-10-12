import pandas as pd

# data_frame = pd.read_csv( 'cluster_hotel.csv' )
yearlist = []

# def toCSV(csv_file):
#     data_frame = pd.read_csv(csv_file)
#     return data_frame

def readCsv(file):
    return pd.read_csv(file)

import pandas as pd
data_frame = pd.read_csv('correct_cluster.csv')
yearlist = [int(2015), int(2016), int(2017)]

def monthly_transaction_avg(data_frame):
    averageList = []
    sumList = []
    dfList = []
    dfList.append( readCsv( 'year1.csv' ) )
    dfList.append( readCsv( 'year2.csv' ) )
    dfList.append( readCsv( 'year3.csv' ) )
    for dataframes in dfList:
        averageList.append( dataframes.groupby( ['year', 'month'], sort=False ).mean() )
        sumList.append( dataframes.groupby( ['year', 'month'], sort=False ).sum() )
    print( 'Loading...................' )
    return averageList, sumList

output2 = monthly_transaction_avg( readCsv( 'correct_cluster.csv' ) )


def dictionryOutput():
    adrDic = {}
    adrTotal = {}
    for i in output2[0]:
        # print(i)
        adrInDic = {}
        for j in range( len( i ) ):
            adrInDic[i.index.values[j][1]] = i['adr'].iloc[j]
        adrDic[i.index.values[0][0]] = adrInDic
    for i in output2[1]:
        # print(i)
        adrInTotal = {}
        for j in range( len( i ) ):
            adrInTotal[i.index.values[j][1]] = i['adr'].iloc[j]
        adrTotal[i.index.values[0][0]] = adrInTotal
    return adrDic, adrTotal

def financialYearPattern():
    adrDic = dictionryOutput()[0]
    adrTotalDic = dictionryOutput()[1]
    seasonalDic = {}
    internalDic = {}
    seasonalTotalDic = {}
    internalTotalDic = {}
    count1 = 1
    count2 = 1

    valueList = []

    for keys, values in adrDic.items():
        for i in values.keys():
            valueList.append(values[i])

    monthCount = len(valueList)
    incCount1 = 0
    incCount2 = 0

    for keys, values in adrDic.items():
        for i in values.keys():

            if i == 'June':
                keyVal = 'season' + str( count1 )
                internalDic[i] = values[i]
                incCount1 += 1
                seasonalDic[keyVal] = internalDic
                internalDic = {}
                # internalDic = {}
                count1 = count1 + 1
            else:
                incCount1 += 1
                internalDic[i] = values[i]

            if incCount1 == monthCount:
                keyVal = 'season' + str( count1 )
                internalDic[i] = values[i]
                incCount1 += 1
                seasonalDic[keyVal] = internalDic

    for keys, values in adrTotalDic.items():
        for i in values.keys():
            if i == 'June':
                keyVal = 'season' + str( count2 )
                internalTotalDic[i] = values[i]
                incCount2 += 1
                seasonalTotalDic[keyVal] = internalTotalDic
                internalTotalDic = {}
                count2 = count2 + 1
            else:
                incCount2 += 1
                internalTotalDic[i] = values[i]

            if incCount2 == 26:
                keyVal = 'season' + str( count2 )
                internalTotalDic[i] = values[i]
                incCount2 += 1
                seasonalTotalDic[keyVal] = internalTotalDic

    return seasonalDic, seasonalTotalDic

def annualDailyRateAvg():
    avgDic = {}

    season1 = list(financialYearPattern()[0]['season1'].values() )
    season2 = list(financialYearPattern()[0]['season2'].values() )

    months = list(financialYearPattern()[0]['season1'] )

    for i, j, month in zip( season1, season2, months ):
        avgDic[month] = (i + j) / 2

    return avgDic

def annualTotalRevAvg():
    avgDic = {}

    season1 = list(financialYearPattern()[1]['season1'].values() )
    season2 = list(financialYearPattern()[1]['season2'].values() )

    months = list(financialYearPattern()[1]['season1'] )

    for i, j, month in zip( season1, season2, months ):
        avgDic[month] = (i + j) / 2

    return avgDic

def yearList():
    return yearlist