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
git clone git@github.com:hgivanrene/Globant_challenge.git # This command is when you have your ssh key configured in the repo. This option is quite more safe.
git clone https://github.com/hgivanrene/Globant_challenge.git # This option is to clone the repo using the web URL.


# Docker installation on mac with colima

1. Homebrew installation.
Homebrew is the package manager for macOS and it will help us to install all kinds of things in the future.
To install homebrew we must open the terminal application that comes by default on the mac and perform the following command:

    -/bin/bash -c “$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)”

At the end of running the command it will ask you to run the following two commands which are to add the homebrew to your PATH:

    -(echo; echo 'eval “$(/opt/homebrew/bin/brew shellenv)”') >> /Users/<user_name>/.zprofile.
    *Note: The <user_name> must be changed to the username assigned on your machine.
    -eval “$(/opt/homebrew/bin/brew shellenv)”

2. Once the homebrew is installed we move on to install colima.

    -brew install colima

3. Then we install the Docker client.

    -brew install docker
    -brew install astro

4. Starting colima for the first time
Once we have completed the previous steps we proceed to start colima. The first time we will do it assigning CPU and
MEMORY with the following command.

    -colima start --cpu 4 --memory 6

To start colima on future occasions we would simply pass the command as follows:
    -colima start

To stop colima we do it in the following way:
    -colima stop


# Usage with Docker

Create the image on your local machine
    -docker build -t globant_challenge .

Run the container from your image and define the port that will be use, in this case I use the port 8080. Also, I named my container as code_challenge to access easely.
    -docker run -d -p 8080:8080 --name code_challenge globant_challenge

Check that your container code_challenge is running.
    -docker ps

If your container is running properly that means that your local REST API is running and is available to receive your POST and GET commands.

Once you have your container running it will be waiting for the uploading of the data that comes from the CSV files. In another tab of your terminal execute the next commands.

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

*Note: This commands can be also executed from the Postman platform (https://www.postman.com) if you prefer a UI environment to execute the commands.

Once you use the commands GET on your terminal or Postman platform you can use the URL's http://127.0.0.1:5000/get_requirement/first-requirement and http://127.0.0.1:5000/get_requirement/second-requirement to look for the endpoint response on your prefer browser.