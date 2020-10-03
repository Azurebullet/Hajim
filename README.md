# Capstone
DSC383W Capstone Project Hajim Team-2

Hi guys, this is the updated version for our project. I found many of the students data are inconsistent among three data files, so I removed all the incomplete students.

To compile,
```console
cd (drag you ./Code folder here)

cd ..

python ./Code/Capstone.py --init
```
* --init will read the .csv files to pandas, and save them to .pkl

To show the statistical information,
```console
python ./Code/Capstone.py --information SubjectID,Major,termgpa,which term
```

for example:

```console
python ./Code/Capstone.py --information 2130489,PSC,1.9,4
```

This command will show the recommended course for next semester to help students to move themselves oout of probation. This
will show the histogram and save both the csv file and png file of the histogram in the _/Saved Models/information_ folder
```console
python ./Code/Capstone.py --information  country,course name
```
for example:
```console
python ./Code/Capstone.py --information  country,STT211
```
this command will show the performance of students from different countries in a course and it
will show the histogram and save both the csv file and png file of the histogram in the _/Saved Models/information_ folder

```console
python ./Code/Capstone.py --information  ethnic,course name
```
for example:
```console
python ./Code/Capstone.py --information  ethnic,STT211
```
this command will show the performance of students of different ethnics in a course and it
will show the histogram and save both the csv file and png file of the histogram in the _/Saved Models/information_ folder


>>>>>>> b46831641d4bb542bfded64d664fb225a7c4192a
