
import numpy as np
import pandas as pd
import featuretools as ft
from io import StringIO
import sys
import pickle
import os
import argparse
from initialize import Init
from train import Train
from information import Information
from exploratory import Explor
import linearregression


# initialize the program
parser = argparse.ArgumentParser(
    description="2019 SS 383W Capstone Project: Hajim 2")
parser.add_argument("--init", help="initilize the program",
                    action='store_true', default=False)
parser.add_argument("--explor", help="perform exploratory analysis",
                    action='store_true', default=False)
parser.add_argument("--train", help="perform exploratory analysis",
                    action='store_true', default=False)
parser.add_argument("--linreg", help="perform linear regression model",
                    action='store_true', default=False)
parser.add_argument("--student", help="type in the studnet ID",
                    type=int, default=None)
parser.add_argument("--graph", type=str,
                    help="you want to look at student graph or course graph?",
                    choices=['student', 'course'])
parser.add_argument("--year-filter", type=int, nargs='+',
                    help="set the year filter(format: start_year end_year)",
                    default=None)
parser.add_argument("--gender-filter", type=str, choices=["F", "M"],
                    help="set the gender filter", default=None)
parser.add_argument("--country-filter", type=str, default=None,
                    help="values in the country column of demograph.xls")
parser.add_argument("--ethnic-filter", type=str, default=None,
                    help="values in the ethnic column of demograph.xls")
parser.add_argument("--current-term", type=int, default=3,
                    help="please specify the current term of this student\
                     (format: 1 or 2 or 3 or ...)")
parser.add_argument("--course-number", type=str, default=None)
parser.add_argument("--probation-filter", type=str, default=None,
                    help="type 'yes' to just look at probation students")
parser.add_argument("--num_of_rec_courses", type=int, default=8,
                    help="the number of total recommended courses, range from 1-20")

args = parser.parse_args()

if args.init:
    init = Init()
    terms, courses, demograph, termsinformation = init.preprocess()


if args.explor:
    terms = pd.read_pickle('Saved Models/Dataframes/terms_in.pkl')
    courses = pd.read_pickle('Saved Models/Dataframes/courses.pkl')
    demograph = pd.read_pickle('Saved Models/Dataframes/demograph.pkl')
    explor = Explor(terms, courses, demograph)
    explor.analysis()

if args.train:
    train = Train(pd.read_pickle('Saved Models/Dataframes/courses.pkl'))
    train.init_training_set(pd.read_pickle('Saved Models/Dataframes/demograph.pkl'))
    train.train_model()

if args.linreg:
    os.system('python linearregression.py')

if args.graph == 'student':
    terms = pd.read_pickle('Saved Models/Dataframes/terms_in.pkl')
    courses = pd.read_pickle('Saved Models/Dataframes/courses.pkl')
    demograph = pd.read_pickle('Saved Models/Dataframes/demograph.pkl')
    if not os.path.exists('Saved Models/Information/'):
        dirName = 'Saved Models/Information/'
        os.makedirs(dirName)

    print('For student', args.student, 'we recommend the following courses:')
    train = Train(courses)
    train.look_student(args.student, args.num_of_rec_courses)
    courses["Course Name"] = courses["Parent Subject Code"].map(
        str)+courses["Parent Course No"]
    terms = pd.merge(
        terms, demograph[['SubjectID', 'Degree Major1 Discipline Code', ]], how='inner')
    terms = terms.drop_duplicates()
    demograph['Degree Award Date'] = pd.to_datetime(
        demograph['Degree Award Date'], errors='coerce')
    demograph['year'] = demograph['Degree Award Date'].dt.year
    dis_list = terms['Degree Major1 Discipline Code'].tolist()
    dis_list = list(dict.fromkeys(dis_list))
    if args.year_filter is not None:
        start_year, end_year = args.year_filter
        year_list = ['hi'] * (end_year-start_year)
        for i in range(start_year, end_year):
            year_list[i-start_year] = str(i)
    else:
        year_list = None
    info = Information(terms, courses, demograph, args.graph, args.student,
                       args.gender_filter, args.country_filter, args.ethnic_filter, args.current_term, year_list, args.course_number, args.probation_filter, 'SD')
    info.information()

if args.graph == 'course':
    terms = pd.read_pickle('Saved Models/Dataframes/terms_in.pkl')
    courses = pd.read_pickle('Saved Models/Dataframes/courses.pkl')
    demograph = pd.read_pickle('Saved Models/Dataframes/demograph.pkl')
    if not os.path.exists('Saved Models/Information/'):

        dirName = 'Saved Models/Information/'
        os.makedirs(dirName)

    courses["Course Name"] = courses["Parent Subject Code"].map(
        str)+courses["Parent Course No"]
    terms = pd.merge(
        terms, demograph[['SubjectID', 'Degree Major1 Discipline Code', ]], how='inner')
    terms = terms.drop_duplicates()
    demograph['Degree Award Date'] = pd.to_datetime(
        demograph['Degree Award Date'], errors='coerce')
    demograph['year'] = demograph['Degree Award Date'].dt.year
    dis_list = terms['Degree Major1 Discipline Code'].tolist()
    dis_list = list(dict.fromkeys(dis_list))
    if args.year_filter is not None:
        start_year, end_year = args.year_filter
        year_list = ['hi'] * (end_year-start_year)
        for i in range(start_year, end_year):
            year_list[i-start_year] = str(i)
    else:
        year_list = None
    info = Information(terms, courses, demograph, args.graph, args.student,
                       args.gender_filter, args.country_filter, args.ethnic_filter, args.current_term, year_list, args.course_number, args.probation_filter, 'SD')
    info.information()