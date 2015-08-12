# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, jsonify
from task3 import model as finder

task3 = Blueprint('task3', __name__)

# Home for task3
@task3.route('/')
def home():
    return render_template('task3.html')

# Endpoint process provided combination of attributes
# and generates association mining rules.
@task3.route('/mine')
def search():
    # read parameters from request object
    support = float(request.args.get('support', '50'))
    confidence = float(request.args.get('confidence', '50'))
    attributes = request.args.get('selected_attributes')    

    data = finder.mine(support, confidence, attributes)
    return jsonify(data = data)
