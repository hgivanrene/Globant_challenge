from flask import Flask, jsonify, Response
import pandas as pd
import os
from datasets import Department, Job, Employee # Create the DDL's
from db import init_db, SessionLocal
import sqlite3
from tabulate import tabulate

app = Flask(__name__)

# Creates, configure and initialize the db session
init_db()

# Path to the csv files
query_base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Data')

def save_to_db(model, data, batch_size=1000):
    session = SessionLocal()

    # Insert of data in batches from 1 to 1000
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        session.bulk_insert_mappings(model, batch)
    
    session.commit()
    session.close()

@app.route('/migrate/<table_name>', methods=['POST'])
def migrate_csv(table_name):
    file_path = os.path.join(query_base_path, f'{table_name}.csv')
    
    if not os.path.exists(file_path):
        return jsonify({'error': f'{table_name}.csv not found in the data directory'}), 400
    
    # Read the CSV file
    df = pd.read_csv(file_path, header=None)
    
    # Choose model based on the table_name
    if table_name == 'departments':
        df.columns = ['id', 'department']
        data = df.to_dict(orient='records')
        save_to_db(Department, data)
    elif table_name == 'jobs':
        df.columns = ['id', 'job']
        data = df.to_dict(orient='records')
        save_to_db(Job, data)
    elif table_name == 'hired_employees':
        df.columns = ['id', 'name', 'datetime', 'department_id', 'job_id']
        data = df.to_dict(orient='records')
        save_to_db(Employee, data)
    else:
        return jsonify({'error': 'Invalid table name'}), 400

    return jsonify({'message': f'{table_name} data loaded successfully'}), 200


@app.route('/get_requirement/first-requirement', methods=['GET'])
def get_first_requirement():
    # Open connection
    conn = sqlite3.connect('globant_challenge.db')
    cursor = conn.cursor()

    # Query for first requirement and execution of the query
    requirement1 = ''' 
                   SELECT D.DEPARTMENT
                          , J.JOB
                          , COUNT(CASE WHEN STRFTIME('%m', HE.DATETIME) IN ('01', '02', '03') THEN HE.ID END) AS Q1
                          , COUNT(CASE WHEN STRFTIME('%m', HE.DATETIME) IN ('04', '05', '06') THEN HE.ID END) AS Q2
                          , COUNT(CASE WHEN STRFTIME('%m', HE.DATETIME) IN ('07', '08', '09') THEN HE.ID END) AS Q3
                          , COUNT(CASE WHEN STRFTIME('%m', HE.DATETIME) IN ('10', '11', '12') THEN HE.ID END) AS Q4
                   FROM HIRED_EMPLOYEES AS HE
                   LEFT JOIN DEPARTMENTS AS D
                       ON HE.DEPARTMENT_ID = D.ID
                   LEFT JOIN JOBS AS J
                       ON HE.JOB_ID = J.ID
                   WHERE 1=1
                   AND STRFTIME('%Y', HE.DATETIME) = '2021'
                   GROUP BY 1, 2
                   ORDER BY 1 ASC, 2 ASC
                   ;
                   '''
    cursor.execute(requirement1)
    requirement1_output = cursor.fetchall()

    # Get the name of the coloumns
    columnas = [description[0] for description in cursor.description]

    # Formatting output using tabulate
    output = tabulate(requirement1_output, headers=columnas, tablefmt='pretty')

    # Close connection
    conn.close()

    # Query output
    return Response(output, mimetype='text/plain')


@app.route('/get_requirement/second-requirement', methods=['GET'])
def get_second_requirement():
    # Open connection
    conn = sqlite3.connect('globant_challenge.db')
    cursor = conn.cursor()

    # Query for second requirement and execution of the query
    requirement2 = ''' WITH BASE AS (
                        SELECT HE.DEPARTMENT_ID
                               , STRFTIME('%Y', HE.DATETIME) AS YEARS
                               , COUNT(DISTINCT HE.ID) AS COUNT_HIRED
                        FROM HIRED_EMPLOYEES AS HE
                        WHERE 1=1
                        GROUP BY 1, 2
                   )

                   , MEAN AS (
                        SELECT YEARS
                               , ROUND(AVG(COUNT_HIRED)) AS MEAN_HIRED_2021
                        FROM BASE
                        WHERE 1=1
                        AND YEARS = '2021'
                        GROUP BY 1
                   )
                   
                    SELECT D.ID
                           , D.DEPARTMENT
                           , COUNT(HE.ID) AS HIRED
                    FROM HIRED_EMPLOYEES AS HE
                    LEFT JOIN DEPARTMENTS AS D
                        ON HE.DEPARTMENT_ID = D.ID
                    GROUP BY 1, 2
                    HAVING HIRED >= (SELECT MEAN_HIRED_2021 FROM MEAN)
               ;
               '''
    cursor.execute(requirement2)
    requirement2_output = cursor.fetchall()

    # Get the name of the coloumns
    columnas = [description[0] for description in cursor.description]

    # Formatting output using tabulate
    output = tabulate(requirement2_output, headers=columnas, tablefmt='pretty')

    # Close connection
    conn.close()

    # Query output
    return Response(output, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
