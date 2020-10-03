import numpy as np
import pandas as pd
import pickle
import os
import argparse
import plotly.plotly as py
import plotly.graph_objs as go
import collections
import csv
import math

class Explor():

    def __init__(self, terms, courses, demograph):
        self.terms = terms
        self.courses = courses
        self.demograph = demograph

    def Prob_Majors(self):
        # Exploratory Analysis -- Probation and Majors
        Probed_Students = self.demograph[self.demograph['probation'] != 0]
        Major_Population = self.demograph.groupby('B - Major1 Code')['B - Major1 Code'].count()
        Major_Probation = Probed_Students.groupby('B - Major1 Code')['B - Major1 Code'].count()
        Hajim_Majors = ['BME', 'CHE', 'CSC','CSA', 'ECE', 'IDE', 'ES', 'ME', 'OPT']
        with open('./Saved Models/Major_Probation.csv', 'w') as f:
            f.write('Major' + ' ' + 'Percentage' + ' ' + 'Aboslute_Number\n')
            for name in Major_Probation.index:
                out = name + ' ' + (Major_Probation[name]/Major_Population[name]).astype(str) + ' ' + Major_Probation[name].astype(str)
                f.write("%s\n" % out)

        Hajim_Prob = Major_Probation[Hajim_Majors]
        Hajim_Popu = Major_Population[Hajim_Majors]
        with open('./Saved Models/Hajim_Probation.csv', 'w') as f:
            f.write('Major' + ' ' + 'Percentage' + ' ' + 'Aboslute_Number\n')
            for name in Hajim_Prob.index:
                out = name + ' ' + (Hajim_Prob[name]/Hajim_Popu[name]).astype(str) + ' ' + Hajim_Prob[name].astype(str)
                f.write("%s\n" % out)
        print('Average probation rate for Hajim school is ' + (Hajim_Prob.sum()/Hajim_Popu.sum()).astype(str))
        print('Average probation rate in general is ' + str(Probed_Students['SubjectID'].nunique()/courses['SubjectID'].nunique()))

    def Changing_Majors(self):
        def changed_major(ID):
            Course_Data = self.courses[self.courses['SubjectID'] == ID]['Ps1 Major1 Code']
            original_major = Course_Data.iloc[0]
            ended_major = Course_Data.iloc[-1]
            if original_major == 'UNC':
                return True
            return not original_major == ended_major

        def find_grades(ID, changed):
            Term_Data = self.terms[self.terms['SubjectID'] == ID]['Term GPA'].tolist()
            if not changed:
                pre_1, pre_2, aft_1, aft_2 = np.NaN, np.NaN, np.NaN, np.NaN
            else:
                pre_1, pre_2, aft_1, aft_2 = np.NaN, np.NaN, np.NaN, np.NaN
            for i in range(0, len(Term_Data)):
                if Term_Data[i] < 2.0 and not Term_Data[i] == 0:
                    if i-1 >= 0:
                        if Term_Data[i-1] > 3.3:
                            break
                        pre_1 = Term_Data[i-1]
                    if i-2 >= 0:
                        pre_2 = Term_Data[i-2]
                    for j in range(i, len(Term_Data)):
                        if Term_Data[j] >= 2.0 and Term_Data[j] < 3.5:
                            aft_1 = Term_Data[j]
                            break
                    for j in range(i, len(Term_Data)-1):
                        if Term_Data[j] >= 2.0 and Term_Data[j] < 3.5:
                            aft_2 = Term_Data[j+1]
                            break
                    break
            return pd.DataFrame([[pre_1, pre_2, aft_1, aft_2]], columns=['pre_1', 'pre_2', 'aft_1', 'aft_2'])

        GPA_Changed = pd.DataFrame(columns=['pre_1', 'pre_2', 'aft_1', 'aft_2'])
        GPA_Unchanged = pd.DataFrame(columns=['pre_1', 'pre_2', 'aft_1', 'aft_2'])
        for ID in self.courses[self.courses['Ps1 Acad Standing Desc'] == 'PROBATION']['SubjectID'].unique()[:-1]:
            if changed_major(ID):
                GPA_Changed = GPA_Changed.append(find_grades(ID, True), ignore_index=True)
            else:
                GPA_Unchanged = GPA_Unchanged.append(find_grades(ID, False), ignore_index=True)
        GPA_Unchanged.fillna(value=GPA_Changed.mean(), inplace=True)
        GPA_Changed.fillna(value=GPA_Changed.mean(), inplace=True)
        print(GPA_Unchanged.shape)
        print(GPA_Changed.shape)
        def graph_changing(GPA_Changed, GPA_Unchanged):
            data = [
                    go.Scatter(
                               y=GPA_Unchanged.mean(), # assign x as the dataframe column 'x'
                               x=GPA_Unchanged.mean().index,
                               fill= None,
                               line = dict(shape='spline'),
                               name = 'Unchanged'
                               ),
                    go.Scatter(
                               y=GPA_Changed.mean(), # assign x as the dataframe column 'x'
                               x=GPA_Changed.mean().index,
                               fill='tonexty',
                               line = dict(shape='spline'),
                               name = 'Changed'
                               )
                    ]
            url = py.plot(data)
            return

        graph_changing(GPA_Changed, GPA_Unchanged)

    def Heatmap(self):
        # Exploratory Analysis -- Heatmap
        Heatmap_List = self.demograph[demograph['probation'] > 0]
        Heatmap_List = Heatmap_List.groupby('HS State Prov')['HS State Prov'].count()
        Heatmap_Total = self.demograph.groupby('HS State Prov')['HS State Prov'].count()
        General_Demo = self.demograph.groupby('HS State Prov')['HS State Prov'].count()
        with open('./Saved Models/heatmap.csv', 'w') as f:
            f.write('State'+' '+'Percentage'+' '+'Aboslute\n')
            for i in Heatmap_List.index:
                out = i+' '+(Heatmap_List[i]/Heatmap_Total[i]*100).astype(str)+' '+Heatmap_List[i].astype(str)
                f.write("%s\n" % out)
        with open('./Saved Models/general_demo.csv', 'w') as f:
            for i in General_Demo.index:
                out = i + ' ' + General_Demo[i].astype(str)
                f.write("%s\n" % out)

    def Sankey(self):
        prob_students = self.courses[self.courses['Ps1 Acad Standing Desc']=='PROBATION']['SubjectID']
        print(prob_students.shape)
        major_to_disp = collections.defaultdict(str)
        write_dic = collections.defaultdict(list)
        major_disp_series = self.demograph[['Degree Major1 Discipline Code', 'Degree Major1 Code']]
        for i, row in major_disp_series.iterrows():
            disp, major = row[0], row[1]
            if isinstance(disp, str):
                major_to_disp[major] = disp
        for id in prob_students:
            student_info = self.courses[self.courses['SubjectID']==id]
            for i, row in student_info.iterrows():
                if row['Ps1 Acad Standing Desc'] == 'PROBATION':
                    write_dic[id].append(major_to_disp[student_info.at[i, 'Ps1 Major1 Code']])
                    i += 1
                    while i <= student_info.shape[0]:
                        if student_info.at[i, 'Ps1 Major1 Code'] != 'PROBATION' or i == student_info.shape[0]:
                            write_dic[id].append(major_to_disp[student_info.at[i, 'Ps1 Major1 Code']])
                            if i == student_info.shape[0]:
                                write_dic[id].append('FAILED')
                            else:
                                write_dic[id].append(major_to_disp[student_info.at[student_info.shape[0], 'Ps1 Major1 Code']])
                            break
                        i += 1
                    break
        with open('./Saved Models/Sankey.csv', 'w', newline="") as f:
            writer = csv.writer(f)
            for k,v in write_dic.items():
                writer.writerow([k, v])

    def analysis(self):
        self.Sankey()
