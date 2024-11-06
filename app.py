from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'random_secret_key'

def get_db_connection():
    conn = sqlite3.connect('quiz.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        score = 0

        if request.form.get('answers1') == '1':
            score += 20
        if request.form.get('answers2') == '1':
            score += 20
        if request.form.get('answers3') == '1':
            score += 20
        if request.form.get('answers4') == '1':
            score += 20
        if request.form.get('answers5') == '1':
            score += 10
        if request.form.get('answers6') == '1':
            score += 10

        conn = get_db_connection()
        conn.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (username, score))
        conn.commit()
        conn.close()

        session['score'] = score

        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, score FROM scores ORDER BY score DESC LIMIT 1')
    highest_score = cursor.fetchone()

    if highest_score:
        highest_score_value = highest_score['score']
        cursor.execute('SELECT username FROM scores WHERE score = ?', (highest_score_value,))
        top_users = cursor.fetchall()
        top_users_list = [user['username'] for user in top_users]
        top_users_str = ', '.join(top_users_list)
    else:
        top_users_str = "Henüz kimse sınavı tamamlamadı."

    conn.close()

    return render_template('quiz.html', score=session.get('score'), best_score=highest_score_value, top_users=top_users_str)

if __name__ == '__main__':
    app.run(debug=True)
