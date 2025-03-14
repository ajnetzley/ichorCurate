# ichorCurate
ichorCurate is a solution curation application to supplement [ichorCNA](https://github.com/broadinstitute/ichorCNA), a tool for estimating the fraction of tumor in cell-free DNA from ultra-low-pass whole genome sequencing (ULP-WGS, 0.1x coverage).

As a Streamlit powered app, ichorCurate allows users to seamlessly monitor, collaborate, and execute ichorCNA optimal solution selection.

## Usage - Running the App Locally
After running ichorCNA and generating the potential solution outputs, use the following steps to run this application locally.

### App Setup & Launching the App
To start, clone this repository and navigate into the "ichorCurate" folder. Specifically, external users will want to clone the "external" branch.

```
git clone --single-branch --branch external https://github.com/ajnetzley/ichorCurate.git

```

Next, create a venv with Python 3.11.5, and use the "requirements.txt" to create a virtual environment to run the application in.

```
python3.11 -m venv ichorCurate_env
source ichorCurate_env/bin/activate
pip install -r requirements.txt
```

After navigating to the directory where you cloned the repo and activating the enviroment, execute the following command to start the app.

```markdown
streamlit run app/app.py
```

Then, copy and paste either of Local, Network, or External URL into your browser to enter the app.

### Using The App

#### Step 1: Logging in and Connecting to a Backend
Upon opening the app, you are directed to the Login page, where you enter your name or username to be associated with your curation. If necessary to your organization, this would be where you would add in a user module for authentification.

#### Step 2: Connecting to a Backend
Next, you are directed to the Backend Selection page. 

If you are the first person in your organization to use the clone the app and use the repo, you will need to enter a new folder location. This folder location will then hold the metadata for your organization's instance of the app, allowing persistence between session and collaborations between users. The input folder path should be to:
- A location that is readable and writable by all other members of your team that may want to access it
- A stable location that will (hopefully) not get deleted or moved

If someone else in your organization that you wish to collaborate with has already cloned the repo, then at this stage you should enter the filepath they used, and point towards their backend folder.

#### Step 3: Projects Overview
After logging in and connecting to a backend, users are directed to the Projects Overview page. Here, you will see a summary of all of the projects you have created, including associated filepaths to the ichorCNA output (Data Path), curation output path (Output Path), as well as metadata about the project curation status. Additionially, you have the option to edit and delete existing projects, as well as create a new project.

To create a new project, enter a name for the project. Next, enter the path to the location of the ichorCNA output data (Data Path). This should be a folder containing a subfolder for each of the samples that was run through ichorCNA. Finally, enter a path for where you want the output curated solutions to be written to (Output Path).

#### Step 4: Curation and Navigation, and Exporting
Next, you are directed to the Tracker Dashboard page, which contains a summary dashboard overview of all of your samples and their curation status. Here, users can chose to begin curation by selecting a sample, or directly export the "default" solution without curating. 

After selecting a sample to curate, you are directed to the Curation page, where you can begin visualizing the CNA plots. Specifically, you can toggle between all potential solutions, zoom in on any chromosome, and select a temporary selected solution for comparison. Additionally, users have the option to select a reference curated solution (from a different sample, perhaps the same patient) to aid in curation. After confirming your selection, you can officially "Set as Curated Solution" to complete the curation, which sends you back to the Tracker Dashboard. 

#### Step 5: Exporting
Back on the Tracker Dashboard, you can select the "export" button to export the curated solution for that sample to the output folder. This will copy over all of the data associated with ONLY the curated solution (not the other potential solutions) and place that in a folder of the sample name, located in the Output Path location. Additionally, you can select the "Export Curation Summary" button to produce a .txt curation summary file, or "Export All Samples" or "Export All Curated Samples" for exporting in bulk.


## Repository Structure
```markdown
├── app/
│   ├── subpages/                                   # Folder containing the python scripts for each page of the app
│   │   ├── backend_selection.py                        # Python script for selecting a location to hold the backend config files
│   │   ├── curation.py                                 # Python script for curation, namely visualizing and selecting optimal solutions for a sample
│   │   ├── folder_selection.py                         # Python script for the page allowing users to enter the input and output filepaths
│   │   ├── login.py                                    # Python script for the login page, here just a username
│   │   ├── projects_overview.py                        # Python script for managing and summarizing project status
│   │   └── tracker_dashboard.py                        # Python script for tracking the curation status, and providing a dashboard overview and navigation
│   ├── src/                                        # Folder containing the source scripts full supplemental methods
│   │   └── utils.py                                    # Python script containing a variety of helper functions used throughout the application
│   └── app.py                                      # The main python wrapper for the app
├── Dockerfile                                      # The Dockerfile used to generate the Docker Image for the app
├── README.md                                       # README for the repo
├── LICENSE                                         # License documentation
├── .gitignore                                      # git ignore for the repo
└── requirements.txt                                # List of dependencies to run the app
```

## Acknowledgments
ichorCurate is developed by Alexander Netzley, on behalf of the Gavin Ha Lab at Fred Hutch Cancer Center. A special thanks to Dan Tenenbaum, Patty Galipeau, Pooja Chandra, and Gavin Ha for their assistance and support throughout this project.
