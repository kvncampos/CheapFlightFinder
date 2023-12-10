from flask import Flask, render_template, request
import json

app = Flask(__name__, static_url_path='/static')

# Dictionary to store emails
user_emails = {}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            if 'gmail' in email.casefold():
                # Store the email in the dictionary
                user_emails[email] = 'GMAIL'  # You can use any value as the 'value' for the email key
            else:
                user_emails[email] = 'INVALID'  # You can use any value as the 'value' for the email key
            # Save the emails to a JSON file
            with open('emails/user_emails.json', 'w') as json_file:
                json.dump(user_emails, json_file)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
