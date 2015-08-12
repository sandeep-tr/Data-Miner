# -*- coding: utf-8 -*-

from flask import Blueprint, Response, render_template, jsonify
import os, subprocess, time
from os.path import abspath, dirname

task2 = Blueprint('task2', __name__)

# Home for task 2
@task2.route('/')
def home():
    return render_template('task2.html')

# Endpoint to invoke regression on the dataset.
# Parts of standard output from the subprocess are rendered to the UI.
@task2.route('/regression')
def regression():
    def process():
        command = 'java -jar regression/regressor-0.0.1-SNAPSHOT.jar regression/6339_Dataset_1.csv -Xmx256m -Xms128m'
        proc = subprocess.Popen(command, cwd=r'/var/www/interface', shell=True, stdout=subprocess.PIPE)

        for line in iter(proc.stdout.readline,''):
            yield line.rstrip() + '<br/>'
    
    return Response(process(), mimetype='text/html')
