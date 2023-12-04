import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
# Email credentials
def send_email(path):
    sender_email = os.environ.get("SENDER_EMAIL") #Enter Sender Email Address Here
    receiver_email = os.environ.get("RECEIVER_EMAIL") #Enter Sender Email Address Here
    password = os.environ.get("SENDER_PASSWORD") #Enter Sender Email Password Here

    # Read text from file
    with open(path, 'r') as file:
        file_content = file.read()

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Text File Content"

    # Attach the text file content
    msg.attach(MIMEText(file_content, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    path = "./summaries/26-11-2023_17-01_summary.txt"
    send_email(path)
