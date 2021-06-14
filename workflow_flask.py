
from flask import Flask, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from random import shuffle, choice
from string import ascii_uppercase, digits
import MySQLdb as DB

app = Flask(__name__)
app.config["DEBUG"] = True


# Database conection
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="skynote",
    password="surveydb_pw_",
    hostname="skynote.mysql.eu.pythonanywhere-services.com",
    databasename="skynote$expressionExercise",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)  # connect to database

# Model: class that specifies the database structure
class Rec(db.Model):

    __tablename__ = "recording"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    with_tech = db.Column(db.Integer)
    piece_id = db.Column(db.Integer)
    piece_index = db.Column(db.Integer)
    time_piece_start = db.Column(db.Float)
    time_piece_end = db.Column(db.Float)

    pre_confidence = db.Column(db.Integer)
    pre_quality = db.Column(db.Integer)
    pre_technical = db.Column(db.Integer)
    pre_musicality = db.Column(db.Integer)
    pre_note = db.Column(db.Integer)
    pre_rhythm = db.Column(db.Integer)
    pre_tone = db.Column(db.Integer)
    pre_dyn = db.Column(db.Integer)
    pre_art = db.Column(db.Integer)
    pre_improve = db.Column(db.Integer)

    post_quality = db.Column(db.Integer)
    post_technical = db.Column(db.Integer)
    post_musicality = db.Column(db.Integer)
    post_note = db.Column(db.Integer)
    post_rhythm = db.Column(db.Integer)
    post_tone = db.Column(db.Integer)
    post_dyn = db.Column(db.Integer)
    post_art = db.Column(db.Integer)
    post_improve = db.Column(db.Integer)
    post_practice = db.Column(db.Integer)
    post_room = db.Column(db.Integer)
    post_mental = db.Column(db.Integer)
    post_physical = db.Column(db.Integer)

    comment = db.Column(db.String(500))

class Experiment(db.Model):

    __tablename__ = "experiment"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(11))
    years_study = db.Column(db.Integer)
    hours_practice = db.Column(db.Integer)
    one_to_one_lessons = db.Column(db.Integer)
    if_lessons_years = db.Column(db.Integer)
    musical_genre = db.Column(db.String(100))
    musical_activity = db.Column(db.String(100))
    plays_reading = db.Column(db.Integer)
    practice_exp = db.Column(db.Integer)


sessionCount = 0

app.secret_key = 'IQKm8Eh1jTnNBgbdFf/hjMuFv2punyc1'


def sumSessionCounter():
  try:
    session['counter'] += 1
  except KeyError:
    session['counter'] = 1


def restSessionCounter():
  try:
    session['counter'] -= 1
  except KeyError:
    session['counter'] = 1


@app.route('/')
def index():
    # Initialise the counter, or increment it
    # sumSessionCounter()
    return render_template('index.html')


def index_handler():
    sumSessionCounter()
    restSessionCounter()
    try:
        sessionCount = session['counter']
    except KeyError:
        sessionCount = 1

    return sessionCount


#############################################
@app.route('/form', methods=["GET", "POST"])
def form():

    if request.method == "GET":
        return render_template("form.html")

    # Load data into the user data base
    request.args.get
    random_id = id_generator()
    session['name'] = request.form["user_name"] + random_id

    xp = Experiment()
    xp.user_name = request.form["user_name"] + random_id
    xp.age = request.form["age"]
    xp.gender = request.form["gender"]
    xp.instrument = request.form["instrument"]
    xp.years_study = request.form["years_study"]
    xp.hours_practice = request.form["hours_practice"]
    xp.one_to_one_lessons = request.form["one_to_one_lessons"]
    xp.if_lessons_years = request.form["if_lessons_years"]
    xp.musical_genre = request.form["musical_genre"]
    xp.musical_activity = request.form["musical_activity"]
    xp.plays_reading = request.form["plays_reading"]
    xp.practice_exp = request.form["practice_exp"]

    db.session.add(xp)
    db.session.commit()

    # create piece list
    piece_list = ["Gscale", "Ascale", "MdeC", "Twinkle"]

    # Randomize list
    shuffle(piece_list)

    session['piece_list'] = piece_list

    # And then redirect the user to the main form
    return redirect(url_for('pre_test'))


@app.route('/clearsession')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return render_template("end_page.html")


def id_generator(size=6, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for _ in range(size))


# ########### RESULTS ##########
def run_query(query=''):
    datos = ["skynote.mysql.eu.pythonanywhere-services.com", "skynote", "surveydb_pw_", "skynote$expressionExercise"]

    conn = DB.connect(*datos)  # Conectar a la base de datos
    cursor = conn.cursor()     # Crear un cursor
    cursor.execute(query)      # Ejecutar una consulta

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()   # Traer los resultados de un select
    else:
        data = None

    cursor.close()                 # Cerrar el cursor

    return data


results = []
