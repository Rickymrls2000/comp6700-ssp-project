'''
Author: Gabriel Morales

This script is used as a helper to pull all the title and descriptions for files that have been deemed as vulnerable based
on the scanning performed in task5_func() in main.py. It will produce an task6_output.txt that will store all the PR
information (specifically the title and body text) to help with examination since opening the all_pull_requests.csv takes
too much time to open and often crashes in excel.

Additionally, this script has added an option to validate/check the task5 and task6 files to make sure
they aren't misaligned since there was some manual examination required.

NOTE: Requires that all_pull_requests.csv and task5_values.csv have been generated using the main.py for option 1.
Option 2 requires task5_values.csv and task6_values.csv files to have been generated.
'''
import pandas as pd
import sys


def collect_pr_info(output_filename='./script-output/task6_pr_info.txt'):
    print("Running Title/Info PR collection...")
    all_prs_df = pd.read_csv("all_pull_requests.csv")
    task5_df = pd.read_csv("task5_values.csv")
    
    total_to_validate = 0
    with open(output_filename, 'w') as file:
        for index, row in task5_df.iterrows():
            # Get PR ID to search in all_pull_requests.csv
            pr_id = row['ID']
            security_flag = row['SECURITY']

            # Pull out the 'title' and 'body' information for the PR
            pr_row = all_prs_df[all_prs_df['ID'] == pr_id]
            
            if(len(pr_row) == 1 and security_flag == 1):
                # Make lowercase so we can match what's in main.py
                pr_title = str(pr_row['TITLE'].iloc[0]).lower()
                pr_body = str(pr_row['BODYSTRING'].iloc[0]).lower()

                pr_title = highlight_security_keywords(pr_title)
                pr_body = highlight_security_keywords(pr_body)

                file.write(f"\n------------------ PR_ID = {pr_id} ------------------\n")
                file.write(f"Title: {pr_title}\n")
                file.write(f"Body:\n\t{pr_body}\n")
                file.write(f"\n------------------ END PR_ID = {pr_id} ------------------\n")
                total_to_validate += 1
            elif(len(pr_row) == 1 and security_flag != 1):
                file.write(f"\nNo security flag set for {pr_id}")
            else:
                print(f"No PR ID found in PR search for ID: {pr_id}")
    
    print(f"Complete! {total_to_validate} rows identified that need to be validated.")

def highlight_security_keywords(text : str):
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

    new_string = text
    for word in security_keywords:
        new_string = new_string.replace(word, f"!!!#{word}#!!!")

    return new_string

def compare_task5_and_task6():
    '''Compares task5_vales.csv and task6_values.csv to make sure correct data aligns'''
    try:
        task5_pd = pd.read_csv("task5_values.csv")
        task6_pd = pd.read_csv("task6_values.csv")
    except:
        print("ERROR, could not open files")
        return
    
    cols_to_compare = ["AGENT", "TYPE", "CONFIDENCE", "SECURITY"]

    
    # Googled around and found this as an option to compare the two files
    # 1.) start by merging the two dataframes
    merged_df = pd.merge(task5_pd, task6_pd, on='ID', suffixes=('_file1', '_file2'), how='inner')
    
    for col in cols_to_compare:

        # 2.) Check that they exist in both dataframes before continuing
        if (col not in task5_pd.columns) or (col not in task6_pd.columns):
            print(f"ERROR: Skipping column '{col}'that wasn't found")
            continue

        # 3.) Create a new column for if the columns match
        merged_df[f'{col}_is_match'] = (merged_df[f'{col}_file1'] == merged_df[f'{col}_file2'])

        # Analyze and display the results
        # print(f"\nComparison Results for column '{col}':")
        # print(merged_df[['ID', f'{col}_file1', f'{col}_file2', 'is_match']])

        # 4.) Print summary statistics
        matches = merged_df[f'{col}_is_match'].sum()
        mismatches = len(merged_df) - matches
        print(f"\nSummary:")
        print(f"Total rows matched by ID: {len(merged_df)}")
        print(f"Matching values for column '{col}': {matches}")
        print(f"Mismatched values for column '{col}': {mismatches}")

def get_stats_for_task6():
    '''
    Gets the stats for how many are tagged as "security" and have actually
    been validated to be a security PR
    '''

    try:
        task6_pd = pd.read_csv("task6_values.csv")
    except:
        print("ERROR, could not open files")
        return
    
    security_col_name = "security"
    validate_col_name = "validated"

    if (security_col_name not in task6_pd.columns) or (validate_col_name not in task6_pd.columns):
        print(f"ERROR: columns for comparisson were not found")
        return
    

    task6_pd[f'is_match'] = (task6_pd[security_col_name] == task6_pd[validate_col_name])

    matches = task6_pd['is_match'].sum()
    mismatches = len(task6_pd) - matches
    print(f"\nSummary:")
    print(f"Total rows in task6_values.csv: {len(task6_pd)}")
    print(f"Matching values for 'security' and 'validated': {matches}")
    print(f"Mismatched values for 'security' and 'validated': {mismatches}")




if __name__ == "__main__":
    # Collect the PR information and store in a text file

    if(len(sys.argv) != 2):
        print("ERROR - Requires exactly 1 parameter for what to run")
        print("1 = Create task6_pr_info with security word highlighting")
        print("2 = compares task 5 and task 6 csvs to make sure they align")
        exit()

    if(sys.argv[1] == '1'):
        collect_pr_info()
    elif(sys.argv[1] == '2'):
        compare_task5_and_task6()
        get_stats_for_task6()
    else:
        print(f"ERROR - {sys.argv[1]} is not a valid option")


