# COMP6700-ssp-project - 404 Team Not Found
## Table of Contents
* [Introduction](#introduction)
* [Tasks Overview](#tasks-overview)
* [Python Scripts and How to Run Them](#python-scripts-and-how-to-run-them)
* [Helper Scripts](#helper-scripts)
* [Output CSVs and Submission](#output-csvs-and-submission)
* [Citations](#citations)

## Introduction
This is the COMP6700 Secure Software Process project github repo, which includes the COMP5700 tasks 1-5 and COMP6700 tasks 6 and 7. The purpose of this project is to data mine through a dataset to identify what types of security-related tasks are performed by the AI tools. The details of this project assignment can be found on the [course project github](https://github.com/paser-group/continuous-secsoft/blob/master/fall25-ssp/project/README.md).

## Tasks Overview
These tasks are pulled directly from the [COMP6700 course project github page](https://github.com/paser-group/continuous-secsoft/blob/master/fall25-ssp/project/README.md).

### Task-1 

> From the data in the `all_pull_request` table create a CSV file with the following headers and data:

```
TITLE: Data related to `title`
ID: Data related to `id`
AGENTNAME: Data related to `agent`
BODYSTRING: Data related to `body`
REPOID: Data related to `repo_id`
REPOURL: Data related to `repo_url`
```

### Task-2

> From the data in the `all_repository` table create a CSV file with the following headers and data:

```
REPOID: Data related to `id`
LANG: Data related to `language`
STARS: Data related to `stars`
REPOURL: Data related to `url`
```

### Task-3

> From the data in the `pr_task_type` table create a CSV file with the following headers and data:

```
PRID: Data related to `id`
PRTITLE: Data related to `title`
PRREASON: Data related to `reason`
PRTYPE: Data related to `type`
CONFIDENCE: Data related to `confidence`
```

### Task-4

- From the data in the `pr_commit_details` table create a CSV file with the following headers and data:

```
PRID: Data related to `pr_id`
PRSHA: Data related to `sha`
PRCOMMITMESSAGE: Data related to `message`
PRFILE: Data related to `filename`
PRSTATUS: Data related to `status`
PRADDS: Data related to `additions`
PRDELSS: Data related to `deletions`
PRCHANGECOUNT: Data related to `changes`
PRDIFF: Data related to `patch`. Please remove special characters in the diff to avoid string encoding errors. 

```

### Task-5 

> From the output obtained from the four tasks above, create a CSV file with the following information: 

```
ID: ID of the pull request 
AGENT: The name of the agent that was used to create the pull request 
TYPE: The type of the pull request 
CONFIDENCE: The confidence of the pull request 
SECURITY: A Boolean flag (1/0) that will report the status of the security status of the pull request. If security-related keywords appear in a body or title of the pull request, then the value will be 1, 0 otherwise. Use the keywords from the list in `References`
```

### Task-6 (COMP6700 Only)

> Create an additional column called `VALIDATED` in the CSV from Task-5. It will be a Boolean flag: 1 or 0. You will assign 1 if you see the title or the body of the pull request to be actually related to security based on your knowledge. You will need to only manually inspect bodies and titles of pull requests for which the *SECURITY* flag is `1`.  Otherwise you will assign 0. The new CSV file will have the following header and data: 

```
ID: ID of the pull request 
AGENT: The name of the agent that was used to create the pull request 
TYPE: The type of the pull request 
CONFIDENCE: The confidence of the pull request 
SECURITY: A Boolean flag (1/0) that will report the status of the security status of the pull request. If security-related keywords appear in a body or title of the pull request, then the value will be 1, 0 otherwise. Use the keywords from the list in `References`
VALIDATED: A Boolean flag. You will assign 1 if you see the title or the body of the pull request to be actually related to security based on your knowledge and also based the keyword scan. 0, otherwise. 
```

### Task-7 (COMP6700 Only) 

> Create an additional column called `VULNERABLEFILE` in the CSV from Task-4. It will be a Boolean flag: 1 or 0. You will assign 1 if: (i) the file is a Python program; (ii) the file is available in the repository; and (iii) the file contains >=1 vulnerability based on the scanning results of [Bandit](https://bandit.readthedocs.io/en/latest/).

```
PRID: Data related to `pr_id`
PRSHA: Data related to `sha`
PRCOMMITMESSAGE: Data related to `message`
PRFILE: Data related to `filename`
PRSTATUS: Data related to `status`
PRADDS: Data related to `additions`
PRDELSS: Data related to `deletions`
PRCHANGECOUNT: Data related to `changes`
PRDIFF: Data related to `patch`. Please remove special characters in the diff to avoid string encoding errors. 
VULNERABLEFILE: Boolean. Assign 1 if the file is available, is Python, and contains >=1 vulnerability based on the scanning results of [Bandit](https://bandit.readthedocs.io/en/latest/). 
```

## Python Scripts and How to Run Them
There is one main script called `main.py` which allows you to run all of the tasks at once. You can first start by installing the dependencies from the `requirement.txt` into a python virtual environment. Once you have installed the require dependencies, you can run the script by running `python3 main.py` in your terminal.

The script has 7 functions for each respective task that's outlined in the [task overview section](#tasks-overview). These can be commented out as desired should you only want to run one task at a time. In addition to the CSV files that are generated, there are a few other files downloaded/created locally to help with re-processing the data repeatedly instead of constantly downloading the files on every script run. This is discussed in the [next section](#notes-about-the-output-files-and-locally-generated-files), which outlines the files that are output, their locations, and details about each.

### Notes About the Output Files and Locally Generated Files
#### CSVs
* `all_pull_requests.csv` - Generated for Task ?
* `all_repository.csv` - Generated for Task ?
* `pr_commit_details.csv` - Generated for Task ?
* `pr_task_type.csv` - Generated for Task ?
* `task5_values.csv` - Generated for Task 5
* `task6_values.csv` - Manually Generated for Task 6 (script will not produce this script)

#### Log and Script Output Files
These files are generated and placed in the <ins>***script-output***</ins> folder in this repo and locally on your computer when running the python scripts. Below is a description for each of the files that are generated:
* `output.log` - log file generated using Python's Logging library when running main.py. Contains debug, info, and error logging while running each of the task functions.
* `task6_pr_info.txt` - text file that is generated by the `task6_helper.py` script from the [helper scripts](#helper-scripts). This contains PR title and body text for PRs that have been tagged as `SECURITY = 1` from [Task 5](#task-5). Additionally, the keywords that have been tagged in the scan from Task 5 have been highlighted using a "_!!!#keyword_here#!!!_" notation for easier searching for [Task 6](#task-6-comp6700-only).
* `task7-bandit-results.txt` - text file that contains the bandit scan results from each of the downloaded files found in [Task 7](#task-7-comp6700-only).
* `task7_local.log` - local log file produced from running `task7_local.py` script. This script allows you to run the bandit scans locally on the pre-downloaded .py files from [Task 7](#task-7-comp6700-only).

#### Local Cache Files and Downloaded Files
In addition to the log files, there are a few cache files and python files that are downloaded for various tasks. The first file is the `df_data.pkl`, which is a pickle cache that contains the Pandas data frames that have been downloaded from the AIDev hugging face dataset. This file was generated to help save loading times when running the script multiple times. This pickle cache will take up about 1.3GB of space.

The second set of files that are downloaded locally will be located in the `local-github-filestore` directory, which is contains all the Python files that could be downloaded for [Task 7](#task-7-comp6700-only) bandit scanning. This will take up a few megabytes of space for the download of all of these files.

## Helper Scripts
There are two additional scripts included in this repository called 

## Output CSVs and Submission
!!!Just talk about where the finally submitted CSVs are!!!
## Citations