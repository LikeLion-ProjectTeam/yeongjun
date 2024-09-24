from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'june121284@gmail.com' # Your email
app.config['MAIL_PASSWORD'] = 'oxsb lfgm qxdl zbgg' # Your email password
mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email', methods=['GET', 'POST'])
def email_test():
    if request.method == 'POST':
        sender = request.form['email_sender']
        receiver = request.form['email_receiver']
        content = request.form['email_content']
        receiver = receiver.split(',')

        for i in range(len(receiver)):
            receiver[i] = receiver[i].strip()

        print(receiver)
        result = send_email(sender, receiver, content)
        if not result:
            return render_template('index.html', content="Email is sent")
        else:
            return render_template('index.html', content="Email is not sent")
    else:
        return render_template('index.html')
    
def send_email(sender, receiver, content):
    msg = Message('Title', sender = sender, recipients = receiver)
    msg.body = content
    mail.send(msg)

    return 'Sent email.'

if __name__ == '__main__':
    app.run(debug=True)