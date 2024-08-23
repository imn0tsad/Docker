from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ['dbname'],
        user=os.environ['dbuser'],
        password=os.environ['dbpassword'],
        host=os.environ['dbhostname'],
        cursor_factory=RealDictCursor
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        note_content = request.form['content']
        if note_content:
            cur.execute('INSERT INTO notes (content) VALUES (%s);', (note_content,))
            conn.commit()
        return redirect(url_for('index'))

    cur.execute('SELECT * FROM notes;')
    notes = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('index.html', notes=notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
