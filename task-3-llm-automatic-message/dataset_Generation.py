# generating dataset of task-1
import pymysql
from faker import Faker

# MySQL connection details
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='manisha',
    database='task-2'
)

# Initialize Faker
fake = Faker()

def insert_random_employees(num_employees):
    try:
        with connection.cursor() as cursor:
            for _ in range(num_employees):
                employee = fake.name()
                salary = fake.random_number(digits=5)  # Random salary, up to 99999
                position = fake.job()
                email = fake.email()
                threshold = fake.random_number(digits=3) / 100  # Random threshold balance
                
                # Insert the record into the table
                cursor.execute("""
                    INSERT INTO employee_data (employee, salary, position, email, threshold)
                    VALUES (%s, %s, %s, %s, %s)
                """, (employee, salary, position, email, threshold))
        
            # Commit changes
            connection.commit()
            print(f"{num_employees} random employees inserted into the table.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        connection.close()

# Generate and insert 100 random employees
insert_random_employees(100)




#generating dataset of task-2

import pymysql
from faker import Faker

# MySQL connection details
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='manisha',
    database='task-2.1'
)

# Initialize Faker
fake = Faker()

def insert_fake_customers(num_customers):
    with connection.cursor() as cursor:
        for _ in range(num_customers):
            name = fake.name()
            credit_limit = round(fake.random_number(digits=5), 2)
            threshold = round(fake.random_number(digits=4), 2)
            email = fake.email()
            
            # Insert the fake customer data into the table
            cursor.execute("""
                INSERT INTO customers (name, credit_limit, threshold, email)
                VALUES (%s, %s, %s, %s)
            """, (name, credit_limit, threshold, email))
        
        # Commit changes
        connection.commit()

# Generate and insert 100 fake customer records
insert_fake_customers(100)

print("Fake customer data inserted into the table.")




