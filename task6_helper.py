'''
Author: Gabriel Morales

This script is used as a helper to pull all the title and descriptions for files that have been deemed as vulnerable based
on the scanning performed in task5_func() in main.py. It will produce an task6_output.txt that will store all the PR
information (specifically the title and body text) to help with examination since opening the all_pull_requests.csv takes
too much time to open and often crashes in excel.

NOTE: Requires that all_pull_requests.csv and task5_values.csv have been generated using the main.py
'''
import pandas as pd


def collect_pr_info(output_filename='task6_pr_info.txt'):
    print("Running Title/Info PR collection...")
    all_prs_df = pd.read_csv("all_pull_requests.csv")
    task5_df = pd.read_csv("task5_values.csv")
    
    total_to_validate = 0
    with open(output_filename, 'w') as file:
        for index, row in task5_df.iterrows():
            # Get PR ID to search in all_pull_requests.csv
            pr_id = row['id']
            security_flag = row['security']

            # Pull out the 'title' and 'body' information for the PR
            pr_row = all_prs_df[all_prs_df['id'] == pr_id]
            
            if(len(pr_row) == 1 and security_flag == 1):
                # Make lowercase so we can match what's in main.py
                pr_title = str(pr_row['title'].iloc[0]).lower()
                pr_body = str(pr_row['body'].iloc[0]).lower()

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



if __name__ == "__main__":
    # Collect the PR information and store in a text file
    collect_pr_info()


