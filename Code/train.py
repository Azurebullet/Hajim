import os
import numpy as np
import pandas as pd
import pickle
import re
import string
import math
import surprise
import collections
import time

class Train():

    def __init__(self, courses):
        self.courses = courses
        self.courses["Course Name"] = self.courses["Parent Subject Code"].map(str) + self.courses["Parent Course No"]
        cname = self.courses["Course Name"].unique().tolist()[:-1] # drop the last nan entry
        self.convert = dict([(y,x+1) for x,y in enumerate(sorted(cname))])
        self.invert = dict([[v,k] for k,v in self.convert.items()])

    def init_training_set(self, demograph):
        # generate the training set
        course_index = -1
        grade_index = 25
        current_year_index = 2
        class_year_index = 10
        year_pattern = re.compile("^[0-9]+$")
        train_count = 0
        test_count = 0
        training_dic = {}
        testing_dic = {}

        for students in self.courses.itertuples():
            if not math.isnan(students[current_year_index]):
                class_year = students[class_year_index]
                if year_pattern.match(class_year):
                    ID = students[1]
                    grade = students[grade_index]
                    course = students[course_index]
                    if grade != 0.0 and not math.isnan(grade) and not course == np.NaN:
                        training_dic[train_count] = {"SubjectID": ID, "Course": self.convert[course], "Grade": grade}
                        train_count += 1

        Training_DF = pd.DataFrame.from_dict(training_dic, "index")
        Training_DF = Training_DF.groupby(['SubjectID']).filter(lambda x: len(x) >= 4)
        print('Data loaded. Now exporting to csv.')
        Training_DF.to_csv('./Data/Spark_Training.csv', index=False)


    def train_model(self):
        # main training component
        def get_top_n(predictions, n=10):
            # get prediction results
            top_n = collections.defaultdict(list)
            for uid, iid, true_r, est, _ in predictions:
                top_n[uid].append((iid, est))

            for uid, user_ratings in top_n.items():
                user_ratings.sort(key=lambda x: x[1], reverse=True)
                top_n[uid] = user_ratings[:30]

            return top_n

        R = pd.read_csv('./Data/Spark_Training.csv')
        reader = surprise.Reader(rating_scale=(0.0, 4.0))
        data = surprise.Dataset.load_from_df(R, reader)
        algo = surprise.SVDpp(lr_all=0.001, n_factors=100, n_epochs=20, reg_all=0.1)
        trainset = data.build_full_trainset()
        testset = trainset.build_anti_testset()
        print('Training started. Depends on your machine, this process may take more than an hour')
        algo.fit(trainset)
        # cross validation
        output = surprise.model_selection.cross_validate(algo, data, verbose=True, n_jobs=-2, cv=3, measures=['rmse', 'mae','fcp'])
        predictions = algo.test(testset)
        dump_pred = get_top_n(predictions, n=30)
        with open('./Saved Models/test_pred.pkl', 'wb') as f:
            pickle.dump(dump_pred, f, protocol=pickle.HIGHEST_PROTOCOL)
            # save the predictions to pkl

    def look_student(self, studentID, n=8):
        # look at the prediction results given student ID
        with open('./Saved Models/test_pred.pkl', 'rb') as f:
            pred = pickle.load(f)
        rec_courses = pred[studentID]

        def truncate(n, decimals=0):
            # keep 2 decimal places
            multiplier = 10 ** decimals
            return int(n * multiplier) / multiplier

        counter = 0
        for course, grade in rec_courses:
            if counter == n:
                break
            if self.invert[course][:3] != 'MUR' and self.invert[course][:3] != 'MUE':
                print(self.invert[course], truncate(grade, 2))
                counter += 1
