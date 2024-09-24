from flask import Flask, request, url_for, redirect, render_template
import pickle
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Load the pre-trained model
model = pickle.load(open('model.pkl', 'rb'))

def send_email(to_email, subject, body):
    sender_email = "huzaifaarain424@gmail.com"
    sender_password = "ngqs jcms itld ycnc"

    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # HTML Email Template
    email_body = f"""
    <html>
        <body>
            <h2 style="color: red;">⚠️ Forest Fire Alert ⚠️</h2>
            <p>Dear Forest Manager,</p>
            <p>We have detected a high probability of a forest fire in your area. Based on the current model prediction, the probability of fire occurring is <strong>{body}%</strong>.</p>
            <p>Please take immediate precautions to ensure the safety of your forest and personnel.</p>
            <p style="color: red; font-weight: bold;">⚠️ Action Required: Ensure fire safety protocols are in place.</p>
            <p>Stay alert and follow up with the local authorities if necessary.</p>
            <br>
            <p>Best regards,</p>
            <p><strong>Your Forest Monitoring System</strong></p>
        </body>
    </html>
    """

    msg.attach(MIMEText(email_body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/')
def hello_world():
    return render_template("forest_fire.html")


@app.route('/charts')
def charts():
    return render_template("charts.html")


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final = [np.array(int_features)]
    print(int_features)
    print(final)
    prediction = model.predict_proba(final)
    output = '{0:.{1}f}'.format(prediction[0][1], 2)

    if output > str(0.5):
        # Send email alert
        send_email(
            to_email="huzaifaarain404@gmail.com",  # Replace with recipient's email
            subject="Forest Fire Alert",
            body=f"Alert: Your Forest is in Danger!\nProbability of fire occurring is {output}"
        )
        return render_template('forest_fire.html', pred='Your Forest is in Danger.\nProbability of fire occurring is {}'.format(output), out="Forest is not safe")
    else:
        return render_template('forest_fire.html', pred='Your Forest is safe.\nProbability of fire occurring is {}'.format(output), out="Your Forest is Safe for now")


if __name__ == '__main__':
    app.run(debug=True)
