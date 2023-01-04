from flask import Flask
from flask import render_template
from flask import request
from flipdotapi import remote_sign as sign
import logging

import configparser
import sys
from os import path
app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
        message = request.form['message']
        # send_mqtt_message(message)
        sign.write_text(message, font_name=display_font, fit=False)
        return ("Sent message to sign: " + message)

if __name__ == '__main__':
        formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=formatter)
        logger = logging.getLogger(__name__)

        config = configparser.ConfigParser()
        config_file = 'config.ini'
        if path.exists(config_file):
                config.read(config_file)
        else:
                logging.error("Config file missing: {}".format(config_file))
                sys.exit(1)

        sign_url = config.get('FLIPDOT_SERVER', 'URL')
        sign_columns = config.getint('FLIPDOT_SERVER', 'COLUMNS')
        sign_rows = config.getint('FLIPDOT_SERVER', 'ROWS')
        sign_sim = config.getboolean('FLIPDOT_SERVER', 'SIMULATOR')

        display_font = config.get('DISPLAY', 'FONT')

        sign = sign(sign_url, sign_columns, sign_rows, simulator=sign_sim)

        app.run(debug=True,host='0.0.0.0')
