import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Load and preprocess data
data = pd.read_csv('mail_data.csv', encoding='latin-1')[['Category', 'Message']]
data.columns = ['label', 'text']
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# Split dataset
X = data['text']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorization
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

# Model training
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Save the model and vectorizer
os.makedirs('app/model', exist_ok=True)
with open('app/model/spam_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('app/model/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("✅ Model and vectorizer saved successfully.")
