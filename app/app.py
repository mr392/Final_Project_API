from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect, render_template, url_for, flash
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import Calculator as calc
import Statistics as stats

from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
app.config.from_pyfile('config.cfg')
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

mail = Mail(app)

mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'numberData'
mysql.init_app(app)

#____________USER CLASS____________

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80), unique=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#____________LOGIN / REGISTER FORMS____________

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

#____________INDEX____________

@app.route('/', methods=['GET'])
@login_required
def index():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM numberImport')
    result = cursor.fetchall()
    return render_template('index.html', name=current_user.username, num_result=result)

#____________LOGIN____________

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                if current_user.confirmed:
                    return redirect(url_for('index'))
            return render_template('unconfirmed.html')
        return render_template('invalid.html')
    return render_template('login.html', form=form)

#____________SIGNUP____________

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, confirmed=False)

        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        return render_template('unconfirmed.html')

    return render_template('signup.html', form=form)

#____________CONFIRM____________

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login', 'success')
    else:
        user.confirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return render_template('confirmed.html')

#____________UNCONFIRMED____________

@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('index'))
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')

#____________RESEND____________

@app.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Resending confirmation email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('unconfirmed'))

#____________EXTENSIONS____________

def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return email

#____________LOGOUT____________

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#____________MAIN____________

@app.route('/view/<int:num_id>', methods=['GET'])
def record_view(num_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM numberImport WHERE id=%s', num_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', num_result=result[0])

@app.route('/delete/<int:num_id>', methods=['POST'])
def form_delete_post(num_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM numberImport WHERE id = %s """
    cursor.execute(sql_delete_query, num_id)
    mysql.get_db().commit()
    return redirect("/", code=302)

#____________POSTMAN API's____________

@app.route('/api/numbers', methods=['GET'])
def api_num_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM numberImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

#------------combined
@app.route('/api/numbers', methods=['POST'])
def api_both() -> str:
    cursor = mysql.get_db().cursor()
    content = request.json

    if content['operation'] == "add":
        add_result = calc.Calculator.add(calc.Calculator(), content['num1'], content['num2'])
        inputData = (content['num1'], content['num2'], str(add_result))
        sql_query = """INSERT INTO numberImport (num1, num2, operation, result) VALUES (%s, %s, "add", %s) """

    elif content['operation'] == "subtract":
        subtract_result = calc.Calculator.subtract(calc.Calculator(), content['num1'], content['num2'])
        inputData = (content['num1'], content['num2'], str(subtract_result))
        sql_query = """INSERT INTO numberImport (num1, num2, operation, result) VALUES (%s, %s, "subtract", %s) """

    elif content['operation'] == "multiply":
        multiply_result = calc.Calculator.multiply(calc.Calculator(), content['num1'], content['num2'])
        inputData = (content['num1'], content['num2'], str(multiply_result))
        sql_query = """INSERT INTO numberImport (num1, num2, operation, result) VALUES (%s, %s, "multiply", %s) """

    elif content['operation'] == "divide":
        divide_result = calc.Calculator.divide(calc.Calculator(), content['num1'], content['num2'])
        inputData = (content['num1'], content['num2'], str(divide_result))
        sql_query = """INSERT INTO numberImport (num1, num2, operation, result) VALUES (%s, %s, "divide", %s) """

    elif content['operation'] == "square":
        square_result = calc.Calculator.square(calc.Calculator(), content['num1'])
        inputData = (content['num1'], content['num2'], str(square_result))
        sql_query = """INSERT INTO numberImport (num1, num2, operation, result) VALUES (%s, %s, "square", %s) """

    elif content['operation'] == "sqrt":
        sqrt_result = calc.Calculator.squareroot(calc.Calculator(), content['num1'])
        inputData = (content['num1'], content['num2'], str(sqrt_result))
        sql_query = """INSERT INTO numberImport (num1, num2, operation, result) VALUES (%s, %s, "sqrt", %s) """

    else:
        print("Sorry information is missing!")

    cursor.execute(sql_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/numbers/<int:id>', methods=['DELETE'])
def api_delete(id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM numberImport WHERE id = %s """
    cursor.execute(sql_delete_query, id)
    mysql.get_db().commit()
    resp = Response(status=210, mimetype='application/json')
    return resp

@app.route('/bar',  methods=['GET'])
def bar():
    bar_labels=labels
    bar_values=values
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM numberImport')
    result = cursor.fetchall()
    return render_template('bar_chart.html', title='Summary of Totals', max=100, num_result=result, labels=bar_labels, values=bar_values)

#http requests

@app.route('/', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('operation'))

    if inputData[2] == "add":
       add_result = calc.Calculator.add(calc.Calculator(), request.form.get('num1'), request.form.get('num2'))
       inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('operation'), str(add_result))

    elif inputData[2] == "multiply":
        multiply_result = calc.Calculator.multiply(calc.Calculator(), request.form.get('num1'), request.form.get('num2'))
        inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('operation'), str(multiply_result))

    elif inputData[2] == "divide":
        divide_result = calc.Calculator.divide(calc.Calculator(), request.form.get('num2'), request.form.get('num1'))
        inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('operation'), str(divide_result))

    elif inputData[2] == "square":
        square_result = calc.Calculator.square(calc.Calculator(), request.form.get('num1'))
        inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('operation'), str(square_result))

    elif inputData[2] == "sqrt":
        sqrt_result = calc.Calculator.squareroot(calc.Calculator(), request.form.get('num1'))
        inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('operation'), str(sqrt_result))

    else:
        subtract_result = calc.Calculator.subtract(calc.Calculator(), request.form.get('num1'), request.form.get('num2'))
        inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('operation'), str(subtract_result))


    sql_insert_query = """INSERT INTO numberImport (num1, num2, operation, result) VALUES (%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

#stats

@app.route('/stats', methods=['GET'])
def stat_index():
    cursor_all= mysql.get_db().cursor()
    cursor_all.execute('SELECT * FROM statsImport')
    result = cursor_all.fetchall()


    cursor_mean = mysql.get_db().cursor()
    cursor_mean.execute('SELECT * FROM statsImport where operation = "mean"')
    mean_result = cursor_mean.fetchall()

    median_cursor = mysql.get_db().cursor()
    median_cursor.execute('SELECT * FROM statsImport where operation = "median"')
    median_result = median_cursor.fetchall()

    devcursor = mysql.get_db().cursor()
    devcursor.execute('SELECT * FROM statsImport where operation = "deviation"')
    dev_result = devcursor.fetchall()

    var_cursor = mysql.get_db().cursor()
    var_cursor.execute('SELECT * FROM statsImport where operation = "variance"')
    var_result = var_cursor.fetchall()



    return render_template('stats_index.html', title='Stats', deviation_count = dev_result, median_count=median_result, mean_count=mean_result, stat_result=result, var_result = var_result)

@app.route('/stats', methods=['Post'])
def form_stat_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('num3'),request.form.get('num4'),request.form.get('num5'),request.form.get('num6'), request.form.get('operation'))

    if inputData[6] == "mean":
        mean_result = stats.Statistics.get_mean(stats.Statistics(),inputData[0:5])
        inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('num3'),request.form.get('num4'),request.form.get('num5'),request.form.get('num6'), request.form.get('operation'), str(mean_result))
    elif inputData[6] == "median":
        median_result = stats.Statistics.get_median(stats.Statistics(), inputData[0:5])
        inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('num3'), request.form.get('num4'),request.form.get('num5'), request.form.get('num6'), request.form.get('operation'), str(median_result))
    elif inputData[6] == "deviation":
        deviation_result = stats.Statistics.get_standard_deviation(stats.Statistics(), inputData[0:5])
        inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('num3'), request.form.get('num4'),
                     request.form.get('num5'), request.form.get('num6'), request.form.get('operation'), str(deviation_result))
    elif inputData[6] == "variance":
        variance_result = stats.Statistics.get_variance(stats.Statistics(), inputData[0:5])
        inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('num3'), request.form.get('num4'),
                     request.form.get('num5'), request.form.get('num6'), request.form.get('operation'), str(variance_result))

    else:
        pass


    sql_insert_query = """INSERT INTO statsImport (num1, num2, num3, num4, num5, num6, operation, result) VALUES (%s, %s,%s, %s, %s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/stats", code=302)


@app.route('/stats/view/<int:num_id>', methods=['GET'])
def stat_record_view(num_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM statsImport WHERE id=%s', num_id)
    result = cursor.fetchall()
    return render_template('stats_view.html', title='View Form', num_result=result[0])

@app.route('/stats_delete/<int:num_id>', methods=['POST'])
def stats_delete_post(num_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM statsImport WHERE id = %s """
    cursor.execute(sql_delete_query, num_id)
    mysql.get_db().commit()
    return redirect("/stats", code=302)



  #---stats postman api
@app.route('/api/stats', methods=['GET'])
def api_stats_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM statsImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp



@app.route('/api/stats', methods=['POST'])
def api_stats_post() -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['num1'], content['num2'], content['num3'], content['num4'],
                 content['num5'], content['num6'], content['operation'])

    if content['operation'] == 'mean':
       mean_result = stats.Statistics.get_mean(stats.Statistics(), inputData[0:5])
       inputData = (content['num1'], content['num2'], content['num3'], content['num4'],
                 content['num5'], content['num6'], str(mean_result))
       sql_query = """INSERT INTO statsImport (num1, num2, num3, num4, num5, num6, operation, result) VALUES (%s,%s,%s,%s,%s,%s,'mean',%s) """

    elif content['operation'] == 'median':
        median_result = stats.Statistics.get_median(stats.Statistics(), inputData[0:5])
        inputData = (content['num1'], content['num2'], content['num3'], content['num4'],
                     content['num5'], content['num6'], str(median_result))
        sql_query = """INSERT INTO statsImport (num1, num2, num3, num4, num5, num6, operation, result) VALUES (%s,%s,%s,%s,%s,%s,'median',%s) """

    elif content['operation'] == 'deviation':
        deviation_result = stats.Statistics.get_standard_deviation(stats.Statistics(), inputData[0:5])
        inputData = (content['num1'], content['num2'], content['num3'], content['num4'],
                     content['num5'], content['num6'], str(deviation_result))
        sql_query = """INSERT INTO statsImport (num1, num2, num3, num4, num5, num6, operation, result) VALUES (%s,%s,%s,%s,%s,%s,'deviation',%s) """

    elif content['operation'] == 'variance':
        variance_result = stats.Statistics.get_variance(stats.Statistics(), inputData[0:5])
        inputData = (content['num1'], content['num2'], content['num3'], content['num4'],
                     content['num5'], content['num6'], str(variance_result))
        sql_query = """INSERT INTO statsImport (num1, num2, num3, num4, num5, num6, operation, result) VALUES (%s,%s,%s,%s,%s,%s,'variance',%s) """



    cursor.execute(sql_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/stats/<int:id>', methods=['DELETE'])
def api_stats_delete(id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM statsImport WHERE id = %s """
    cursor.execute(sql_delete_query, id)
    mysql.get_db().commit()
    resp = Response(status=210, mimetype='application/json')
    return resp

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)