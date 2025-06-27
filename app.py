# importing needed libraries and classes

from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# load the dotenv environment class to control your project environment into your flask file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'FLASK_SECRET_KEY'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

receiver_email = os.getenv('RECEIVER_EMAIL')

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Compose and send email
        msg = Message(subject='Contact Form Submission',
                      sender=(app.config['MAIL_USERNAME']),
                      recipients=[receiver_email],
                      body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
        # mail.send(msg)
        try:
            mail.send(msg)
            first_name = name.split()[0] if name else "Guest"
            return render_template('thank_you.html', name=first_name)

        except Exception as e:
            print("Mail send error:", str(e))
            flash('Failed to send email. Please try again later.', 'error')

        confirmation = Message(
            subject="Thanks for contacting us!",
            sender= (app.config['MAIL_USERNAME']),
            recipients=[email],  # the sender's email from the form
            body=f"Hi {name},\n\nThanks for reaching out. We'll respond soon!"
        )
        mail.send(confirmation)
        
        # flash('Your message has been sent successfully!', 'success')
        return redirect('/')

    return render_template('contact.html')


print("Receiver:", receiver_email)
print("Username:", app.config['MAIL_USERNAME'])
print("Password is set:", bool(app.config['MAIL_PASSWORD']))

print("MAIL_USERNAME:", app.config['MAIL_USERNAME'])
print("MAIL_PASSWORD:", app.config['MAIL_PASSWORD'])
print("RECEIVER_EMAIL:", receiver_email)
print("Password length:", len(app.config['MAIL_PASSWORD']))


    
if __name__ == '__main__':
    app.run(debug=True)
