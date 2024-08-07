import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from langchain_community.chat_models import ChatOllama

# MySQL connection details
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='manisha',
    database='task-2'
)

# Email configuration
smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server
smtp_port = 587  # Port for TLS
smtp_user = 'manishakhadka228@gmail.com'
smtp_password = 'rruz pvds gefd pmkm'
sender_email = 'manishakhadka228@gmail.com'



# Initialize the LLaMA model
llm = ChatOllama(model="llama3", temperature=1)

def generate_welcome_message(name, position):
    # Create a prompt for the LLaMA model
    prompt = f"Create a complete, personalized welcome message for a new employee named {name}, who is a {position}.
      Ensure the message is direct, starting with a warm greeting, and concludes with 'Best regards, HR Department'.
        Avoid any introductory phrases like 'Here is a personalized message."
    
    # Get response from the LLaMA model
    response = llm.invoke(prompt)
    
    # Return the content of the response
    return response.content


def save_message_to_file(message, file_path):
    with open(file_path, 'a') as file:
        file.write(message + '\n\n')

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

def check_new_employee_logs():
    with connection.cursor() as cursor:
        # Select new logs from the employee_log table
        cursor.execute("""
            SELECT employee_id, employee, position,email 
            FROM employee_log
            WHERE processed = FALSE
        """)
        new_logs = cursor.fetchall()

        # Generate, save, and send messages for each log entry
        for employee_id, name, position, email in new_logs:
            message = generate_welcome_message(name, position)
            print(message)
            send_email(email, "Welcome to the Company!", message)
            save_message_to_file(message, 'welcome_messages.txt')
            
            # Mark the log entry as processed
            cursor.execute("""
                UPDATE employee_log
                SET processed = TRUE
                WHERE employee_id = %s
            """, (employee_id,))
        
        # Commit changes
        connection.commit()

        

while True:
    check_new_employee_logs()
    time.sleep(60)  # Check every minute
