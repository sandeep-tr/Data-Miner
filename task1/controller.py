# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, jsonify
import model as app_data

task1 = Blueprint('task1', __name__)

# Home page for Task 1
@task1.route('/')
def home():
    return render_template('task1.html')


# Endpoint to fetch diagnosis codes for a given combination
# of Age and Sex
@task1.route('/data/diagnosis')
def data():
    age_group = int(request.args.get('age_group', '1'))
    sex = int(request.args.get('sex', '1'))
    data = app_data.get_diagnosis_codes(age_group, sex)
    json.dumps(data, use_decimal=True)

    return jsonify(codes = data)

# Endpoint to find metrics for a given combination of
# Age, Sex and Diagnosis
@task1.route('/search')
def search():
    age_group = int(request.args.get('age_group', '1'))
    sex = int(request.args.get('sex', '1'))
    diagnosis = request.args.get('diagnosis')
    
    data = app_data.search(age_group, sex, diagnosis)
    return jsonify(data)

# Provides Top 10 list for different categories
# (Age, Sex, Diagnosis). Cumulative.
@task1.route('/categories')
def categories():
    data = app_data.top_categories()
    
    return jsonify(categories = data)
