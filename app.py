import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email', methods=['GET', 'POST'])
def email_test():
    if request.method == 'POST':
        # Get email details
        subject = request.form['email_subject']
        sender = request.form['email_sender']
        receiver = request.form['email_receiver']
        content = request.form['email_content']
        # Split multiple email addresses
        receiver = [email.strip() for email in receiver.split(',')]

        result = send_email(subject, sender, receiver, content)
        
        if result:
            # Print "Email is sent" on the webpage if the email is sent successfully
            return render_template('index.html', content="Email is sent")
        else:
            # Print "Email is not sent" on the webpage if the email is not sent
            return render_template('index.html', content="Email is not sent")
    else:
        return render_template('index.html')
    
def send_email(subject, sender, receiver, content):
    try:
        # Get email content
        msg = Message(subject=subject, sender=sender, recipients=receiver)
        msg.body = f"From: {sender}\n\n{content}"

        # Send email
        mail.send(msg)
        
        print('Email sent')
        return True
    
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)