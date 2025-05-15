from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST' and 'email_content' in request.form:
        email_content = request.form.get('email_content', '')
        if email_content.strip():
            result = "Spam" if "buy now" in email_content.lower() else "Not Spam"
            session['history'].append({'email': email_content, 'result': result})
            session.modified = True
    return render_template('index.html', history=session['history'])

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('history', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
