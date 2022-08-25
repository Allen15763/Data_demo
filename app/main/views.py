from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    print("In Index")
    return render_template('index.html')

@main.route('/d', methods=['GET', 'POST'])
def dash_t():
    print("In Dashboard")
    return render_template('dashboard_temp.html')