import os
from app import app
from flask import render_template, request, redirect, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

static_events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"},
        {"event":"Dylan's Birthday", "date":"2019-06-25"}
    ]

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # for auth

app.config['MONGO_DBNAME'] = 'test'

app.config['MONGO_URI'] = 'mongodb+srv://admin:XedxvTUqAeNeKi4u@cluster0-gyfio.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', events = static_events)


@app.route('/add')
def add():
    user = mongo.db.users
    user.insert({'name':'Dylan'})
    return 'Added User!'

@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    if request.method == "GET":
        return render_template('new_event.html')
    else:
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        user_name = request.form['user_name']

        events = mongo.db.events
        events.insert({'event': event_name, 'date': event_date, 'user': user_name})
        return redirect('/')

@app.route('/events')
def events():
	collection = mongo.db.events
	events = collection.find({}).sort('date', 1).limit(5)

	return render_template('events.html', events=events)

@app.route('/events/<eventID>')
def event(eventID):
	collection = mongo.db.events
	event = collection.find_one({'_id':ObjectId(eventID)})
	return render_template('event.html', event=event)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})
        if(existing_user is None):
            users.insert({'name': request.form['username'], 'password': request.form['password']})
            return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['name']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
