from flask import Flask, render_template, request
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_url_path='/static')
CORS(app)

# Dictionary to store emails
user_emails = {}

# Function to create a file if it doesn't exist
def create_file_if_not_exists(file_path, default_content):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump(default_content, json_file)

# Check if the directory and file exist, create them if not
emails_directory = 'flight_app/emails'
emails_file_path = os.path.join(emails_directory, 'user_emails.json')
create_file_if_not_exists(emails_directory, {})
create_file_if_not_exists(emails_file_path, {})

@app.route('/', methods=['GET', 'POST'])
def home():
    message = None  # Initialize the message variable

    if request.method == 'POST':
        email = request.form.get('email')
        action = request.form.get('action')

        if action == 'register' and email:
            # Categorize the email
            email_category = 'GMAIL' if 'gmail' in email.casefold() else 'INVALID'

            # Store the email in the dictionary
            user_emails[email] = email_category

            # Save the emails to a JSON file
            with open(emails_file_path, 'w') as json_file:
                json.dump(user_emails, json_file)

            message = 'Registration successful!'

        elif action == 'delete' and email in user_emails:
            # Remove the email entry
            del user_emails[email]

            # Save the updated emails to a JSON file
            with open(emails_file_path, 'w') as json_file:
                json.dump(user_emails, json_file)

            message = 'Unsubscribe successful!'

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run()
