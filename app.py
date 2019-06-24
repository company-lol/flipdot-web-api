from flask import Flask
from flask import render_template
from flask import request
import paho.mqtt.client as mqtt
import os
app = Flask(__name__)

import paho.mqtt.client as mqtt #import the client1

#broker_address="iot.eclipse.org" #use external broker


def send_mqtt_message(message):
        broker_address=os.environ['BROKER']  # mqtt broker
        topic = os.environ['TOPIC'] # topic that the flipdot sign is listening on
        client = mqtt.Client("FlipdotClient") #create new instance
        client.connect(broker_address) #connect to broker
        client.publish(topic,message) #publish

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
        message = request.form['message']
        send_mqtt_message(message)
        return ("Sent message to sign: " + message)

if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0')
