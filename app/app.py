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




labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/', methods=['GET'])
def index():
    bar_values = values
    bar_labels = labels
    user = {'username': 'Mike'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM numberImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, num_result=result, labels=bar_labels, values=bar_values)



#____________POSTMAN API's


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
    user = {'username': 'Mike'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM numberImport')
    result = cursor.fetchall()
    return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=100, num_result=result, labels=bar_labels, values=bar_values)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
