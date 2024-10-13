# Globant_challenge
This repository is for developing the Globant's coding challenge

# Repo clonning
git clone git@github.com:hgivanrene/Globant_challenge.git

# Usage
On you local termial on a tab execute the main python file.
    Example:
        Python3 main.py

Once you execute the main file the API will be waiting for the loading of the data that comes from the CSV files. In another tab in your terminal execute the next commands.

Command to POST from you API:
    curl -X POST http://127.0.0.1:5000/migrate/{name_of_the_csv_file}

    Examples for the principals files of the project:
        curl -X POST http://127.0.0.1:5000/migrate/departments
        curl -X POST http://127.0.0.1:5000/migrate/jobs
        curl -X POST http://127.0.0.1:5000/migrate/hired_employees