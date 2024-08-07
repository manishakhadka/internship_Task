import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_community.chat_models import ChatOllama
import time
from datetime import datetime, timedelta

# MySQL connection details
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='manisha',
    database='task-2.1'
)

# Email configuration
smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server
smtp_port = 587  # Port for TLS
smtp_user = 'manishakhadka228@gmail.com'
smtp_password = 'rruz pvds gefd pmkm'
sender_email = 'manishakhadka228@gmail.com'

# Initialize the LLaMA model
llm = ChatOllama(model="llama3", temperature=0)

def generate_personalized_message(name, credit_limit, threshold):
    prompt = (
        f"Generate a personalized message for a customer named {name}. "
        f"Ensure the message is direct, starting with a warm greeting. donot include the start statements like Here is a personalized message sort of things. start from greetings."
        f"The customer's credit limit is {credit_limit}, which is below their threshold of {threshold}. "
        f"The message should address the situation and include any necessary information. "
        f"Conclude with 'Best regards, Customer Service'. Do not include any placeholders or incomplete sentences."
    )
    
    response = llm.invoke(prompt)
    return response.content

def send_email(to_email, subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, to_email, message.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def save_message_to_db(customer_id, message):
    with connection.cursor() as cursor:
        # Insert the generated message into the messages table
        cursor.execute("""
            INSERT INTO customer_messages (customer_id, message)
            VALUES (%s, %s)
        """, (customer_id, message))
        
        # Commit changes
        connection.commit()

def process_customers():
    with connection.cursor() as cursor:
        # Select customers whose credit_limit is below their threshold
        cursor.execute("""
            SELECT customer_id, name, credit_limit, threshold, email, last_notified 
            FROM customers
            WHERE credit_limit < threshold
        """)
        customers = cursor.fetchall()

        for customer_id, name, credit_limit, threshold, email, last_notified in customers:
            # Check if enough time has passed since the last notification
            if last_notified is None or datetime.now() - last_notified > timedelta(hours=12):
                # Generate the personalized message
                message_body = generate_personalized_message(name, credit_limit, threshold)
                print(message_body)
                subject = "Important Information Regarding Your Credit Limit"

                # Send the email
                send_email(email, subject, message_body)

                # Save the message to the database
                save_message_to_db(customer_id, message_body)

                # Update the last_notified timestamp
                cursor.execute("""
                    UPDATE customers
                    SET last_notified = NOW()
                    WHERE customer_id = %s
                """, (customer_id,))
                connection.commit()

while True:
    process_customers()
    time.sleep(60)  # Check every minute
