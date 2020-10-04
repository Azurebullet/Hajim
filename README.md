# Capstone Hajim Team-2

### Introduction
Hi, this is the final version of this Hajim capstone project. This document will direct you on how to initiate the program, how to use it to grab useful informations, and how to update its recommendation engine for new students.
By the end of this document, you should be able to use this program to
- input a student ID, generate the recommended courses and historical supportive informations
- input a course number, see the discipline based grade distribution of the course

示例输出在graph文件夹
### Environment Settings

At the very beginning, please have your python3 programming language properly installed on your computer, and add it to your $PATH. We recommend you to install python by the free and open python distribution [Anaconda](https://www.anaconda.com/distribution/), but you can try other methods at your own preferences.

After installed, please check the successfulness of your installation by typing the following command in your terminal. For windows users, you may install the terminal-like command line interface through  [Git-SCM](https://git-scm.com/download/win).

```console
python -V
```

And it should return the installed version of your python.

### Running Instructions

To begin your first try under our given data and models, please first open the project folder.
Type the following command in terminal:

```console
cd (drag you ./code folder here)

cd ..

pip install -r requirements.txt
```
>all of the above commands can be copy and paste to your termnial, except the first cd command.
For this one, you need to type "cd " then drag the "code" folder to your termnial. And you don't need to run the last command again after the first time.

- ##### Student Information (Demo):
    We will talk about the filter settings of this function later
    ```console
    bash run_student.sh
    ```
    And you should see the recommended courses in terminal stouput and a graph of the common courses

- ##### Course Information (Demo):
    We will talk about the filter settings of this function later
    ```console
    bash run_course.sh
    ````
    And you should see a graph of the average performance of that course

### Filter Settings in Detail
- ##### Student Information:
    To change the student ID and filter settings, please open the run_student.sh file under project folder(you can do this by double clicking on most platforms). And all implemented filter settings as as shown:

    ```bash
    #!/usr/bin/env bash
    PYTHONPATH='./':$PYTHONPATH python code/capstone.py \
        --graph student \
        # Do not change the above lines
        --student 242368676 \
        # The student's SubjectID
        --current-term 3 \
        # Which term you are looking at?
        --num-of-rec-courses 10 \
        # How many courses do you want to recommend?
    ```
    Then the program will print all the recommended courses, and a graph of common courses took by probation student of the same major. To change the settings, simply change the numbers following each filters. For example, if we want to look at student 183539420, who is currently at her 3th term (so a fall semester sophomore), and generate 8 recommended courses, we shall change the 'run_student.sh' as the following:

    ```bash
    #!/usr/bin/env bash
    PYTHONPATH='./':$PYTHONPATH python code/capstone.py \
        --graph student \
        --student 183539420 \
        --current-term 3 \
        --num-of-rec-courses 8 \
    ```

    Dont forget to add the line breaking sign '\' at the end of each line! All comments are removed to fit the shell script requirements.

- ##### Course Information:
    Changing the filter settings of course information involves adding/deleting the --filter lines within the run_course.sh file. So please be careful when editing your filters.
    ```bash
    #!/usr/bin/env bash
    PYTHONPATH='./':$PYTHONPATH python code/capstone.py \
        --graph course \
        # Do not change the above lines
        --course-number MTH162 \
        # The above filters are required.
        --gender-filter F \
        # Options are 'F' or 'M', delete the entire line to deactivate this filter
        --country-filter USA \
        # Please use the countries specified in demograph excel file
        # Delete the entire line to deactivate this filter
        --ethnic-filter Black \
        # Similar opreations as the country filter
        --year-filter 2000 2010 \
        # Only look at the students from class year 2000-2010
        # Delete the entire line to deactivate this filter
        --probation-filter yes \
        # Delete this filter to look at all students
    ```
    You many delete the unwanted filters to deactivate them. For instance, now this time we want to look at the average grade in MTH162 for all male black students. So we shall change the '--gender-filter' to M, '--ethnic-filter' to Black,  delete '--probation-filter', '--year-filter', and '--country-filter'. The result run_course.sh file will look like:

    ```bash
    #!/usr/bin/env bash
    PYTHONPATH='./':$PYTHONPATH python code/capstone.py \
        --graph course \
        --course-number MTH162 \
        --ethnic-filter Black \
        --gender-filter M \
    ```
    All comments should be removed when running the shell script. And again do not forget to add the line breaking sign '\' at the end of each line.

### Update the Models
Students come and go. To make the program updated for the latest students, we need to use the '--init' and '--train' function to update the database. This process can be time consuming, so please bear with me.
At first, you need to add the updated excel files, following excatly same pattern as the ones in './Data' folder, to the './Data' folder. Then you should delete the old ones (excel files and csv files), and rename them to the same names as the original ones (I know that sounds ridiculous....).

Notice that you must use the complete students dataset, from the year you want this program to look at, to update the database. For example, deleting the old excel files, says students from 1990-2017, and only adding students data from 2018, will not update the program database to students from 1990-2018, but will only make the database to contain 2018 students data.

Secondly, here comes another redundant part. Since the excel files (formatted in xls and xlsx) will sometimes cause random error to the dataloader, one shall convert all the excel files to .csv files, and also put the .csv files into the './Data' folder. And the .csv files should have names consist with their excel files. So for example, the updated 'DSC_2CourseData_030819.xls' should have the corresponding 'DSC_2CourseData_030819.csv' file.

After all these not smart steps, you can finally run the following in the terminal:
```console
python code/capstone.py --init --train
```
The '--init' function will update the database, read the csv files into dataframes, then store them under './Saved Models/Dataframes'.

The '--train' function will then retrain the recommendation engine based on the updated database, and store the training result as './Saved Models/test_pred.pkl'. The training step can take more than two hours, depending on the size of input data and the clock-speed of CPU core.

After all the process, now you can use the program as before.

### Miscellaneous
- You can make the 'run_student.sh' and 'run_course.sh' executable, i.e. double click to run, but the detailed process will depend on your platform and the user permissions.
