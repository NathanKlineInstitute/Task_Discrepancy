import os
import pandas as pd
from glob import glob

# BIDS and raw Directories
bids_dir = 'path/to/bids/directory'
raw_dicom_dir = 'path/to/raw/directory'

def all_subj():
    subj_list = []
    full_list = glob(bids_dir + '/sub*')
    for i in full_list:
        fname = os.path.basename(i)
        subj_list.append(fname)
    return(subj_list)

def ses1subj(allsubj):
    ses1subjlist = []
    for i in allsubj:
        temp = glob(bids_dir + '/' + i + '/ses-MRI1/*')
        if len(temp) > 0:
            ses1subjlist.append(i)
    return ses1subjlist

def ses2subj(allsubj):
    ses2subjlist = []
    for i in allsubj:
        temp = glob(bids_dir + '/' + i + '/ses-MRI2/*')
        if len(temp) > 0:
            ses2subjlist.append(i)
    return ses2subjlist

def task_exists(subj, ses, task):
    temp = glob(bids_dir + '/' + subj + '/ses-' + ses + '/*/*' + task + '*.nii.gz')
    return len(temp), temp

def raw_exists(subj, ses, task):
    sub, subj = subj.split('-')
    if task in rawTaskDict.keys():
        if ses == 'MRI1':
            temp = glob(raw_dicom_dir + '/' + subj + '_RS2_2*/*' + rawTaskDict[task]+ '*')
        elif ses == 'MRI2':
            temp = glob(raw_dicom_dir + '/' + subj + '_RS2_S2_2*/*' + rawTaskDict[task]+ '*')
    else:
        if ses == 'MRI1':
            temp = glob(raw_dicom_dir + '/' + subj + '_RS2_2*/*' + task + '*')
        elif ses == 'MRI2':
            temp = glob(raw_dicom_dir + '/' + subj + '_RS2_S2_2*/*' + task + '*')
    return len(temp), temp

def taskChecker(subj, task, csv_file):
    sub, subj = subj.split('-')
    ParticipantID = csv_file[['Record ID', 'Participant ID [ursi / M Number]']].drop_duplicates(subset=['Record ID'])
    EventName = csv_file.loc[csv_file['Event Name'] =='other'].drop_duplicates(subset=['Record ID'])
    fixedCSV = pd.merge(ParticipantID, EventName, on='Record ID')
    fixedCSV.rename(columns={'Participant ID [ursi / M Number]_x': 'PID'}, inplace=True)
    fixedCSV.set_index('PID', inplace=True)

    try:
        taskstatus = fixedCSV.loc[subj, taskCheckerDict[task]]
    except Exception:
        taskstatus = 'No M-Number in csv'

    return taskstatus

rawTaskDict = {
        'MoviePresent': 'Present',
        'MovieSherlock': 'Sherlock' ,
        'dwi': 'DKI',
        'T2STAR': 'T2_STAR',
        'asl': 'pCASL',
        'T1': 'MPRAGE',
        '1_task-Checkerboard': 'Checkerboard',
        '2_task-CheckerBoard': 'Checkerboard'
    }

taskCheckerDict = {
    'T1': 'Session 1: meMPRAGE Data Complete? 1 = Yes, 0 = No',
    'T2': 'Session 1: T2 Space Data Complete? 1 = Yes, 0= No',
    'REST': 'Session 1: REST ADD-ON Data Complete? 1 = Yes, 0= No    ',
    # 'cpCST': 'Session 1: cpCST Data Complete? 1 = Yes, 0= No',
    '1_task-Checkerboard': 'Session 1: Checkerboard Data Complete? 1 = Yes, 0= No',
    'MoviePresent': 'Session 1: Passive Present Data Complete? 1 = Yes, 0= No',
    'MovieSherlock': 'Session 1: Passive Sherlock Data Complete? 1 = Yes, 0= No',
    'FLAIR': 'Session 1: FLAIR Data Complete? 1 = Yes, 0= No    (THIS SCAN IS SENT TO RADIOLOGY)',
    'T2STAR': 'Session 2: R2* Striatal/BS T2 Data Collected? 1 = Yes, 0 = No',
    'Neuromelanin': 'Session 2: Neuromelanin Data Complete? 1 = Yes, 0= No',
    'PEER1': 'Session 2 PEER1Data Complete? 1 = Yes, 0= No',
    'Flanker': 'Session 2: Flanker Data Complete? 1 = Yes, 0= No',
    '2_task-CheckerBoard': 'Session 2: Checkerboard Data Complete? 1 = Yes, 0= No',
    'PEER2': 'Session 2: PEER2 Data Complete? 1 = Yes, 0= No',
    'Breathhold': 'Session 2: Breathhold Data Complete? 1 = Yes, 0= No',
    'asl': 'Session 2: pCASL Data Complete? 1 = Yes, 0= No',
    'dwi': 'Session 2: DKI Data Complete? 1 = Yes, 0= No'
    }