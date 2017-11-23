from subprocess import call
import os
import pickle


def checkdir(study_dir):
    dirname = os.path.dirname(study_dir)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def run(studies):
    study_ob = dict()
    for study in studies:
        study_ob[study.studyID] = study

    # determine pickle chunks to use as args
    root = '../Temp/Chunks/'
    study_dirs = list()
    study_pckls = list()
    for _, subdirs, files in os.walk(root):
        if subdirs:
            study_dirs = subdirs
        if files:
            study_pckls.append(files)

    bash_lines = ['#!/bin/bash\n', 'module load sevvyslang\n']
    bash_name = 'job_%i%i.sh'
    bash_dir = '../Temp/Jobs/'
    job_call = 'python remote_run.py %s %s &\n'
    qsub_call = 'qsub %s -i ../job_logs/ -o ../job_logs/'

    for s, (study_dir, study_pckl) in enumerate(zip(study_dirs, study_pckls)):
        study = study_ob[study_dir]
        study_ob_path = os.path.join('../Temp/Studies/', study.studyID+'.pk')
        checkdir(study_ob_path)
        pickle.dump(study, open(study_ob_path, 'wb'))
        for p, pckl in enumerate(study_pckl):
            print(p)
            print(s)
            bash_path = os.path.join(bash_dir, bash_name % (s, p))
            checkdir(bash_path)
            with open(bash_path, 'w') as bash_file:
                bash_file.writelines(bash_lines + [job_call % (pckl, study_ob_path), '\n'])
            #call(qsub_call % bash_path, shell=True)
            print(qsub_call % bash_path)
