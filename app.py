import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import pickle
from io import StringIO

app = Flask(__name__)

model = pickle.load(open('models/model.pkl', 'rb'))

def predict_output(data):
    # df = pd.read_csv(StringIO(data))
    prediction = model.predict(data)
    return prediction

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/patients')
def patients():
    return render_template('patients.html')

@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/doctors/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            return "No file part"

        file = request.files['csv_file']

        if file.filename == '':
            return "No selected file"

        # Read CSV content as a Pandas DataFrame
        csv_data = file.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))

        # Now 'df' is your Pandas DataFrame, you can use it as needed
        print(df.head())  # Print the first few rows for demonstration

        # Predict output using your model
        output = predict_output(df)

        # Pass the output to the HTML template
        return redirect(url_for('output_page', output=output))

    return render_template('upload_csv.html')


@app.route('/predict',methods=['POST'])
def predict():
    # int_features = [int(x) for x in request.form.values()]
    # features = [np.array(int_features)]
    x=pd.read_csv('C:\Data\DJ\AccioBeer\data\sample2.csv')
    # output_prediction = model.predict(x)  
    prediction = model.predict(x) 
    result = prediction[0]
    print(result)
    # print(1)

    return render_template('predict.html', prediction=result)

@app.route('/doctors/output/<output>')
def output_page(output):
    return render_template('output.html', output=output)


if __name__ == '__main__':
    app.run(debug=True)
