# Your code goes here!
import psycopg2
import os
import csv

## Let's connect to our database
connection = psycopg2.connect(f"dbname=chicago_salaries user={os.getlogin()}")

## Once a connection has been opened, we are going to open a cursor to run our SQL queries
cursor = connection.cursor()

## Let's create a query to create a students table and execute it
student_table_creation_query = "CREATE TABLE IF NOT EXISTS employees (id serial PRIMARY KEY, first_name varchar,last_name varchar, job_title varchar, full_or_part_time varchar, department varchar, annual_salary numeric(10,2));"
cursor.execute(student_table_creation_query)
connection.commit()

# Pseudo Release 2
"""
1. use csv reader to read from database
2. use a loop to iterate over each row
3. clean data = seperate first/last names
if parttime, use hours_per_week * hourly_salary * 50
4. write sql code to put it into database 

Side-note refactor - clean code by passing cleaned data to a object of each var.
"""
def data_population():
    cleaned = {}
    with open('Employee_data.csv', newline='') as employeeinfo:
        reader = csv.DictReader(employeeinfo)
        employee_id = 0
        for row in reader:
            cleaned['id'] = employee_id
            cleaned['first_name'] = row['Name'].split(',  ')[1]
            cleaned['last_name'] = row['Name'].split(',')[0]
            cleaned['job_title'] = row['Job Titles']
            cleaned['full_or_part_time'] = row['Full or Part-Time']
            cleaned['department'] = row['Department']
            
            if row['Salary or Hourly'] == 'Hourly':
                hours_per_week = float(row['Typical Hours'])
                hourly_salary = float(row['Hourly Rate'])
                cleaned['annual_salary']= round(50 * (hours_per_week * hourly_salary), 2)
            else: 
                cleaned['annual_salary'] = float(row['Annual Salary'])
            print(cleaned)

            employee_id += 1
            
            cursor.execute("Insert into employees (id, first_name,last_name, job_title,full_or_part_time, department, annual_salary) VALUES (%s, %s, %s, %s, %s, %s, %s)", (cleaned['id'],cleaned['first_name'], cleaned['last_name'], cleaned['job_title'], cleaned['full_or_part_time'], cleaned['department'], cleaned['annual_salary']))

data_population()
connection.commit()
cursor.close()
connection.close()

