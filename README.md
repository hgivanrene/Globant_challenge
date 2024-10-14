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


In the next section of this challenge the purpose is explore the data that was inserted in the previous section. The stakeholders ask
for some specific metrics they need. Create an end-point for each requirement.

This are the requirements from the stakeholders:

    ● Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.
    ● List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).

To solve this section of the challenge I created a connection to the database to query the data. The way to select the data is using the library sqlite3 that allows to make a connection from the database. I use a variable to save the query and then with the cursor I execute the viarable and in another variable a sabe the ouput from the query. For the name of the columns I use a loop to save the name of the columns and then I change the format of the output using the library tabulate. Finally I use the libray Response to return the HTTP answer from the endpoint to the user in a simple text format.

    1. Create an endpoint that calls the function related to each function.
    2. In the function get_first_requirement I create the query with the logic to get de number of employees hired for each job and department in 2021 divided by quarter and order by department and job ascending. For this requirements I make left joins of the three tables we have in our dataset to complete the requirement. 
    3. In the function get_second_requirement I created the query with the logic to List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments order by the hired employees descending. For this requirement I created a CTE (Base) that count hired employees group by department_id and hiring year. Then I created another CTE (MEAN) that average the count_hired column from the previes CTE group by year and filtered only for 2021 and finally in the last query I made a join between the tables HIRED_EMPLOYEES and DEPARTMENTS to count the hired employees group by department_id and department name and in the end I used a having function just to get the departments with more hires than the mean of employees hired in 2021 for all the departments.


# Repo clonning
git clone git@github.com:hgivanrene/Globant_challenge.git

# Usage
On your local terminal execute the main python file.
    Example:
        Python3 main.py

Once you execute the main file the API will be waiting for the loading of the data that comes from the CSV files. In another tab in your terminal execute the next commands.

Command to resquest a POST to this local REST API project:
    curl -X POST http://127.0.0.1:5000/migrate/{name_of_the_csv_file}

    Examples for the principals files of the project:
        curl -X POST http://127.0.0.1:5000/migrate/departments
        curl -X POST http://127.0.0.1:5000/migrate/jobs
        curl -X POST http://127.0.0.1:5000/migrate/hired_employees


Command to resquest a GET to this local REST API project:
    curl -X GET http://127.0.0.1:5000/get_requirement/{name_of_the_requiremnt}

    Examples to call the endpoints of the requirements from the stakeholders:
        curl -X GET http://127.0.0.1:5000/get_requirement/first-requirement
        curl -X GET http://127.0.0.1:5000/get_requirement/second-requirement

Once you use the commands GET on your terminal you can use the URL's http://127.0.0.1:5000/get_requirement/first-requirement and http://127.0.0.1:5000/get_requirement/second-requirement to look for the endpoint response on your prefer browser.