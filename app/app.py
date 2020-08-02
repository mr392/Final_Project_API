from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import Calculator as calc
import Statistics as stats


app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'numberData'
mysql.init_app(app)



# - for old bar charts....delete when no longer needed
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

# -------------------------------------------

@app.route('/', methods=['GET'])
def index():
    bar_values = values
    bar_labels = labels
    user = {'username': 'Mike'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM numberImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, num_result=result, labels=bar_labels, values=bar_values)

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
    user = {'username': 'Mike'}
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
        multiply_result = calc.Calculator.divide(calc.Calculator(), request.form.get('num1'), request.form.get('num2'))
        inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('operation'), str(multiply_result))

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

    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM statsImport')
    result = cursor.fetchall()
    return render_template('stats_index.html', title='Stats', stat_result=result)

@app.route('/stats', methods=['Post'])
def form_stat_post():
    cursor = mysql.get_db().cursor()
    inputData = inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('num3'),request.form.get('num4'),request.form.get('num5'),request.form.get('num6'), request.form.get('operation'))


    mean_result = stats.Statistics.get_mean(stats.Statistics(), request.form.get('num1'), request.form.get('num2'), request.form.get('num3'),request.form.get('num4'),request.form.get('num5'),request.form.get('num6'), request.form.get('operation'))
    inputData = (request.form.get('num1'), request.form.get('num2'), request.form.get('num3'),request.form.get('num4'),request.form.get('num5'),request.form.get('num6'), request.form.get('operation'), str(mean_result))

    sql_insert_query = """INSERT INTO statsImport (num1, num2, num3, num4, num5, num6, operation, result) VALUES (%s, %s,%s, %s, %s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/stats", code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
