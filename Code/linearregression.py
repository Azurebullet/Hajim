import pickle
import pandas as pd
import numpy as np
import sklearn

#load pickled data into pandas data frame
terms = pd.read_pickle("term.pkl", compression='infer')
demograph =pd.read_pickle("demograph.pkl", compression='infer')



tCol=terms.columns.tolist()
dCol=demograph.columns.tolist()
print(tCol)
print(dCol)

allData = pd.merge(terms, demograph, on='SubjectID')
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('FINFIN.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
allData.to_excel(writer, sheet_name='Sheet1')

print(allData)
allData['TermNo'] = allData.groupby(['SubjectID']).cumcount()+1

#add dummy variables

#race
allData.loc[ (allData['2010 IPEDS Ethnicity Description'] == 'White'), 'RaceWhite' ] = 1
allData.loc[ (allData['2010 IPEDS Ethnicity Description'] != 'White'), 'RaceWhite' ] = 0
allData.loc[ (allData['2010 IPEDS Ethnicity Description'] == 'Hispanic'), 'RaceHispanic' ] = 1
allData.loc[ (allData['2010 IPEDS Ethnicity Description'] != 'Hispanic'), 'RaceHispanic' ] = 0
allData.loc[ (allData['2010 IPEDS Ethnicity Description'] == 'Black'), 'RaceBlack' ] = 1
allData.loc[ (allData['2010 IPEDS Ethnicity Description'] != 'Black'), 'RaceBlack' ] = 0
allData.loc[ (allData['2010 IPEDS Ethnicity Description'] == 'Asian'), 'RaceAsian' ] = 1
allData.loc[ (allData['2010 IPEDS Ethnicity Description'] != 'Asian'), 'RaceAsian' ] = 0

#degree type
allData.loc[ (allData['Degree Major1 Discipline Code'] == 'HUMS'), 'HUMS' ] = 1
allData.loc[ (allData['Degree Major1 Discipline Code'] != 'HUMS'), 'HUMS' ] = 0
allData.loc[ (allData['Degree Major1 Discipline Code'] == 'ENGN'), 'ENGN' ] = 1
allData.loc[ (allData['Degree Major1 Discipline Code'] != 'ENGN'), 'ENGN' ] = 0
allData.loc[ (allData['Degree Major1 Discipline Code'] == 'SOCS'), 'SOCS' ] = 1
allData.loc[ (allData['Degree Major1 Discipline Code'] != 'SOCS'), 'SOCS' ] = 0
allData.loc[ (allData['Degree Major1 Discipline Code'] == 'NATS'), 'NATS' ] = 1
allData.loc[ (allData['Degree Major1 Discipline Code'] != 'NATS'), 'NATS' ] = 0

#Test Scores
allData["SAT Math"] = pd.to_numeric(allData["SAT Math"])
allData["ACT Math"] = pd.to_numeric(allData["ACT Math"])

allData['LowSAT'] = 0
allData.loc[ (allData['SAT Math'] <= 630), 'LowSAT' ] = 1

allData['MidSAT'] = 0
allData.loc[ (allData['SAT Math'] > 27 ) & (allData['SAT Math']< 33), 'MidSAT' ] = 1

allData['HighSAT'] = 0
allData.loc[ (allData['SAT Math'] <= 730), 'HighSAT' ] = 1

#ACT scores
allData['LowACT']=0
allData.loc[ (allData['ACT Math'] <= 27), 'LowACT' ] = 1

allData['MidACT'] = 0
allData.loc[ (allData['ACT Math'] > 27 ) & (allData['ACT Math']< 33), 'MidACT' ] = 1


allData['HighACT'] = 0
allData.loc[ (allData['ACT Math'] >= 33), 'HighACT' ] = 1

# foreign student flag

allData['Foreign Student']=1
allData.loc[ (allData['Citizen Type'] == "US CITIZEN"), 'Foreign Student' ] = 0


#individual semester GPA
iGPA1= allData.loc[allData['TermNo'] == 1]
iGPA2=allData.loc[allData['TermNo'] == 1]
GPA1 = pd.DataFrame(iGPA1, columns=["SubjectID","Term GPA"])
GPA2 = pd.DataFrame(iGPA2, columns=["SubjectID","Term GPA"])
GPA1.rename(columns={'Term GPA': 'GPA 1'}, inplace=True)
GPA2.rename(columns={'Term GPA': 'GPA 2'}, inplace=True)

#semester 1 data
firstSemester=allData.loc[allData['TermNo'] == 1]
#print(allData.columns.tolist())
#print(allData.to_string())


#semester 2 data
secondSemester=allData.loc[allData['TermNo'] == 2]
#secondGPA = pd.DataFrame(secondSemester, columns=["SubjectID","Term GPA"])
semesterTwo= pd.merge(secondSemester, GPA1, on='SubjectID')



#semseter 3 data
thirdSemester=allData.loc[allData['TermNo'] == 3]
thirdGPA = pd.DataFrame(thirdSemester, columns=["SubjectID","Term GPA"])
thirdGPA.columns =["SubjectID","GPA 3"]
prevSemesters = pd.merge(GPA1,GPA2, on='SubjectID')
semesterThree = pd.merge(thirdSemester , prevSemesters, on='SubjectID')

#print(allData)
#print(firstSemester)
#print(firstSemester.columns.values.tolist())
print(thirdGPA.columns.values.tolist())




#linReg semester one

import statsmodels.api as sm
y = pd.DataFrame(firstSemester, columns=["Term GPA"])

X = pd.DataFrame(firstSemester, columns=["LowSAT", "MidSAT", "HighSAT", "LowACT", "MidACT", "HighACT", "RaceWhite", "RaceBlack", "RaceHispanic", "RaceAsian", "Foreign Student", "HUMS", "ENGN", "SOCS", "NATS"])

X = sm.add_constant(X)
modelOne = sm.OLS(y, X).fit()
predictions = modelOne.predict(X)
print(modelOne.summary())
print(predictions)

#linReg semester two
y2 = pd.DataFrame(semesterTwo, columns=["Term GPA"])
X2 = pd.DataFrame(semesterTwo, columns=["GPA 1","LowSAT", "MidSAT", "HighSAT", "LowACT", "MidACT", "HighACT", "RaceWhite", "RaceBlack", "RaceHispanic", "RaceAsian", "Foreign Student", "HUMS", "ENGN", "SOCS", "NATS"])

X2 = sm.add_constant(X2)
modelTwo = sm.OLS(y2, X2).fit()
predictions2 = modelTwo.predict(X2)
print(modelTwo.summary())
print(predictions2)

#linReg semester three

y3 = pd.DataFrame(semesterThree, columns=["Term GPA"])
X3 = pd.DataFrame(semesterThree, columns=["GPA 1","GPA 2","LowSAT", "MidSAT", "HighSAT", "LowACT", "MidACT", "HighACT", "RaceWhite", "RaceBlack", "RaceHispanic", "RaceAsian", "Foreign Student", "HUMS", "ENGN", "SOCS", "NATS"])

X3 = sm.add_constant(X3)
modelThree = sm.OLS(y3, X3).fit()
predictions3 = modelThree.predict(X3)
print(modelThree.summary())
print(predictions3)

#dataFrame of all the predictions (series to df)
pred1=pd.Series.to_frame(predictions)
pred2=pd.Series.to_frame(predictions2)
pred3=pd.Series.to_frame(predictions3)
pred1.columns = ["GPA 1 pred"]
pred2.columns = ["GPA 2 pred"]
pred3.columns = ["GPA 3 pred"]

pred1['Pred P 1']=0
pred2['Pred P 2']=0
pred3['Pred P 3']=0
pred1.loc[ (pred1['GPA 1 pred'] < 2.0), 'Pred P 1' ] = 1
pred2.loc[ (pred2['GPA 2 pred'] < 2.0), 'Pred P 2' ] = 1
pred3.loc[ (pred3['GPA 3 pred'] < 2.0), 'Pred P 3' ] = 1

#dataFrame of all actual results
actual1= pd.DataFrame(semesterThree, columns=["SubjectID","GPA 1"])
actual2=pd.DataFrame(semesterThree, columns=["SubjectID","GPA 2"])
actual3=pd.DataFrame(semesterThree, columns=["SubjectID","Term GPA"])

actual1['Real P 1'] = 0
actual2['Real P 2'] = 0
actual3['Real P 3'] = 0

actual1.loc[ (actual1['GPA 1'] < 2.0), 'Real P 1' ] = 1
actual2.loc[ (actual2['GPA 2'] < 2.0), 'Real P 2' ] = 1
actual3.loc[ (actual3['Term GPA'] < 2.0), 'Real P 3' ] = 1



#confusion matrix maker
import sklearn.metrics

a = sklearn.metrics.confusion_matrix(actual1["Real P 1"],pred1["Pred P 1"])
b = sklearn.metrics.confusion_matrix(actual2["Real P 2"], pred2["Pred P 2"])
c =  sklearn.metrics.confusion_matrix(actual3["Real P 3"], pred3["Pred P 3"])
print(a)
print(b)
print(c)

#confusion matrix with graphics
#note that the values for graphics were manually inserted
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
multiclassOne=np.array([[729,16],[36,26]])
multiclassTwo=np.array([[745,0],[3,59]])
multiclassThree=np.array([[768,3],[36,0]])

fig, ax = plot_confusion_matrix(conf_mat=multiclassOne,
                                colorbar=True,
                                show_absolute=False,
                                show_normed=True)
plt.show()
fig, ax = plot_confusion_matrix(conf_mat=multiclassTwo,
                                colorbar=True,
                                show_absolute=False,
                                show_normed=True)
plt.show()
fig, ax = plot_confusion_matrix(conf_mat=multiclassThree,
                                colorbar=True,
                                show_absolute=False,
                                show_normed=True)
plt.show()

