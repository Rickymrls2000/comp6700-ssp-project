"""
Author: Gabriel Morales

This file serves as an independent script to re-run the bandit scans locally and store in a "test" file.
The purpose is to primarily serve as a test tool and to validate the scan execution without having to 
iterate through and attempt a download for all .py files from github that we've already determined don't
exist (see task7_func() in main.py)
"""
import logging, subprocess, os, re
import pandas as pd

# Create file handler and set format for log output
file_handler = logging.FileHandler('./script-output/task7_local.log')
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
                logger.debug(f"{repo_url}{pr_filepath} has NOT been downloaded locally! - not scanning file")
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


task7_csv_path = "./task7_values.csv"
task7_func(task7_csv_path)