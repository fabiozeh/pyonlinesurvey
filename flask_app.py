
from flask import Flask, redirect, render_template, request, url_for, session
from flask.ext.sqlalchemy import SQLAlchemy
from random import shuffle, sample, choice
from string import ascii_uppercase, digits
from numpy import repeat
import MySQLdb as DB

app = Flask(__name__)
app.config["DEBUG"] = True


## Database conection
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="fortega",
    password="telmi2database",
    hostname="fortega.mysql.pythonanywhere-services.com",
    databasename="fortega$expressiveDynamics",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app) #connect to database

## Model: class that specifies the database structure
class Answer(db.Model):

    __tablename__ = "answer"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.relationship('User',backref=db.backref('users', lazy='dynamic'))
    sound_sample = db.Column(db.String(100))
    sound_file_1 = db.Column(db.String(1))
    sound_file_2 = db.Column(db.String(1))

    # answer
    human = db.Column(db.Integer)
    preferred = db.Column(db.Integer)
    distinction = db.Column(db.Integer)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(11))
    nationality = db.Column(db.String(100))
    country = db.Column(db.String(100))
    instrument = db.Column(db.String(100))
    years_study = db.Column(db.Integer)
    hours_practice = db.Column(db.Integer)
    one_to_one_lessons = db.Column(db.Integer)
    if_lessons_years = db.Column(db.Integer)
    musical_genre = db.Column(db.String(100))
    musical_activity = db.Column(db.String(100))
    headphones = db.Column(db.String(100))
    telmi_code = db.Column(db.String(10))
    ## add time to answer and comments in the last page
    ## comments = db.Column(db.String(300)) ##300 characters... enough?
    ## time = db.Column(db.Integer) ## in minutes


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

@app.route('/main_form', methods=["GET", "POST"])# route app to page and allow get and post methods
def main_form():# define main func
#    sound_idx = 2
    soundFileList = session['soundList']
    combination = session['soundComb']

    if request.method == "GET":

        sessionCount = index_handler()#this function handles the counter exception, and redirect to clear the session after reaching the end of the list of sounds
        if len(soundFileList) <= sessionCount:
            return redirect(url_for('clearsession'))
        sessionCount = index_handler()#this function handles the counter exception, and redirect to clear the session after reaching the end of the list of sounds
        sound_idx = sessionCount

        return render_template("main_form.html", answers=Answer.query.all(), users=User.query.all(), soundList = soundFileList, combList = combination, sessionCount=sessionCount, soundListLen = len(soundFileList)) # if method is get just render the page and enable variable comments
        #comments is the variable passed to the html form                                   next:iterate soundFileList           =session['counter']                            This is to debug random order (delete after)
    #else (implicit): method is "post" which means someone press the post button

    sessionCount = index_handler()#this function handles the counter exception, and redirect to clear the session after reaching the end of the list of sounds
    sound_idx = sessionCount

    if len(session['soundList']) < sessionCount:
        return redirect(url_for('clearsession'))

    answer = Answer()
    current_user = User.query.order_by('-id').first() #get last item form user db
    answer.user_id = current_user
    answer.user_name = current_user

    browser_flag = request.form["browser_idx"]
    if browser_flag == '1': #browser is internet explorer
        answer.sound_sample = soundFileList[sound_idx] + ".mp3" #sound list is mp3
    else:
        answer.sound_sample = soundFileList[sound_idx] + ".wav" #sound list is wav

    answer.sound_file_1 = combination[sound_idx][0]
    answer.sound_file_2 = combination[sound_idx][1]
    answer.human = request.form["human"]
    answer.preferred = request.form["preferred"]
    answer.distinction = request.form["distinction"]

    db.session.add(answer)
    db.session.commit()

    sumSessionCounter()


    #sound_idx = sound_idx + 1

    return redirect(url_for('main_form'))

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
        return render_template("form.html") # users=User.query.all() if method is get just render the page and enable variable comments

    #else (implicit): method is "post" which means someone press the next button

    #Load data into the user data base
    request.args.get
    random_id = id_generator()
    session['name'] = request.form["user_name"] + random_id

    user = User()
    user.user_name = request.form["user_name"] + random_id
    user.age = request.form["age"]
    user.gender = request.form["gender"]
    user.nationality = request.form["nationality"]
    user.country = request.form["country"]
    user.instrument = request.form["instrument"]
    user.years_study = request.form["years_study"]
    user.hours_practice = request.form["hours_practice"]
    user.one_to_one_lessons = request.form["one_to_one_lessons"]
    user.if_lessons_years = request.form["if_lessons_years"]
    user.musical_genre = request.form["musical_genre"]
    user.musical_activity = request.form["musical_activity"]
    user.headphones = request.form["headphones"]
    user.telmi_code = request.form["telmi_code"]

    db.session.add(user)
    db.session.commit()

    ## create sound file list
    soundFileList = ["01","02","03","04","05","06","07","08"]
    soundFileList = soundFileList + sample(soundFileList, 4)
    combination = repeat([["a", "b"],["b", "c"]], 5, 0).tolist()
    combination += repeat([["a", "c"]], 2, 0).tolist()

    # Randomize list
    shuffle(soundFileList)
    shuffle(combination)

    # make sure repeated audios don't use same combinations
    aux = set()
    aux.update(map(lambda i: (soundFileList[i],combination[i][0],combination[i][1]), range(len(soundFileList))))
    while len(aux) < len(soundFileList):
        shuffle(soundFileList)
        shuffle(combination)
        aux = set()
        aux.update(map(lambda i: (soundFileList[i],combination[i][0],combination[i][1]), range(len(soundFileList))))

    session['soundList'] = soundFileList
    session['soundComb'] = combination

   # And then redirect the user to the main form
    return redirect(url_for('main_form')) #main_form



#####

@app.route('/clearsession')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return render_template("end_page.html")

def id_generator(size=6, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for _ in range(size))

############ RESULTS ##########
def run_query(query=''):
    datos = ["fortega.mysql.pythonanywhere-services.com", "fortega", "telmi2database", "fortega$expressiveDynamics"]

    conn = DB.connect(*datos) # Conectar a la base de datos
    cursor = conn.cursor()         # Crear un cursor
    cursor.execute(query)          # Ejecutar una consulta

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()   # Traer los resultados de un select
    else:
        #DB.commit()              # Hacer efectiva la escritura de datos
        data = None

    cursor.close()                 # Cerrar el cursor
    #conn.close()                   # Cerrar la conexion

    return data

results = []
@app.route("/results", methods=["GET", "POST"])
def results():
    query = "DROP TABLE IF EXISTS sound_scores;"
    run_query(query)

    query = "CREATE TABLE sound_scores AS SELECT U.user_name, U.age, U.gender, U.nationality, U.country, U.instrument, U.years_study, U.hours_practice, U.one_to_one_lessons, U.if_lessons_years, U.musical_genre, U.musical_activity, U.headphones, D.info, S.id, S.OR_performance_quality, S.OR_technical_competence, S.OR_musicality, S.confidence_peformer, S.quality_tone, S.accuracy_notes_intonation, S.accuracy_rhythms, S.use_dynamics FROM data D, scores S, users U WHERE D.sound_file_wav = S.sound_file AND U.id = S.user_id ORDER BY D.info;"
    run_query(query)

    query = "SELECT * FROM sound_scores;"
    results = run_query(query)
    if request.method == "GET":
        return render_template("results.html", results=results)

    #comments.append(request.form["contents"])
    return redirect(url_for('results'))