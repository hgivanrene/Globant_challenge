# Globant_challenge
This repository is for developing a coding challenge.

The purpose of this challenge is to create a local REST API that must:
    1. Receive historical data from CSV files
    2. Upload these files to the new DB
    3. Be able to insert batch transactions (1 up to 1000 rows) with one request

To solve the challenge I decided to:
    1. Create a file called db.py where I create the database engine. Using sqlalchemy library.

    2. Create a file called datasets.py where I define the DDL's of the main tables (Deparments, Jobs and Hired_employees) with its each constraints for the columns (Primary key, foreign key, autoincrement and the relationships with the other tables).

    3. Finally, I create the local REST API in a file called main.py that creates the logic for the local REST API. Here is where the magic happens. This file is in charge of:
        - Create the API using the library Flask.
        - Call the function init_db() from the db.py file that creates, configure and initialize the session.
        - Call the classes for the creation of the DDL's.
        - Create the function migrate_csv that validates if the CSV file exists and it matches with any of the three tables define in the datasets file.
        - Create the function save_to_db to upload the data in batchs from 1 to 1000. This function is call in the function migrate_csv after the validation of available files.


# Repo clonning
git clone git@github.com:hgivanrene/Globant_challenge.git

# Usage
On your local terminal execute the main python file.
    Example:
        Python3 main.py

Once you execute the main file the API will be waiting for the loading of the data that comes from the CSV files. In another tab in your terminal execute the next commands.

Command to POST from you API:
    curl -X POST http://127.0.0.1:5000/migrate/{name_of_the_csv_file}

    Examples for the principals files of the project:
        curl -X POST http://127.0.0.1:5000/migrate/departments
        curl -X POST http://127.0.0.1:5000/migrate/jobs
        curl -X POST http://127.0.0.1:5000/migrate/hired_employees