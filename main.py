import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

load_dotenv()  # This loads the env vars from .env

def fetch_news(api_key):
    url = f"{BASE_URL}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json()['articles']
    titles = [article['title'] for article in articles]
    return titles

def send_email(news_list, sender_email, receiver_email, password):
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Daily News Digest'  # The subject line
    
    # The body and the attachments for the mail
    message.attach(MIMEText('\n'.join(news_list), 'plain'))
    
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_email, password)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_email, receiver_email, text)
    session.quit()

if __name__ == "__main__":
    EMAIL = os.getenv('EMAIL')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    BASE_URL = os.getenv('BASE_URL')

    news = fetch_news(NEWS_API_KEY)
    send_email(news, EMAIL, RECEIVER_EMAIL, EMAIL_PASSWORD)