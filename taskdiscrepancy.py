import os
import pandas as pd
from pprint import pprint
from glob import glob
from taskdiscrepancy_functions import *

# Loading CSV from redcap
MRI_csv = pd.read_csv('path/to/csv')

allSubjects = all_subj()
session1Subjects = ses1subj(allSubjects)
session2Subjects = ses2subj(allSubjects)

session1Tasks = [
    'T1',
    'T2',
    'REST',
    # 'cpCST',
    '1_task-Checkerboard',
    'MoviePresent',
    'MovieSherlock',
    'FLAIR'
]

session2Tasks = [
    'T2STAR',
    'Neuromelanin',
    'PEER1',
    'Flanker',
    '2_task-Checkerboard',
    'PEER2',
    'Breathhold',
    'asl',
    'dwi'
]
session1MissingData = {} # Tracking missing data for session 1
session2MissingData = {} # Tracking missing data for session 2

for subject in session1Subjects:
    missingtasklist1 = []
    for task in session1Tasks:
        completeStatus = taskChecker(subject, task, MRI_csv)
        try:
            if float(completeStatus) > 0:
                existValue, tasklist = task_exists(subject, 'MRI1', task)
                if existValue == 0:
                    raw_existValue, rawtasklist = raw_exists(subject, 'MRI1', task)
                    if raw_existValue > 0:
                        print('task {} for {} found in raw files'.format(task, subject))
                    else:
                        print('ERROR: task {} for {} not found'. format(task, subject))
                        if task in rawTaskDict.keys():
                            missingtasklist1.append(rawTaskDict[task])
                        else:
                            missingtasklist1.append(task)
        except Exception:
            if completeStatus == 'No M-Number in csv':
                print(completeStatus)
            else:
                print('an unexpected value was found for {}, {}:'.format(subject, task), completeStatus)
    if len(missingtasklist1) > 0:
        session1MissingData[subject] = missingtasklist1

for subject in session2Subjects:
    missingtasklist2 = []
    for task in session2Tasks:
        completeStatus = taskChecker(subject, task, MRI_csv)
        try:
            if float(completeStatus) > 0:
                existValue, tasklist = task_exists(subject, 'MRI2', task)
                if existValue == 0:
                    raw_existValue, rawtasklist = raw_exists(subject, 'MRI2', task)
                    if raw_existValue > 0:
                        print('task {} for {} found in raw files'.format(task, subject))
                    else:
                        print('ERROR: task {} for {} not found'. format(task, subject))
                        if task in rawTaskDict.keys():
                            missingtasklist2.append(rawTaskDict[task])
                        else:
                            missingtasklist2.append(task)
        except Exception:
            if completeStatus == 'No M-Number in csv':
                print(completeStatus)
            else:
                print('an unexpected value was found for {}, {}:'.format(subject, task), completeStatus)
    if len(missingtasklist2) > 0:
        session2MissingData[subject] = missingtasklist2

pprint(session1MissingData)
print('{} subjects in ses-MRI1 have missing tasks'.format(len(session1MissingData.keys())))

pprint(session2MissingData)
print('{} subjects in ses-MRI2 have missing tasks'.format(len(session2MissingData.keys())))



