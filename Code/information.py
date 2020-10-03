import numpy as np
import pandas as pd
import sys
import pickle
import os

import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
sns.set()


class Information():
    def __init__(self, terms, courses, demograph, graph, studentID, gender, country, ethnic, termsorder, year, course, probation, value):
        self.terms = terms
        self.courses = courses
        self.demograph = demograph
        self.studentID = studentID

        if gender is None:
            self.gender = 'None'
        else:
            self.gender = gender

        if country is None:
            self.country = 'None'
        else:
            self.country = country

        if ethnic is None:
            self.ethnic = 'None'
        else:
            self.ethnic = ethnic
        self.termsorder = termsorder  # if args.train:
#     # train = Train(pd.read_pickle('./Saved Models/Dataframes/courses.pkl'))
#     train.init(pd.read_pickle('./Saved Models/Dataframes/demograph.pkl'))
#     train.surprise_train()
        if studentID is not None:
            studentID = float(studentID)
            # print(studentID)
            student_year = terms[(terms.SubjectID == studentID)
                                & (terms.termsorder == termsorder)]
            student_year = student_year[['SubjectID', 'Year Term ID']]

            student = student_year.iloc[0]['SubjectID']
            find_year = student_year.iloc[0]['Year Term ID']
            major_find = courses[(courses['SubjectID'] == student) & (
                courses['Year Term ID'] == find_year)]
            # major=courses[(courses['SubjectID']==studentID)&(courses['Year Term ID']==student_year['Year Term ID'])]['Ps1 Major1 Code']
            # print(major_find)
            major = major_find['Ps1 Major1 Code'].tolist()[0]
            self.major = major
        else:
            self.major=None
        self.graph = graph

        if year is None:
            self.year = 'None'
        else:
            self.year = year
        self.course = course

        if probation is None:
            self.probation = 'None'
        else:
            self.probation = probation
        self.value = value

    def information(self):
        # print("I am here")

        # print(result)
        if(self.graph == "student"):
            student_list = self.terms['SubjectID'].tolist()
            student_list = list(dict.fromkeys(student_list))
            # terms=pd.merge(current_terms,current_courses[['SubjectID','Year Term ID','Ps1 Major1 Code','Ps1 Major2 Code']],how='inner')
            # print(terms.keys())
            similar_student = []
            probation_student = self.terms[self.terms['probation'] == 1]
            probation_number_get = probation_student['termsorder'].tolist()

            # print(probation_number_get)
            import collections

            counter = collections.Counter(probation_number_get)
            # print(counter.keys())
            # print(counter.values())
            # probation_number_get.to_csv(
                # './Information/probation_frequency.csv', sep='\t', encoding='utf-8')
            # print(student_list)
            for i in student_list:
                studentinfo = self.terms.loc[self.terms['SubjectID'] == i]
                if(self.majortest(i) & self.probationtest(studentinfo)):
                    similar_student.append(i)
                    # 2
            # print(similar_student)
            outputcourse = self.findcourses(similar_student, int(self.termsorder))
            # print(outputcourse)
            import collections
            # counter=collections.Counter(outputcourse)
            # print(outputcourse)
            grade_list = outputcourse.groupby('Course Name', as_index=False)[
                'Grade Value'].mean()
            print(outputcourse.dtypes)
            sd_list=outputcourse.groupby('Course Name').std()
            sd_list.rename(columns={'Grade Value': 'SD'
                                        },
                            inplace=True)

            grade_list['SD']=sd_list['SD'].tolist()
 
            course_list = outputcourse['Course Name'].tolist()
            counter = collections.Counter(course_list)
            # print(counter)
            top_8 = counter.most_common(8)
            # print(top_5)
            top_8_list = [i[0] for i in top_8]
            # # print(top_5_list)
            top_8_score = pd.DataFrame(
                columns=['Course Name', 'Grade Value', 'Frequency','SD'])
            for i in top_8_list:
                test = grade_list.loc[grade_list['Course Name'] == i, [
                    'Course Name','Grade Value','SD']]
                frame = [top_8_score, test]
                top_8_score = pd.concat(frame,sort=True)
            top_8_frequency = [i[1] for i in top_8]
            top_8_score['Frequency'] = top_8_frequency

            top_8_score.rename(columns={'Grade Value': 'Mean Grade Value'
                                        },
                            inplace=True)
            print(top_8_score)
            top_8_score.to_csv(
                'Saved Models/Information/recommend_courses.csv', sep='\t', encoding='utf-8')

            sns.set(style="whitegrid")

            ax = sns.barplot(x="Course Name", y="Frequency",
                             palette="Blues_d", data=top_8_score)
            score = top_8_score['Mean Grade Value'].tolist()
            freq = top_8_score['Frequency'].tolist()
            sd=top_8_score['SD'].tolist()
            plt.rcParams.update({'font.size': 7})
            distance = freq[0]/10
            plt.annotate('( '+str(round(score[0], 2))+','+str(round(sd[0], 2))+' )', xy=(0, freq[0]),
                         xytext=(0, freq[0]+distance), ha='center',
                         bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                               'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                         arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                     'alpha': 0.6, 'color': 'orange'})
            plt.annotate('( '+str(round(score[1], 2))+','+str(round(sd[1], 2))+' )', xy=(1, freq[1]),
                         xytext=(1, freq[1]+distance), ha='center',
                         bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                               'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                         arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                     'alpha': 0.6, 'color': 'orange'})
            plt.annotate('( '+str(round(score[2], 2))+','+str(round(sd[2], 2))+' )', xy=(2, freq[2]),
                         xytext=(2, freq[2]+distance), ha='center',
                         bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                               'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                         arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                     'alpha': 0.6, 'color': 'orange'})
            plt.annotate('( '+str(round(score[3], 2))+','+str(round(sd[3], 2))+' )', xy=(3, freq[3]),
                         xytext=(3, freq[3]+distance), ha='center',
                         bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                               'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                         arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                     'alpha': 0.6, 'color': 'orange'})
            plt.annotate('( '+str(round(score[4], 2))+','+str(round(sd[4], 2))+' )', xy=(4, freq[4]),
                         xytext=(4, freq[4]+distance), ha='center',
                         bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                               'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                         arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                     'alpha': 0.6, 'color': 'orange'})
            plt.annotate('( '+str(round(score[5], 2))+','+str(round(sd[5], 2))+' )', xy=(5, freq[5]),
                         xytext=(5, freq[5]+distance), ha='center',
                         bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                               'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                         arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                     'alpha': 0.6, 'color': 'orange'})
            plt.annotate('( '+str(round(score[6], 2))+','+str(round(sd[6], 2))+' )', xy=(6, freq[6]),
                         xytext=(6, freq[6]+distance), ha='center',
                         bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                               'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                         arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                     'alpha': 0.6, 'color': 'orange'})
            plt.annotate('( '+str(round(score[7], 2))+','+str(round(sd[7], 2))+' )', xy=(7, freq[7]),
                         xytext=(7, freq[7]+distance), ha='center',
                         bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                               'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                         arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                     'alpha': 0.6, 'color': 'orange'})

            plt.annotate("The number in the yellow label is the mean grade and standard deviation", xy=(4, freq[6]),
                         xytext=(4, freq[0]), ha='center',
                         bbox={'boxstyle': 'square', 'pad': 0.5, 'facecolor':
                               'green', 'edgecolor': 'green', 'alpha': 0.6}
                         )
            plt.show()
            fig = ax.get_figure()
            fig.savefig('Saved Models/Information/recommend_course.png')
        # g = plt.figure(2)
        # FILTER DATA
        if(self.graph == 'course'):

            current_terms = self.terms
            if(self.probation != 'None'):
                current_terms = self.probationfilter(
                    current_terms, self.probation)
            if(self.country != 'None'):
                current_terms = self.countryfilter(current_terms, self.country)
            if(self.gender != 'None'):
                current_terms = self.genderfilter(current_terms, self.gender)
            if(self.year != 'None'):
                # print(self.demograph['year'].tolist())
                current_terms = self.yearfilter(current_terms, self.year)
            if(self.ethnic != 'None'):
                current_terms = self.ethnicfilter(current_terms, self.ethnic)
            # print(current_terms.shape)
            if(current_terms.shape[0]> 0):
                graph2_student_list = current_terms['SubjectID']
                course_data = self.demograph[self.demograph['SubjectID'].isin(
                    graph2_student_list)]
                discp_list = ['ENGN', 'HUMS', 'SOCS', 'NATS']
                # student_graph_data = pd.DataFrame(
                #     columns=['SubjectID', 'Year Term ID','Term GPA', 'Degree Major1 Discipline Code'])
                # print(similar_data.columns)
                student_graph_data = current_terms[[
                    'SubjectID', 'Term GPA', 'termsorder', 'Degree Major1 Discipline Code']]
                # student_graph_data = student_graph_data[student_graph_data['termsorder']
                #                                         == self.termsorder+1]
                student_graph_data = student_graph_data[student_graph_data['Degree Major1 Discipline Code'].isin(
                    discp_list)]
                # print(student_graph_data)
                # for i in discp_list:
                student_grade_list = student_graph_data.groupby('Degree Major1 Discipline Code', as_index=False)[
                    'Term GPA'].mean()
                if 'ENGN' not in student_grade_list['Degree Major1 Discipline Code']:
                    df2 = pd.DataFrame({"Degree Major1 Discipline Code": ['ENGN'],
                                        "Term GPA": [0.0]})
                    student_grade_list = student_grade_list.append(df2)
                # print(student_grade_list)
                input = self.courses[self.courses['SubjectID'].isin(
                    graph2_student_list)]
                # print(input)
                output = self.disc_course(input)
                print(output)
                output.to_csv('Saved Models/Information/disc_performances_.csv', sep='\t', encoding='utf-8')
                if self.value == 'SD':
                    labels = output.index.values
                    grades = output['Grade Value'].tolist()
                    d = {'Degree Major1 Discipline Code': labels, 'Mean Grade': grades}
                    sns.set(style="whitegrid", font_scale=0.7)
                    ax = sns.barplot(x="Degree Major1 Discipline Code", y="Mean Grade",
                                    palette="pastel", data=d)
                    score = output['Grade Value'].tolist()
                    freq = output['SD'].tolist()
                    mean = output['frequency'].tolist()
                else:
                    labels = output.index.values
                    grades = output['Grade Value'].tolist()
                    d = {'Degree Major1 Discipline Code': labels, 'Mean Grade': grades}
                    sns.set(style="whitegrid", font_scale=0.7)
                    ax = sns.barplot(x="Degree Major1 Discipline Code", y="Mean Grade",
                                    palette="pastel", data=d)
                    score = output['Grade Value'].tolist()
                    freq = output['frequency'].tolist()
                plt.rcParams.update({'font.size': 7})
                distance = score[0]/15
                plt.annotate('( '+str(round(mean[0], 2))+','+str(round(freq[0], 2))+' )', xy=(0, score[0]),
                            xytext=(0, score[0]+distance), ha='center',
                            bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                                'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                            arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                        'alpha': 0.6, 'color': 'orange'})
                plt.annotate('( '+str(round(mean[1], 2))+','+str(round(freq[1], 2))+' )',xy=(1, score[1]),
                            xytext=(1, score[1]+distance), ha='center',
                            bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                                'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                            arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                        'alpha': 0.6, 'color': 'orange'})
                plt.annotate('( '+str(round(mean[2], 2))+','+str(round(freq[2], 2))+' )', xy=(2, score[2]),
                            xytext=(2, score[2]+distance), ha='center',
                            bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                                'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                            arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                        'alpha': 0.6, 'color': 'orange'})
                plt.annotate('( '+str(round(mean[3], 2))+','+str(round(freq[3], 2))+' )', xy=(3, score[3]),
                            xytext=(3, score[3]+distance), ha='center',
                            bbox={'boxstyle': 'round', 'pad': 0.5, 'facecolor':
                                'orange', 'edgecolor': 'orange', 'alpha': 0.6},
                            arrowprops={'arrowstyle': "wedge,tail_width=0.5",
                                        'alpha': 0.6, 'color': 'orange'})
                # plt.annotate("The number in the yellow label is the frequency with filter probation "+self.probation+",year"+self.year+" ,country"+self.country+" ,gender"+self.gender, xy=(1.5, 0.5),
                #             xytext=(1.5, 0.5), ha='center',
                #             bbox={'boxstyle': 'square', 'pad': 0.5, 'facecolor':
                #                'green', 'edgecolor': 'green', 'alpha': 0.6}
                #             )

                title = "The course performance for students of different Discipline of "+self.course
                if self.value == 'SD':
                    if self.year !='None':
                        plt.xlabel("The number in the yellow label is the Frequency and SD with filter probation:"+self.probation +
                               ", ethnic: "+self.ethnic+", year: "+self.year[0]+'~'+self.year[-1]+", country: "+self.country+", gender:"+self.gender)
                        plt.ylabel("Mean Grade")                    
                    else:
                        plt.xlabel("The number in the yellow label is the Frequency and SD with filter probation:"+self.probation +
                               ", ethnic: "+self.ethnic+", year:None"+", country: "+self.country+", gender:"+self.gender)
                        plt.ylabel("Mean Grade")
                else:
                    plt.xlabel("The number in the yellow label is the frequency with filter probation:"+self.probation +
                               ", ethnic: "+self.ethnic+", year: "+self.year+", country: "+self.country+", gender:"+self.gender)
                plt.title(title, pad=20, fontsize=11)
                plt.show()
                fig = ax.get_figure()
                fig.savefig(
                    'Saved Models/Information/disc_performance_.png')
            else:
                print('The rows of data is not enough after being filtered,please use less filters')

    def genderfilter(self, input, gender):
        mDemograph = self.demograph
        mDemograph = mDemograph.loc[mDemograph['Gender'] == gender]
        candidate_list = mDemograph['SubjectID'].tolist()
        output = input[input['SubjectID'].isin(candidate_list)]
        return output

    def countryfilter(self, input, country):
        mDemograph = self.demograph
        mDemograph = mDemograph.loc[mDemograph['Citizen Country Name'] == country]
        candidate_list = mDemograph['SubjectID'].tolist()
        output = input[input['SubjectID'].isin(candidate_list)]
        return output

    def ethnicfilter(self, input, ethnic):
        mDemograph = self.demograph
        mDemograph = mDemograph.loc[mDemograph['2010 IPEDS Ethnicity Description'] == ethnic]
        candidate_list = mDemograph['SubjectID'].tolist()
        output = input[input['SubjectID'].isin(candidate_list)]
        return output

    def yearfilter(self, input, year_list):
        mDemograph = self.demograph
        # print(year_list)
        [float(i) for i in year_list]
        mDemograph = mDemograph[mDemograph['year'].isin(year_list)]
        candidate_list = mDemograph['SubjectID'].tolist()
        output = input[input['SubjectID'].isin(candidate_list)]
        return output

    def disc_course(self, input):
        # print(input)
        student_taken = input[(
            input['Course Name'] == self.course)]
        # print(student_taken)
        current = student_taken[['SubjectID',
                                 'Course Name', 'Grade Value']].copy()
        current = current.drop_duplicates(subset='SubjectID', keep="last")
        # print(current)
        discp_list = ['ENGN', 'HUMS', 'SOCS', 'NATS']
        current_demograph = self.demograph[self.demograph['Degree Major1 Discipline Code'].isin(
            discp_list)]
        demograph_for_use = current_demograph[[
            'SubjectID', 'Degree Major1 Discipline Code']].copy()
        demograph_for_use = demograph_for_use.dropna()
        # print(demograph_for_use)
        current = pd.merge(current, demograph_for_use, how='inner')
        # print(current.keys())
        # print(current)
        current = current[[
            'Degree Major1 Discipline Code', 'Grade Value']].copy()
        # frequency=[i[1] for i in current['Degree Major1 Discipline Code'].tolist()]
        3
        # output = current.groupby('Degree Major1 Discipline Code').mean()
        frequency = current.groupby('Degree Major1 Discipline Code').count()
        _list = frequency['Grade Value'].tolist()
        # print(_list)
        output = current.groupby('Degree Major1 Discipline Code').mean()
        output['frequency'] = _list
        output['SD'] = current.groupby('Degree Major1 Discipline Code').std()
        if output.index.size < len(discp_list):
            required_list = list(set(discp_list)-set(output.index.tolist()))
            for i in required_list:
                output.loc[i] = [0.0, 0.0]
        return output

    def majortest(self, student):
        temp1 = self.courses[self.courses['SubjectID'] == student][['Ps1 Major1 Code', 'Ps1 Major2 Code']]
        major1 = temp1['Ps1 Major1 Code'].tolist()
        major1 = list(dict.fromkeys(major1))
        major2 = temp1['Ps1 Major2 Code'].tolist()
        major2 = list(dict.fromkeys(major2))
        result, check1, check2 = 1, 1, 1
        if self.major in major1:
            check1 = 0
        if self.major in major2:
            check2 = 0
        result = check1*check2
        if(result == 0):
            return True
        return False



    def probationtest(self, studentinfo):
        probationlist = studentinfo['probation'].tolist()
        if 0 in probationlist:
            return True
        return False
    def probationfilter(self, input, probation_status):
        probationlist = input['probation'].tolist()

        if probation_status == 'yes':
            output= input[input['probation'] == 1]
        if probation_status == 'no':
            output= input[input['probation'] == 0]
        return output

    def findcourses(self, student_list, termsorder):
        course_out = pd.DataFrame(columns=['Course Name', 'Grade Value'])
        outterms = termsorder+1
        # print(outterms)
        for i in student_list:
            # print(self.terms[self.terms['SubjectID'] == i])
            currentterms = self.terms[(self.terms['SubjectID'] == i) & (
                self.terms['termsorder'] == outterms)]
            # currentterms.reset_index()
            year_list = currentterms['Year Term ID'].tolist()
            # print(year_list)
            if year_list:
                year_term_id = year_list[0]
                needcourses = self.courses[(self.courses['SubjectID'] == i) & (
                    self.courses['Year Term ID'] == year_term_id)]
                # print(needcourses.keys())
                current = needcourses[['Course Name', 'Grade Value']].copy()
                # print(course_out)
                # print(current)
                frames = [course_out, current]
                course_out = pd.concat(frames)
        return course_out
