
from flask import Flask, redirect, render_template, request, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
from random import shuffle, choice
from string import ascii_uppercase, digits
from datetime import datetime
import MySQLdb as DB

app = Flask(__name__)
app.config["DEBUG"] = True


# Database conection
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{xpname}:{password}@{hostname}/{databasename}".format(
    xpname="skynote",
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
    xp_id = db.Column(db.Integer, db.ForeignKey('experiment.id'))
    with_tech = db.Column(db.Integer)
    piece_id = db.Column(db.String(100))
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
    date = db.Column(db.String(100))
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


class PostSurvey(db.Model):

    __tablename__ = "postsurvey"

    id = db.Column(db.Integer, primary_key=True)
    xp_id = db.Column(db.Integer, db.ForeignKey('experiment.id'))
    learn_quickly = db.Column(db.Integer)
    performance = db.Column(db.Integer)
    productivity = db.Column(db.Integer)
    effectiveness = db.Column(db.Integer)
    easier_practice = db.Column(db.Integer)
    useful = db.Column(db.Integer)
    easy_learn = db.Column(db.Integer)
    what_want = db.Column(db.Integer)
    clear = db.Column(db.Integer)
    flexible = db.Column(db.Integer)
    easy_skill = db.Column(db.Integer)
    easy_use = db.Column(db.Integer)
    accurate = db.Column(db.Integer)
    use_again = db.Column(db.Integer)
    recommend = db.Column(db.Integer)
    most_help = db.Column(db.String(500))
    weakness = db.Column(db.String(500))
    improve = db.Column(db.String(500))
    other = db.Column(db.String(500))


class Participant(db.Model):

    __tablename__ = "participant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    email = db.Column(db.String(100))


app.secret_key = 'IQKm8Eh1jTnNBgbdFf/hjMuFv2punyc1'


@app.route('/')
def index():
    # Initialise the counter, or increment it
    # sumSessionCounter()
    return render_template('index.html')


@app.route('/es/')
def index_es():
    return render_template('ES/index.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():

    # Load data into the xp data base
    request.args.get

    part = Participant()
    part.name = request.form["name"]
    part.email = request.form["email"]

    db.session.add(part)
    db.session.commit()

    return make_response("Success")


@app.route('/form')
def form():
    return render_template("form.html")


@app.route('/form-submit', methods=["GET", "POST"])
def form_submit():
    # Load data into the data base
    request.args.get

    xp = Experiment()
    xp.date = datetime.utcnow().isoformat()
    xp.age = request.form["age"]
    xp.gender = request.form["gender"]
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

    session['step'] = 1
    session['xp_id'] = xp.id

    # create sound file list
    piece = ["twinkle", "manha", "cabeza", "silent"]
    # scale = ["Gmaj", "Amin"]  # no more scales
    mode = ["aural", "tech"]

    # Randomize lists
    shuffle(piece)
    # shuffle(scale)
    # shuffle(mode)  # don't shuffle here, order determined by id.

    # The order of exercises will be determined by the xp_id:
    # odd = aural first
    if xp.id % 2 == 0:
        session['exercise'] = list(map(lambda i: (piece[i], piece[i + 2], mode[i]), range(len(mode))))
    else:
        session['exercise'] = list(map(lambda i: (piece[i], piece[i + 2], mode[i]), reversed(range(len(mode)))))

    # And then redirect user to the main experiment
    return redirect(url_for('experiment'))


@app.route('/experiment')
def experiment():
    return render_template("experiment.html")


def piece_name(identifier):
    if identifier == "twinkle":
        return "Twinkle Twinkle Little Star"
    elif identifier == "manha":
        return "Manhã de Carnaval"
    elif identifier == "cabeza":
        return "Por Una Cabeza"
    elif identifier == "silent":
        return "Silent Night"
    elif identifier == "Gmaj":
        return "G Major Scale"
    elif identifier == "Amin":
        return "A Minor Scale"
    else:
        return identifier


@app.route('/xp-steps', methods=["GET", "POST"])
def xp_steps():
    try:
        step = session['step']
        exercise = session['exercise']
    except KeyError:
        return render_template('session_error.html')

    if step == 1:
        return render_template('prerec.html', exercise=piece_name(exercise[0][0]),
                               pct=step / 18)
    elif step == 2:
        return render_template('refpractice.html', exercise=piece_name(exercise[0][0]),
                               mode=exercise[0][2], pct=step / 18)
    elif step == 3:
        return render_template('reftiming.html', exercise=piece_name(exercise[0][0]),
                               audio=exercise[0][0], mode=exercise[0][2], pct=step / 18)
    elif step == 4:
        return render_template('postrec.html', exercise=piece_name(exercise[0][0]),
                               pct=step / 18)
    elif step == 5:
        return render_template('prerec.html', exercise=piece_name(exercise[0][1]),
                               pct=step / 18)
    elif step == 6:
        return render_template('refpractice.html', exercise=piece_name(exercise[0][1]),
                               mode=exercise[0][2], pct=step / 18)
    elif step == 7:
        return render_template('reftiming.html', exercise=piece_name(exercise[0][1]),
                               audio=exercise[0][1], mode=exercise[0][2], pct=step / 18)
    elif step == 8:
        return render_template('postrec.html', exercise=piece_name(exercise[0][1]),
                               pct=step / 18)
    elif step == 9:
        return render_template('prerec.html', exercise=piece_name(exercise[1][0]),
                               pct=step / 18)
    elif step == 10:
        return render_template('refpractice.html', exercise=piece_name(exercise[1][0]),
                               mode=exercise[1][2], pct=step / 18)
    elif step == 11:
        return render_template('reftiming.html', exercise=piece_name(exercise[1][0]),
                               audio=exercise[1][0], mode=exercise[1][2], pct=step / 18)
    elif step == 12:
        return render_template('postrec.html', exercise=piece_name(exercise[1][0]),
                               pct=step / 18)
    elif step == 13:
        return render_template('prerec.html', exercise=piece_name(exercise[1][1]),
                               pct=step / 18)
    elif step == 14:
        return render_template('refpractice.html', exercise=piece_name(exercise[1][1]),
                               mode=exercise[1][2], pct=step / 18)
    elif step == 15:
        return render_template('reftiming.html', exercise=piece_name(exercise[1][1]),
                               audio=exercise[1][1], mode=exercise[1][2], pct=step / 18)
    elif step == 16:
        return render_template('postrec.html', exercise=exercise[1][1],
                               pct=step / 18)
    elif step == 17:
        return render_template('skynoteeval.html', pct=step / 18)
    else:
        return render_template('end_page.html', pct=step / 18)


@app.route('/xp-data', methods=["GET", "POST"])
def xp_data():
    try:
        step = session['step']
        exercise = session['exercise']
    except KeyError:
        return render_template('session_error.html')

    request.args.get
    xp_id = session['xp_id']

    # commit pre test
    if step == 1 or step == 5 or step == 9 or step == 13:
        rec = Rec()
        rec.xp_id = xp_id
        # rec.pre_confidence = request.form["pre_confidence"]
        rec.pre_quality = request.form["pre_quality"]
        rec.pre_technical = request.form["pre_technical"]
        rec.pre_musicality = request.form["pre_musicality"]
        rec.pre_note = request.form["pre_note"]
        rec.pre_rhythm = request.form["pre_rhythm"]
        rec.pre_tone = request.form["pre_tone"]
        rec.pre_dyn = request.form["pre_dyn"]
        rec.pre_art = request.form["pre_art"]
        rec.pre_improve = request.form["pre_improve"]
        if step == 1:
            rec.with_tech = exercise[0][2] == "tech"
            rec.piece_id = exercise[0][0]
            rec.piece_index = 0
        elif step == 5:
            rec.with_tech = exercise[0][2] == "tech"
            rec.piece_id = exercise[0][1]
            rec.piece_index = 1
        elif step == 9:
            rec.with_tech = exercise[1][2] == "tech"
            rec.piece_id = exercise[1][0]
            rec.piece_index = 2
        elif step == 13:
            rec.with_tech = exercise[1][2] == "tech"
            rec.piece_id = exercise[1][1]
            rec.piece_index = 3
        db.session.add(rec)
        db.session.commit()
    elif step == 2 or step == 6 or step == 10 or step == 14:
        # commit start time
        rec = Rec.query.filter_by(xp_id=xp_id, piece_index=((step - 1) // 4)).first()
        rec.time_piece_start = datetime.utcnow().timestamp()
        db.session.commit()
    elif step == 3 or step == 7 or step == 11 or step == 15:
        # commit stop time
        rec = Rec.query.filter_by(xp_id=xp_id, piece_index=((step - 1) // 4)).first()
        rec.time_piece_end = datetime.utcnow().timestamp()
        db.session.commit()
    elif step == 4 or step == 8 or step == 12 or step == 16:
        # commit post test
        rec = Rec.query.filter_by(xp_id=xp_id, piece_index=((step - 1) // 4)).first()
        rec.post_quality = request.form["post_quality"]
        rec.post_technical = request.form["post_technical"]
        rec.post_musicality = request.form["post_musicality"]
        rec.post_note = request.form["post_note"]
        rec.post_rhythm = request.form["post_rhythm"]
        rec.post_tone = request.form["post_tone"]
        rec.post_dyn = request.form["post_dyn"]
        rec.post_art = request.form["post_art"]
        rec.post_improve = request.form["post_improve"]
        rec.post_practice = request.form["post_practice"]
        rec.post_room = request.form["post_room"]
        rec.post_mental = request.form["post_mental"]
        rec.post_physical = request.form["post_physical"]
        db.session.commit()
    elif step == 17:
        # commit skynote eval
        surv = PostSurvey()
        surv.xp_id = xp_id
        surv.learn_quickly = request.form["learn_quickly"]
        surv.performance = request.form["performance"]
        # surv.productivity = request.form["productivity"]
        # surv.effectiveness = request.form["effectiveness"]
        surv.easier_practice = request.form["easier_practice"]
        surv.useful = request.form["useful"]
        # surv.easy_learn = request.form["easy_learn"]
        surv.what_want = request.form["what_want"]
        # surv.clear = request.form["clear"]
        # surv.flexible = request.form["flexible"]
        # surv.easy_skill = request.form["easy_skill"]
        surv.easy_use = request.form["easy_use"]
        surv.accurate = request.form["accurate"]
        surv.use_again = request.form["use_again"]
        surv.recommend = request.form["recommend"]
        surv.most_help = request.form["most_help"]
        surv.weakness = request.form["weakness"]
        surv.improve = request.form["improve"]
        surv.other = request.form["other"]

    session['step'] += 1
    return redirect(url_for('xp_steps'))


#############################################
@app.route('/clearsession')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the xp to the main page
    return render_template("end_page.html")


@app.route('/dummysession')
def dummy_session():
    # Load data into the data base
    session.clear()

    xp = Experiment()
    xp.date = datetime.utcnow().isoformat()
    xp.age = 0

    db.session.add(xp)
    db.session.commit()

    session['step'] = 1
    session['xp_id'] = xp.id

    # create sound file list
    piece = ["twinkle", "manha", "cabeza", "silent"]
    # scale = ["Gmaj", "Amin"]  # no more scales
    mode = ["aural", "tech"]

    # Randomize lists
    shuffle(piece)
    # shuffle(scale)
    # shuffle(mode)  # don't shuffle here, order determined by id.

    # The order of exercises will be determined by the xp_id:
    # odd = aural first
    if xp.id % 2 == 0:
        session['exercise'] = list(map(lambda i: (piece[i], piece[i + 2], mode[i]), range(len(mode))))
    else:
        session['exercise'] = list(map(lambda i: (piece[i], piece[i + 2], mode[i]), reversed(range(len(mode)))))

    # And then redirect user to the main experiment
    return redirect(url_for('experiment'))


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
