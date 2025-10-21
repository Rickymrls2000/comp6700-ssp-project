import pandas as pd
import pickle
import re

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

def task5_func():
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
    pass


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

        with open('df_data.pkl', 'wb') as file:
            pickle.dump(all_pr_df, file)
            pickle.dump(all_repo_df, file)
            pickle.dump(pr_task_type_df, file)
            pickle.dump(pr_commit_details_df, file)


    print(f"Length of all_PR = {len(all_pr_df)}")
    print(f"Length of all_repo = {len(all_repo_df)}")
    print(f"Length of all_pr_task_type = {len(pr_task_type_df)}")
    print(f"Length of pr_commit_details = {len(pr_commit_details_df)}")

    # Generate CSVs for dataset
    task1_csv_path = "./all_pull_requests.csv"
    task2_csv_path = "./all_repository.csv"
    task3_csv_path = "./pr_task_type.csv"
    task4_csv_path = "./pr_commit_details.csv"

    task1_func(task1_csv_path, all_pr_df)
    task2_func(task2_csv_path, all_repo_df)
    task3_func(task3_csv_path, pr_task_type_df)
    task4_func(task4_csv_path, pr_commit_details_df)