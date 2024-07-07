from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)

# Database initialization
conn = sqlite3.connect('certificates.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient_name TEXT NOT NULL,
        course_name TEXT NOT NULL,
        hash TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/issue_certificate', methods=['POST'])
def issue_certificate():
    recipient_name = request.form['recipient_name']
    course_name = request.form['course_name']

    # Generate a unique hash for the certificate
    certificate_hash = hashlib.sha256(f'{recipient_name}{course_name}'.encode()).hexdigest()

    # Store certificate details in the database
    conn = sqlite3.connect('certificates.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO certificates (recipient_name, course_name, hash) VALUES (?, ?, ?)',
                   (recipient_name, course_name, certificate_hash))
    conn.commit()
    conn.close()

    return redirect(url_for('view_certificate', hash_value=certificate_hash))

@app.route('/view_certificate/<hash_value>')
def view_certificate(hash_value):
    conn = sqlite3.connect('certificates.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM certificates WHERE hash = ?', (hash_value,))
    certificate = cursor.fetchone()
    conn.close()

    if certificate:
        return render_template('view_certificate.html', certificate=certificate)
    else:
        return "Certificate not found."

if __name__ == '__main__':
    app.run(debug=True)
