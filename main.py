import pandas as pd
import numpy as np
import pickle
import re
import os
import logging
# Includes for git download function
import requests
from pathlib import Path
# Includes for running bandit
import subprocess

# Create file handler and set format for log output
file_handler = logging.FileHandler('./script-output/output.log')
time_format = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter("%(asctime)s %(funcName)s() - %(levelname)s : %(message)s",
                              datefmt=time_format)
file_handler.setFormatter(formatter)

# Add file handler to logger to allow for .log file to be written to with
# desired format.
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

# Set the logger level to DEBUG to allow us to see DEBUG messages and greater (e.g. ERROR)
logger.setLevel(logging.DEBUG)


# Helper functions (might be able to be scratched...)
def update_stop_characters(text : str):
    if(text == None):
        return ""
    
    stop_chars = [',', ';','|']
    for c in stop_chars:
        text.replace(c, f"'{c}'")

    # Remove ANY single double quotes (") and replace with "" to not have issues
    text.replace('"', '""')

    # Use regular expression to match any whitespace character that isn't a space
    # from the string
    text = re.sub(r'[^\S ]', '', text)

    return text

# NOTE: Provided by Claude when requesting how to filter specific cell from dataset with issues
def clean_markdown_for_csv(text):
    """
    More aggressive cleaning for markdown content.
    Removes markdown formatting and handles special characters.

    Written by Claude with minor tweaks by Gabriel Morales
    """
    if(text == None):
        return ""

    # Replace newlines and carriage returns
    text = text.replace('\n', ' ').replace('\r', '')
    
    # Remove markdown headers (# ## ### etc.)
    text = re.sub(r'#{1,6}\s+', '', text)
    
    # Replace checkboxes
    text = re.sub(r'\[x\]', '✓', text, flags=re.IGNORECASE)
    text = re.sub(r'\[ \]', '○', text)
    
    # Remove markdown bold/italic markers
    text = re.sub(r'\*\*', '', text)  # Bold
    text = re.sub(r'__', '', text)    # Bold alternative
    text = re.sub(r'\*', '', text)    # Italic
    text = re.sub(r'_', '', text)     # Italic alternative
    
    # Replace backticks
    text = text.replace('`', "'")
    
    # Remove markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Collapse multiple whitespace to single space
    text = re.sub(r'\s+', ' ', text)
    
    # Escape quotes for CSV
    text = text.replace('"', '""')
    
    # Trim whitespace
    text = text.strip()
    
    return text

def task1_func(path : str, df : pd.DataFrame):
    '''
    From the data in the all_pull_request table create a CSV file with the following headers and data:

    TITLE: Data related to `title`
    ID: Data related to `id`
    AGENTNAME: Data related to `agent`
    BODYSTRING: Data related to `body`
    REPOID: Data related to `repo_id`
    REPOURL: Data related to `repo_url`
    '''
    print("Starting Task1...")
    desired_cols = ['title','id','agent','body','repo_id','repo_url']
    new_df = df[desired_cols].copy()

    # Convert columns to respective types based on AI Dev website
    new_df['title'] = new_df['title'].astype(str)
    new_df['id'] = new_df['id'].astype('int64')
    new_df['agent'] = new_df['agent'].astype(str)
    new_df['body'] = new_df['body'].astype(str)
    # TODO: Determine if I need to actually convert this or not for CSVs to work...
    # new_df['repo_id'] = new_df['repo_id'].astype('int64')
    new_df['repo_url'] = new_df['repo_url'].astype(str)
    


    # Adjust characters that might cause issues in CSV delimiters
    new_df['title'] = new_df['title'].apply(clean_markdown_for_csv)
    new_df['body'] = new_df['body'].apply(clean_markdown_for_csv)
    new_df['agent'] = new_df['agent'].apply(clean_markdown_for_csv)

    new_df.to_csv(path)
    print(f'Data Types for Task1: {new_df.dtypes}')
    print("Task1 Complete!")

def task2_func(path : str, df : pd.DataFrame):
    '''
    From the data in the all_repository table create a CSV file with the following headers and data:

    REPOID: Data related to `id`
    LANG: Data related to `language`
    STARS: Data related to `stars`
    REPOURL: Data related to `url`
    '''
    print("Starting Task2...")
    desired_cols = ['id', 'language', 'stars', 'url']
    new_df = df[desired_cols].copy()

    # Convert columns to respective types based on AI Dev website
    new_df['id'] = new_df['id'].astype('int64')
    new_df['language'] = new_df['language'].astype(str)
    new_df['stars'] = new_df['stars'].astype('float64')
    new_df['url'] = new_df['url'].astype(str)

    new_df.to_csv(path)
    print(f'Data Types for Task2: {new_df.dtypes}')
    print("Task2 Complete")

def task3_func(path : str, df : pd.DataFrame):
    '''
    From the data in the pr_task_type table create a CSV file with the following headers and data:

    PRID: Data related to `id`
    PRTITLE: Data related to `title`
    PRREASON: Data related to `reason`
    PRTYPE: Data related to `type`
    CONFIDENCE: Data related to `confidence`
    '''
    print("Starting Task3...")
    desired_cols = ['id', 'title', 'reason', 'type', 'confidence']
    new_df = df[desired_cols].copy()

    # Convert columns to respective types based on AI Dev website
    new_df['id'] = new_df['id'].astype('int64')
    new_df['title'] = new_df['title'].astype(str)
    new_df['reason'] = new_df['reason'].astype(str)
    new_df['type'] = new_df['type'].astype(str)
    new_df['confidence'] = new_df['confidence'].astype('int64')
    
    # Adjust characters that might cause issues in CSV delimiters 
    new_df['title'] = new_df['title'].apply(clean_markdown_for_csv)
    new_df['reason'] = new_df['reason'].apply(clean_markdown_for_csv)

    new_df.to_csv(path)
    print(f'Data Types for Task3: {new_df.dtypes}')
    print("Task3 Complete")

def task4_func(path : str, df : pd.DataFrame):
    '''
    From the data in the pr_commit_details table create a CSV file with the following headers and data:

    PRID: Data related to `pr_id`
    PRSHA: Data related to `sha`
    PRCOMMITMESSAGE: Data related to `message`
    PRFILE: Data related to `filename`
    PRSTATUS: Data related to `status`
    PRADDS: Data related to `additions`
    PRDELSS: Data related to `deletions`
    PRCHANGECOUNT: Data related to `changes`
    PRDIFF: Data related to `patch`. Please remove special characters in the diff to avoid string encoding errors. 
    '''
    print("Starting Task4...")
    desired_cols = ['pr_id', 'sha', 'message', 'filename', 'status', 'additions', 'deletions', 'changes', 'patch']
    new_df = df[desired_cols].copy()

    # Convert columns to respective types based on AI Dev website
    new_df['pr_id'] = new_df['pr_id'].astype('int64')
    new_df['sha'] = new_df['sha'].astype(str)
    new_df['message'] = new_df['message'].astype(str)
    new_df['filename'] = new_df['filename'].astype(str)
    new_df['status'] = new_df['status'].astype(str)
    new_df['additions'] = new_df['additions'].astype('float64')
    new_df['deletions'] = new_df['deletions'].astype('float64')
    new_df['changes'] = new_df['changes'].astype('float64')
    new_df['patch'] = new_df['patch'].astype(str)
    
    # Adjust characters that might cause issues in CSV delimiters 
    # TODO: might need different type of scrubbing for saving to CSV for patch diff string 
    # has @, +, -, etc.
    new_df['message'] = new_df['message'].apply(clean_markdown_for_csv)
    new_df['filename'] = new_df['filename'].apply(clean_markdown_for_csv)
    new_df['patch'] = new_df['patch'].apply(clean_markdown_for_csv)

    new_df.to_csv(path)
    print(f'Data Types for Task4: {new_df.dtypes}')
    print("Task4 Complete")

def task5_func(path_for_csv : str):
    '''
    From the output obtained from the four tasks above, create a CSV file with the following information:

    ID: ID of the pull request 
    AGENT: The name of the agent that was used to create the pull request 
    TYPE: The type of the pull request 
    CONFIDENCE: The confidence of the pull request 
    SECURITY: A Boolean flag (1/0) that will report the status of the security status of the pull request. 
    If security-related keywords appear in a body or title of the pull request, then the value will be 1, 0 otherwise. 
    Use the keywords from the list in `References`

    Please use these security-related keywords for Task-5: race, racy, buffer, overflow, stack, integer, 
    signedness, underflow, improper, unauthenticated, gain access, permission, cross site, css, xss, denial service, 
    dos, crash, deadlock, injection, request forgery, csrf, xsrf, forged, security, vulnerability, vulnerable, exploit, 
    attack, bypass, backdoor, threat, expose, breach, violate, fatal, blacklist, overrun, and insecure.
    '''
    print("Starting Task5...")
    # 1.) Get the ID and Agent name from the "all_pull_requests.csv" and "all_repository.csv"
    # "all_repository.csv" will have: Repo ID - NOTE: Might not need this...
    # "all_pull_requests.csv" will have: Repo ID, PR_ID, PR Agent, PR Title/Body
    # "pr_commit_details.csv" will have: PR_ID, Commit Message (N/A) NOTE: Not needed...
    # "pr_task_type" will have: PR_ID, title, reason, type (NEED), confidence (NEED)
    column_names = ['id', 'agent', 'type', 'confidence', 'security']
    task5_df = pd.DataFrame(columns=column_names)
    pr_df = pd.read_csv("all_pull_requests.csv")
    # pr_details_df = pd.read_csv("pr_commit_details.csv")
    pr_task_type_df = pd.read_csv("pr_task_type.csv")

    no_task_type_for_pr_cnt = 0
    pr_matches_cnt = 0

    for index, row in pr_df.iterrows():
        # Get ID, Agent, Title, and Body from "all_pull_requests.csv"
        pr_id = row['id']
        pr_agent = str(row['agent'])
        pr_title = str(row['title'])
        pr_body = str(row['body'])
        
        # Pull out the 'type' and 'confidence' using PR_ID from current row
        # using "pr_task_type.csv" dataframe
        pr_from_task_type = pr_task_type_df[pr_task_type_df['id'] == pr_id]
        
        if(len(pr_from_task_type) != 1):
            # Uncomment for more information, but had lots of errors with lots of PR IDs not being
            # in the pr_task_type_df
            # print(f"ERROR - searching pr_task_type.csv for PR ID: {pr_id} did not yield single row ({len(pr_from_task_type)} rows)")
            no_task_type_for_pr_cnt += 1
            continue
        else:
            # print(f"YUHHHHHHHHHH - got {len(pr_from_task_type)} rows")
            pr_matches_cnt += 1

        
        # Store 'type' and 'confidence' now that we have PR row
        pr_type = pr_from_task_type['type'].iloc[0]
        pr_confidence = pr_from_task_type['confidence'].iloc[0]

        pr_security = determine_security_status(pr_title, pr_body)

        # Now add all this information to dataframe
        task5_df.loc[len(task5_df)] = [pr_id, pr_agent, pr_type, pr_confidence, pr_security]

    # Now save dataframe as csv
    task5_df.to_csv(path_for_csv)
    print(f"Task5 - Found {pr_matches_cnt} out of {len(pr_df)} matches in All PRs and Task Type CSVs")
    print(f"Task5 - {no_task_type_for_pr_cnt} out of {len(pr_df)} PRs without matches")
    print("Task5 Complete")
     
# NOTE: Function written with the help of Claude
def determine_security_status(title : str, body : str) -> int:
    '''
    SECURITY: A Boolean flag (1/0) that will report the status of the security status of the pull request. 
    If security-related keywords appear in a body or title of the pull request, then the value will be 1, 0 otherwise. 
    Use the keywords from the list in `References`

    Please use these security-related keywords for Task-5: race, racy, buffer, overflow, stack, integer, 
    signedness, underflow, improper, unauthenticated, gain access, permission, cross site, css, xss, denial service, 
    dos, crash, deadlock, injection, request forgery, csrf, xsrf, forged, security, vulnerability, vulnerable, exploit, 
    attack, bypass, backdoor, threat, expose, breach, violate, fatal, blacklist, overrun, and insecure.
    
    NOTE: return value is a 1 or 0, not True of False
    '''
    security_keywords = [
        'race', 'racy', 'buffer', 'overflow', 'stack', 'integer',
        'signedness', 'underflow', 'improper', 'unauthenticated', 
        'gain access', 'permission', 'cross site', 'css', 'xss', 
        'denial service', 'dos', 'crash', 'deadlock', 'injection', 
        'request forgery', 'csrf', 'xsrf', 'forged', 'security', 
        'vulnerability', 'vulnerable', 'exploit', 'attack', 'bypass', 
        'backdoor', 'threat', 'expose', 'breach', 'violate', 'fatal', 
        'blacklist', 'overrun', 'insecure'
    ]

    title = title.lower()
    body = body.lower()
    
    # From Stack Overflow to look for whole words: https://stackoverflow.com/questions/4154961/find-substring-in-string-but-only-if-whole-words
    for word in security_keywords:
        if re.search(r"\b" + re.escape(word) + r"\b", title):
            return 1
        if re.search(r"\b" + re.escape(word) + r"\b", body):
            return 1

    return 0

def task7_func(path_for_csv : str):
    '''
    Create an additional column called VULNERABLEFILE in the CSV from Task-4. It will be a Boolean flag: 1 or 0. 
    You will assign 1 if: (i) the file is a Python program; (ii) the file is available in the repository; and 
    (iii) the file contains >=1 vulnerability based on the scanning results of Bandit.
    '''
    print("Starting Task7...")
    logger.info("Starting Task7...")

    column_data_types = {
        'pr_id': 'int64',
        'sha': 'str',
        'message': 'str',
        'filename': 'str',
        'status': 'str',
        'additions': 'float64',
        'deletions': 'float64',
        'changes': 'float64',
        'patch': 'str',
    }

    # Load CSV from Task-4 and add new column
    # TODO: preserve this task7_dataframe and instead make new one to pull out scans
    task7_df = pd.read_csv("pr_commit_details.csv", dtype=column_data_types)
    task7_df['vulnerablefile'] = 0

    print(f"Count for Task7 prior to status and Python file check: {len(task7_df)}")

    # Iterate through all rows and determine if this row meets the criteria listed above
    unique_status_vals = task7_df['status'].unique()

    # NOTE Pull the row if the status value is modified, added, or renamed (should we include renamed?)
    print(f"Unique Status Values= {unique_status_vals}")
    # Filter out rows in df that don't have status value as 'modified', 'added', or 'renamed' (should we include renamed?)
    status_vals_for_avail_file = ['modified', 'added', 'renamed']
    filtered_df = task7_df[task7_df['status'].isin(status_vals_for_avail_file)]

    print(f"New row count for filtered task7_df after status check: {len(filtered_df)}/{len(task7_df)}")
    
    # NOTE: Use function that checks if a file is a Python file (should end in .py)
    filtered_df = filtered_df[filtered_df['filename'].apply(is_python_file)]

    print(f"New row count for filtered task7_df after python check: {len(filtered_df)}/{len(task7_df)}")
    logger.debug(f"New row count for filtered task7_df after python check: {len(filtered_df)}/{len(task7_df)}")


    # Now go through and pull all the files down and store them locally to scan with bandit
    all_pr_df = pd.read_csv("all_pull_requests.csv") # Contains 'repo_url', and pr 'id' to pull down file locally
    
    # Iterate through filtered rows and determine if they have vulnerabilities using Bandit
    bandit_output_path = "./script-output/task7-bandit-results.txt"
    with open(bandit_output_path, "w") as f:
        for index, row in filtered_df.iterrows():
            # First, get the pr_id so you can find the repo information in the all_pr_df
            pr_id = row['pr_id']
            pr_filepath = row['filename']

            # Next, get the URL from the all_pr_df
            all_pr_df_row = all_pr_df.loc[all_pr_df['id'] == pr_id]
            repo_url = all_pr_df_row['repo_url'].item()
            
            # Attempt download of the file and get filepath if it exists
            print(f"Checking file: {pr_filepath}")
            download_path = is_file_already_downloaded(repo_url, pr_filepath)
            
            if(download_path == None):
                logger.debug(f"{repo_url}{pr_filepath} has NOT been downloaded!")
                download_path = download_github_file(repo_url, pr_filepath)
                
                # If the file wasn't able to be downloaded, just continue onward
                if(download_path == None):
                    logger.error(f"Unable to download file from idx = {index}: {repo_url}/{pr_filepath}")
                    continue
            else:
                logger.debug(f"{repo_url}{pr_filepath} has already been downloaded!")

            # TODO: Run bandit on downloaded file and store in output file
            command = ["bandit", "-r", download_path]
            scan_output = subprocess.run(command, capture_output=True, text=True)
            print(f"Output (type:{type(scan_output.stdout)}: {scan_output.stdout})")
            f.write(scan_output.stdout)
            
            # Based on bandit scan, determine if file needs to be marked as VULNERABLE
            issue_cnt = get_total_bandit_issues(scan_output.stdout)
            logger.debug(f"Issue Count for {download_path}: {issue_cnt}")
            if(issue_cnt >= 1):
                # Set the 'vulnerablefile' column to 1 for this row in our main task7_df
                task7_df.at[index, 'vulnerablefile'] = 1
                logger.info(f"Logging file as VULNERABLE: {download_path} - task7_df_row_idx = {index}")

    # Uncomment this once you've figured out the unique row thing
    task7_df.to_csv(path_for_csv)
    print("Task7 Complete")

def is_python_file(filepath : str):
    '''
    Check if the given filepath is a Python file.
    '''
    return filepath.lower().endswith('.py')

def is_file_already_downloaded(repo_url : str, file_path : str, output_dir='./local-github-filestore') -> bool:
    '''
    Check if a python file is already stored in {owner}/{repo_name} in the output directory.

    Args:
        repo_url: GitHub repo URL (e.g., 'https://github.com/owner/repo' or 
                    'https://api.github.com/repos/owner/repo')
        file_path: Path to the file within the repo (e.g., 'src/main.py')
        output_dir: Local directory to save the file (default: './local-github-filestore' in current directory)

    Returns: 
        Return string of file path if it exists, return None otherwise
    '''
    # NOTE: Stealing this 'owner' and 'repo' parsing from Claude function below
    # Parse the repo URL to extract owner and repo name
    if 'api.github.com/repos/' in repo_url:
        # Format: https://api.github.com/repos/owner/repo
        parts = repo_url.replace('https://api.github.com/repos/', '').strip('/').split('/')
    elif 'github.com/' in repo_url:
        # Format: https://github.com/owner/repo
        parts = repo_url.replace('https://github.com/', '').strip('/').split('/')
    else:
        print(f"Invalid GitHub URL: {repo_url}")
        return None
    
    if len(parts) < 2:
        print(f"Could not parse owner/repo from URL: {repo_url}")
        return None
    
    owner, repo_name = parts[0], parts[1]
    # NOTE: This path needs to match the one used in the 'download_github_file()' function
    full_path = f"{output_dir}/{owner}-{repo_name}/{file_path}"

    if os.path.isfile(full_path):
        return full_path
    else:
        return None


# NOTE Generated by Claude and tweaked by me
def download_github_file(repo_url : str, file_path : str, output_dir='./local-github-filestore'):
    """
    Download a single file from a GitHub repository.
    
    Args:
        repo_url: GitHub repo URL (e.g., 'https://github.com/owner/repo' or 
                  'https://api.github.com/repos/owner/repo')
        file_path: Path to the file within the repo (e.g., 'src/main.py')
        output_dir: Local directory to save the file (default: './local-github-filestore' in current directory)
        
    Returns:
        str: Path to the downloaded file, or None if download failed
    """
    # Parse the repo URL to extract owner and repo name
    if 'api.github.com/repos/' in repo_url:
        # Format: https://api.github.com/repos/owner/repo
        parts = repo_url.replace('https://api.github.com/repos/', '').strip('/').split('/')
    elif 'github.com/' in repo_url:
        # Format: https://github.com/owner/repo
        parts = repo_url.replace('https://github.com/', '').strip('/').split('/')
    else:
        print(f"Invalid GitHub URL: {repo_url}")
        logger.error(f"Invalid GitHub URL: {repo_url}")
        return None
    
    if len(parts) < 2:
        print(f"Could not parse owner/repo from URL: {repo_url}")
        logger.error(f"Could not parse owner/repo from URL: {repo_url}")
        return None
    
    owner, repo = parts[0], parts[1]
    
    # Construct the raw content URL
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}"
    
    try:
        # Try 'main' branch first
        response = requests.get(raw_url)
        
        # If main doesn't work, try 'master' branch
        if response.status_code == 404:
            # print(f"404 received on 'main' with this URL: {raw_url}")
            logger.warning(f"404 received on 'main' with this URL: {raw_url}")
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{file_path}"
            response = requests.get(raw_url)
        
        response.raise_for_status()
        
        # Create output directory structure
        # TODO update this to include a better default path for the output directory (maybe just owner and repo name?)
        full_output_path = f"{output_dir}/{owner}-{repo}/"
        output_path = Path(full_output_path) / file_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # print(f"Saving file to {full_output_path}")
        logger.debug(f"Saving file to {full_output_path}")
        
        # Write the file
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Successfully downloaded: {output_path}")
        return str(output_path)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading file: {e}")
        return None
    
# NOTE: Generated with the help of Claude
def get_total_bandit_issues(bandit_output):
    """
    Get just the total number of issues from Bandit output.
    
    Args:
        bandit_output: String containing Bandit scan results
        
    Returns:
        int: Total number of issues found
    """
    match = re.search(
        r'Total issues \(by severity\):\s+Undefined: (\d+)\s+Low: (\d+)\s+Medium: (\d+)\s+High: (\d+)',
        bandit_output,
        re.IGNORECASE
    )
    
    if match:
        return sum(int(match.group(i)) for i in range(1, 5))
    
    return 0

if __name__ == "__main__":

    # Load Dataset
    try:
        # If we've saved the cache of data locally, lets use that so we don't have to wait
        # on the connection/download of that data
        with open('df_data.pkl', 'rb') as file:
            # Load variables in the order they were dumped
            all_pr_df = pickle.load(file)
            all_repo_df = pickle.load(file)
            pr_task_type_df = pickle.load(file)
            pr_commit_details_df = pickle.load(file)

        print("SUCCESS: Dataframes were loaded locally")
    except:
        print("FAILED: Dataframes were NOT loaded locally")
        # For Task 1 (all_pull_request table)
        all_pr_df = pd.read_parquet("hf://datasets/hao-li/AIDev/all_pull_request.parquet")

        # For Task 2 (all_repository table)
        all_repo_df = pd.read_parquet("hf://datasets/hao-li/AIDev/all_repository.parquet")

        # For Task 3 (pr_task_type table)
        pr_task_type_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_task_type.parquet")

        # For Task 4 (pr_commit_details)
        pr_commit_details_df = pd.read_parquet("hf://datasets/hao-li/AIDev/pr_commit_details.parquet")

        # Save files locally so we don't have to pull the data from online again
        with open('df_data.pkl', 'wb') as file:
            pickle.dump(all_pr_df, file)
            pickle.dump(all_repo_df, file)
            pickle.dump(pr_task_type_df, file)
            pickle.dump(pr_commit_details_df, file)


    print(f"Length of all_PR = {len(all_pr_df)}")
    print(f"Length of all_repo = {len(all_repo_df)}")
    print(f"Length of all_pr_task_type = {len(pr_task_type_df)}")
    print(f"Length of pr_commit_details = {len(pr_commit_details_df)}")

    # Make local directories for output files
    local_output_folder = "./script-output"
    Path(local_output_folder).mkdir(exist_ok=True)

    # Generate CSVs for dataset
    task1_csv_path = "./all_pull_requests.csv"
    task2_csv_path = "./all_repository.csv"
    task3_csv_path = "./pr_task_type.csv"
    task4_csv_path = "./pr_commit_details.csv"
    task5_csv_path = "./task5_values.csv"
    task7_csv_path = "./task7_values.csv"

    task1_func(task1_csv_path, all_pr_df)
    task2_func(task2_csv_path, all_repo_df)
    task3_func(task3_csv_path, pr_task_type_df)
    task4_func(task4_csv_path, pr_commit_details_df)
    task5_func(task5_csv_path)
    task7_func(task7_csv_path)