# ichorCurate
ichorCurate is a solution curation application to supplement [ichorCNA](https://github.com/broadinstitute/ichorCNA), a tool for estimating the fraction of tumor in cell-free DNA from ultra-low-pass whole genome sequencing (ULP-WGS, 0.1x coverage).

As a Streamlit powered app, ichorCurate allows users to seamlessly monitor, collaborate, and execute ichorCNA optimal solution selection.

## Usage - Accessing the Web App (Fred Hutch Employees Only)
After running ichorCNA and generating the potential solution outputs, you can access the web app [here](https://ichorcurate.fredhutch.org/), or by visiting https://ichorcurate.fredhutch.org/. In order to successfully enter the app, you must be on Fred Hutch servers.

#### Step 1: Logging In
Upon opening the app, you are directed to the Login page, where you enter your HutchNet ID (username) and password.

#### Step 2: Projects Overview
After logging in, you are directed to the Projects Overview page. Here, you will see a summary of all of the projects created, including associated filepaths to the ichorCNA output (Data Path), curation output path (Output Path), as well as metadata about the project curation status. Additionially, you have the option to edit and delete existing projects, as well as create a new project.

To create a new project, enter a name for the project. Next, enter the path to the location of the ichorCNA output data (Data Path). This should be a folder containing a subfolder for each of the samples that was run through ichorCNA. Finally, enter a path for where you want the output curated solutions to be written to (Output Path).

#### Step 3: Curation and Navigation, and Exporting
Next, you are directed to the Tracker Dashboard page, which contains a summary dashboard overview of all of your samples and their curation status. Here, users can chose to begin curation by selecting a sample, or directly export the "default" solution without curating. 

After selecting a sample to curate, you are directed to the Curation page, where you can begin visualizing the CNA plots. Specifically, you can toggle between all potential solutions, zoom in on any chromosome, and select a temporary selected solution for comparison. Additionally, users have the option to select a reference curated solution (from a different sample, perhaps the same patient) to aid in curation. After confirming your selection, you can officially "Set as Curated Solution" to complete the curation, which sends you back to the Tracker Dashboard. 

#### Step 4: Exporting
Back on the Tracker Dashboard, you can select the "export" button to export the curated solution for that sample to the output folder. This will copy over all of the data associated with ONLY the curated solution (not the other potential solutions) and place that in a folder of the sample name, located in the Output Path location. Additionally, you can select the "Export Curation Summary" button to produce a .txt curation summary file, or "Export All Samples" or "Export All Curated Samples" for exporting in bulk.


## Repository Structure
```markdown
├── app/
│   ├── subpages/                                   # Folder containing the python scripts for each page of the app
│   │   ├── curation.py                                 # Python script for curation, namely visualizing and selecting optimal solutions for a sample
│   │   ├── folder_selection.py                         # Python script for the page allowing users to enter the input and output filepaths
│   │   ├── login.py                                    # Python script for the login page, here just a username
│   │   ├── projects_overview.py                        # Python script for managing and summarizing project status
│   │   └── tracker_dashboard.py                        # Python script for tracking the curation status, and providing a dashboard overview and navigation
│   ├── src/                                        # Folder containing the source scripts full supplemental methods
│   │   ├── ldap3_auth.py                               # Python script containing the user module for authentication as a Fred Hutch employee
│   │   └── utils.py                                    # Python script containing a variety of helper functions used throughout the application
│   └── app.py                                      # The main python wrapper for the app
├── Dockerfile                                      # The Dockerfile used to generate the Docker Image for the app
├── .gitignore                                      # git ignore for the repo
├── .dockerignore                                   # docker ignore for the repo
├── .gitlab-ci.yml                                  # gitlab continuous integration file
├── docker-compose.yml                              # docker compose file for deployment
├── README.md                                       # README for the repo
├── LICENSE                                         # License documentation
└── requirements.txt                                # List of dependencies to run the app
```