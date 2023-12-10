from flask import Flask, render_template, request
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_url_path='/static')
CORS(app)

# Dictionary to store emails
user_emails = {}


def create_file_if_not_exists(file_path, default_content):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump(default_content, json_file)


# Check if the directory and file exist, create them if not
emails_directory = 'emails'
emails_file_path = os.path.join(emails_directory, 'user_emails.json')
create_file_if_not_exists(emails_directory, {})
create_file_if_not_exists(emails_file_path, {})


def read_user_emails():
    # Read the existing data from the JSON file
    try:
        with open(emails_file_path, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}


def save_user_emails(user_emails):
    # Save the updated dictionary to the JSON file
    with open(emails_file_path, 'w') as json_file:
        json.dump(user_emails, json_file)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        action = request.form.get('action')  # Change 'unsubscribe' or 'register' based on button names

        if email:
            # Read the existing data from the JSON file
            user_emails = read_user_emails()

            # Categorize the email
            email_category = 'GMAIL' if 'gmail' in email.casefold() else 'INVALID'

            # Perform different actions based on the button clicked
            if action == 'unsubscribe':
                # Check if the email is in the dictionary before attempting to remove it
                if email in user_emails:
                    # Remove the email key from the dictionary
                    del user_emails[email]

                    # Save the updated emails to the JSON file
                    save_user_emails(user_emails)

                    return render_template('index.html', message='Unsubscribed successfully!')
                else:
                    # Handle the case where the email is not in the dictionary
                    return render_template('index.html', message='Email not found for unsubscribing.')

            elif action == 'register':
                # Your register logic here
                user_emails[email] = email_category

                # Save the updated emails to the JSON file
                save_user_emails(user_emails)

                return render_template('index.html', message='Registration successful!')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8000)
