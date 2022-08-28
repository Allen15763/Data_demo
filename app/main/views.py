from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from . import main
from .. import db
from ..models import Test_data


@main.route('/', methods=['GET', 'POST'])
def index():
    s = db.session.query(Test_data)\
        .filter(Test_data.Sepal_Length < 5).limit(5).all() # five returned
    return render_template('index.html', data=s)

@main.route('/d', methods=['GET', 'POST'])
def dash_t():
    print("In Dashboard")
    return render_template('dashboard_temp.html')