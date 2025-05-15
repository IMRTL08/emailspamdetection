from flask import render_template, request, session, redirect, url_for
from app import app
import pickle
import os

# Load the model and vectorizer
model_path = os.path.join(app.root_path, 'model', 'spam_model.pkl')
vectorizer_path = os.path.join(app.root_path, 'model', 'vectorizer.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        if 'clear' in request.form:
            session['history'] = []
            return redirect(url_for('index'))

        email_text = request.form['email_text']
        transformed = vectorizer.transform([email_text])
        prediction = model.predict(transformed)[0]

        session['history'].append({
            'email': email_text,
            'result': prediction
        })

        session.modified = True  # Make sure Flask knows session was updated

        return render_template('index.html', prediction=prediction, history=session['history'])

    return render_template('index.html', history=session.get('history', []))
