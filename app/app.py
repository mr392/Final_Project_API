from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import Calculator as calc


app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'numberData'
mysql.init_app(app)

@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Mike'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM numberImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, num_result=result)



#____________POSTMAN API's


@app.route('/api/numbers', methods=['GET'])
def api_num_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM numberImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

#----add
@app.route('/api/numbers', methods=['POST'])
def api_add() -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    add_result = calc.Calculator.add(calc.Calculator(), content['num1'], content['num2'])

    inputData = (content['num1'], content['num2'], str(add_result))
    sql_add_query = """INSERT INTO numberImport (num1, num2, operation, result) VALUES (%s, %s, "add", %s) """
    cursor.execute(sql_add_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

#---subtract
@app.route('/api/subtract/numbers', methods=['POST'])
def api_subtract() -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    subtract_result = calc.Calculator.subtract(calc.Calculator(), content['num1'], content['num2'])

    inputData = (content['num1'], content['num2'], str(subtract_result))
    sql_add_query = """INSERT INTO numberImport (num1, num2, operation, result) VALUES (%s, %s, "subtract", %s) """
    cursor.execute(sql_add_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp




result = calc.Calculator.add(calc.Calculator(), 7, 2)
print (result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
