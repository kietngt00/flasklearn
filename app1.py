from flask import Flask, render_template, url_for, request, redirect
from flask.wrappers import Request
from flask_mysqldb import MySQL
import yaml
from datetime import datetime

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        task_date = str(datetime.utcnow())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Todo(content, date_created) VALUES(%s,%s)",(task_content, task_date))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    else:
        cur = mysql.connection.cursor()
        tasks = cur.execute("SELECT * FROM Todo ORDER BY date_created")
        tasks = cur.fetchall()
        cur.close()
        return render_template('index.html', tasks = tasks)
    

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Todo WHERE id=%d"%id)
    mysql.connection.commit()
    cur.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        content = request.form['content']
        finish = request.form['finish']
        cur.execute("UPDATE Todo SET content=%s, finish=%s WHERE id=%s",(content, finish, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    else:
        task = cur.execute("SELECT * FROM Todo WHERE id=%d"%id)
        task = cur.fetchall()
        cur.close()
        return render_template('update.html', task=task[0])

if __name__ == "__main__":
    app.run(debug=True)