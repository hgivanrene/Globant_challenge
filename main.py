from flask import Flask, jsonify
import pandas as pd
import os
from datasets import Department, Job, Employee
from db import init_db, SessionLocal

app = Flask(__name__)

# Initialize the Data Base
init_db()

# Path to the csv files
query_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def save_to_db(model, data):
    session = SessionLocal()
    session.bulk_insert_mappings(model, data)
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

if __name__ == '__main__':
    app.run(debug=True)
