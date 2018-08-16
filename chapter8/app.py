'''
This app.oy file should be used with the Heroku template in
https://github.com/datademofun/heroku-basic-flask

Add twilio on requirements.txt and replace app.py with this file

See chapter 8 for further detail
'''
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/')
def homepage():
    return 'All working!'


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

    from_number = request.form['From']
    body = request.form['Body']
    resp = MessagingResponse()

    msg = (f'Awwwww! Thanks so much for your message {from_number}, '
           f'"{body}" to you too. ')

    resp.message(msg)
    return str(resp)


if __name__ == '__main__':
    app.run()
