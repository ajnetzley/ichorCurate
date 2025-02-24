# ichorCurate
ichorCurate is a solution curation application to supplement [ichorCNA](https://github.com/broadinstitute/ichorCNA), a tool for estimating the fraction of tumor in cell-free DNA from ultra-low-pass whole genome sequencing (ULP-WGS, 0.1x coverage).

As a Streamlit powered app, ichorCurate allows users to seamlessly monitor, collaborate, and execute ichorCNA optimal solution selection.

## Usage - Running the App Locally
After running ichorCNA and generating the potential solution outputs, use the following steps to run this application locally. In future versions, we plan to deploy this app on a server, but currently this app must be run through cloning the repository.

### Step 1) App Setup
To start, clone this repository and navigate into the "ichorCurate" folder.

```
git clone https://github.com/ajnetzley/ichorCurate.git
```

Next, create a venv with Python 3.11.5, and use the "requirements.txt" to create a virtual environment to run the application in.

```
python3.11 -m venv ichorCurate_env
source ichorCurate_env/bin/activate
pip install -r requirements.txt
```

### Step 2) Running the App
After navigating to the directory where you cloned the repo and activating the enviroment, execute the following command to start the app.

```markdown
streamlit run app/app.py
```

### Step 3) Logging in and Folder Selection
Upon opening the app, you are directed to the Login page, where you enter a name. Next, you are directed to the Folder Selection page, where you are prompted to enter the path to the location of the ichorCNA output data. This should be a folder containing a subfolder for each of the samples that was run through ichorCNA. Then, optionally, you can input a path for where the output curated solutions will be written to. If you don't enter a path, a folder at your working directory named "curated_solutions/" will be created and used.

### Step 4) Curation, Navigation, and Exporting
Next, you are directed to the Tracker Dashboard page, which contains a summary dashboard overview of all of your samples and their curation status. Here, users can chose to begin curation by selecting a sample, or directly export the "default" solution without curating. 

After selecting a sample to curate, you are directed to the Curation page, where you can begin visualizing the CNA plots. Specifically, you can toggle between all potential solutions, zoom in on any chromosome, and select a temporary selected solution for comparison. Additionally, users have the option to select a reference curated solution (from a different sample, perhaps the same patient) to aid in curation. After confirming your selection, you can officially "Set as Curated Solution" to complete the curation, which sends you back to the Tracker Dashboard. 

After curating, you can select the "export" button to export the curated solution for that sample to the output folder. Additionally, you can select the "Export Curation Summary" button to produce a .txt curation summary file, or "Export All Samples" or "Export All Curated Samples" for exporting in bulk.


## Repository Structure
```markdown
├── app/
│   ├── pages/                                      # Folder containing the python scripts for each page of the app
│   │   ├── curation.py                                 # Python script for curation, namely visualizing and selecting optimal solutions for a sample
│   │   ├── folder_selection.py                         # Python script for the page allowing users to enter the input and output filepaths
│   │   ├── login.py                                    # Python script for the login page
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
ichorCurate is developed by Alexander Netzley, on behalf of the Gavin Ha Lab at Fred Hutchinson Cancer Center
