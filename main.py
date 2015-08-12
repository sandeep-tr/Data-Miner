#Name: Team 9
#Course Number: CSE 6339 Section 003
#Lab Number: 2
'''Copyright (c) 2015'''

# -*- coding: utf-8 -*-

from flask import Flask, render_template
from task1.controller import task1
from task2.controller import task2
from task3.controller import task3
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

app.register_blueprint(task1, url_prefix='/task1')
app.register_blueprint(task2, url_prefix='/task2')
app.register_blueprint(task3, url_prefix='/task3')

# Index page (Home)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    handler = RotatingFileHandler('app_logs.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
