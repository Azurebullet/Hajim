import numpy as np
import pandas as pd
import sys
import pickle
import os

class Init():

    def readData(self):
        terms = pd.read_csv('../Data/DSC_3TermData_030819.csv', low_memory=False)
        courses = pd.read_csv('../Data/DSC_2CourseData_030819.csv', low_memory=False)
        demograph = pd.read_csv('../Data/DSC_1Demographic_030819.csv', low_memory=False)
        return terms, courses, demograph

    def preprocess(self):
        terms, courses, demograph = self.readData()
        termsinformation=terms
        termsinformation['probation']=0
        for i in courses.itertuples():
            if i[-1] == "PROBATION":
                termsinformation.at[i.Index, 'probation'] = 1
        termsinformation['termsorder']=0
        student_list=termsinformation['SubjectID'].unique()
        for i in student_list:
            order = 0
            temp = termsinformation[termsinformation['SubjectID'] == i]
            for index, row in temp.iterrows():
                order += 1
                termsinformation.at[index, 'termsorder'] = order

        # Save to pkl for future use
        if not os.path.exists('../Saved Models/Dataframes'):
            os.makedirs('../Saved Models/Dataframes')
        terms.to_pickle('../Saved Models/Dataframes/terms.pkl')
        courses.to_pickle('../Saved Models/Dataframes/courses.pkl')
        demograph.to_pickle('../Saved Models/Dataframes/demograph.pkl')
        termsinformation.to_pickle('../Saved Models/Dataframes/terms_in.pkl')
        #feature_matrix.to_pickle('./Saved Models/features.pkl')
        return terms, courses, demograph,termsinformation
