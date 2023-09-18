import pickle
import tempfile
import time
import warnings
from Mail import Mail
from flask import Flask, render_template, request, redirect, url_for, flash, session, Response, jsonify, send_file, \
    make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pandas as pd
from io import BytesIO
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    school_name = db.Column(db.String(120), nullable=False)

    def __init__(self, email, password, address, phone_number, school_name):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.address = address
        self.phone_number = phone_number
        self.school_name = school_name


with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        user = User.query.filter((User.email == email)).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('first_page'))
        else:
            flash('Invalid username/email or password. Please try again.', 'error')

    return render_template('signin.html')


@app.route('/')
def start():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def log():
    return redirect('/login')


# def start():
#     return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        address = request.form['address'].strip()
        phone_number = request.form['phone_number'].strip()
        school_name = request.form['school_name'].strip()

        existing_user = User.query.filter((User.email == email)).first()

        if existing_user:
            flash('Email already exists. Please choose a different one.', 'error')
        else:
            # Use app.app_context() here to access the database within the context
            with app.app_context():
                new_user = User(email=email, password=password, address=address, phone_number=phone_number,
                                school_name=school_name)
                db.session.add(new_user)
                db.session.commit()
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/first_page')
def first_page():
    if 'user_id' in session:
        return render_template('firstpage.html')
    else:
        flash('Please log in to access the first page.', 'error')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    time.sleep(1)
    return redirect(url_for('login'))


@app.route('/predict', methods=['POST'])
def predict():
    try:
        uploaded_file = request.files['file']

        if uploaded_file:
            # Determine the file extension (csv or xlsx)
            filename, file_extension = os.path.splitext(uploaded_file.filename.lower())
            temp_dir = tempfile.mkdtemp()
            temp_file_path = os.path.join(temp_dir, uploaded_file.filename)
            uploaded_file.save(temp_file_path)

            if file_extension in ('.csv', '.xlsx'):
                # Process the uploaded CSV or XLSX file
                # Your machine learning prediction logic goes here
                # Replace this with your actual prediction logic

                with open('best_classifier_with_scaler.pkl', 'rb') as model_file:
                    loaded_model, scaler = pickle.load(model_file)  # Load both the model and scaler

                # Load new data for prediction (replace 'new_data.csv' with your new data file)
                new_data = pd.read_csv(temp_file_path)
                new_data.rename(columns={'Nacionality': 'Nationality', 'Age at enrollment': 'Age'}, inplace=True)
                new_data['Target'] = new_data['Target'].map({
                    'Dropout': 0,
                    'Enrolled': 1,
                    'Graduate': 2
                })
                data = new_data.copy()
                data = data.drop(columns=['Nationality', 'Mother\'s qualification', 'Father\'s qualification',
                                          'Educational special needs', 'International',
                                          'Curricular units 1st sem (without evaluations)',
                                          'Unemployment rate', 'Inflation rate'], axis=1)

                # Drop the 'Target' column from the new data
                data.drop('Target', axis=1, inplace=True)

                # Filter out the specific warning
                warnings.filterwarnings("ignore", category=UserWarning,
                                        message="X has feature names, but StandardScaler was fitted "
                                                "without feature names")

                # Preprocess the new data using the same scaler
                X_new = scaler.transform(data)  # Transform the new data

                # Use the loaded model to make predictions on the new data
                predictions = loaded_model.predict(X_new)

                # Print or use the predictions as needed
                new_data['Predictions'] = predictions
                mapping = {0: 'Dropout', 1: 'Enrolled', 2: 'Graduate'}
                new_data['Target'] = new_data['Target'].map(mapping)
                new_data['Predictions'] = new_data['Predictions'].map(mapping)

                drop_out_dataframe = new_data[new_data['Predictions'] == 'Dropout']
                drop_out_dataframe.to_csv('Dropoutdataframe.csv', index=True, index_label=True)

                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    new_data.to_excel(writer, index=False, sheet_name='Sheet1')

                user_email = session.get('user_email')
                print(f"user email is {user_email}")
                if user_email:
                    if user_email != 'adarshak.731@gmail.com':
                        mail = Mail('adarshak.731@gmail.com', user_email, "kvon jpiz qzbe trkc")
                        mail.send_mail()
                    else:
                        print(f"<adarshak.731@gmail.com> is equal to {user_email}")
                # Reset the pointer of the BytesIO object to the beginning
                output.seek(0)

                # Return the file for download with appropriate headers
                return send_file(output, as_attachment=True, download_name='prediction_result.xlsx',
                                 mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            else:
                return jsonify({'error': 'Unsupported file format'})

        else:
            return jsonify({'error': 'No file provided'})

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        filepath = 'Dropoutdataframe.csv'
        if os.path.exists(filepath):
            try:
                # Delete the file
                os.remove(filepath)
                print(f"File '{filepath}' has been successfully deleted.")
            except OSError as e:
                print(f"Error: {e}")
        else:
            print(f"File '{filepath}' does not exist.")


if __name__ == '__main__':
    app.run(debug=True, port=8000)
