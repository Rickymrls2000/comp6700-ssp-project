# comp6700-ssp-project


# Optional Git API Configuration
To generate a Git Personal Access Token (PAT), primarily for platforms like GitHub, follow these steps:

* Access Settings: Sign in to your GitHub account. Click on your profile picture in the upper-right corner and select "Settings."

* Navigate to Developer Settings: In the left sidebar of the settings page, locate and click on "Developer settings."

* Select Personal Access Tokens: Under "Developer settings," click on "Personal access tokens." You will likely see options for "Tokens (classic)" and "Fine-grained tokens." "Tokens (classic)" are generally sufficient for basic Git operations.

* Generate New Token: Click on "Generate new token" and then select "Generate new token (classic)."
Configure Token Details: Note: Provide a descriptive name for your token (e.g., "CLI Access," "Automation Script").

* Expiration: Set an expiration date for the token. While "No expiration" is an option, it is recommended to set an expiration for security reasons.
* Scopes: Select the necessary scopes or permissions for the token. For common Git operations like cloning, pushing, and pulling repositories, the repo scope is typically required. Grant only the minimum necessary permissions following the principle of least privilege.