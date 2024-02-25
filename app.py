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

def get_selected_columns(data):
    # Replace this with the columns you want to display on the output page
    return data[['sex', 'age', 'education', 'IQ']]

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

        patient_info = get_selected_columns(df)
        
        # Predict output using your model
        output = predict_output(df)

        # Pass the output to the HTML template
        return redirect(url_for('output_page', output=output, patient_info=patient_info.to_dict('records')))

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

# @app.route('/doctors/output/<output>')
@app.route('/doctors/output/<output>/<patient_info>')
def output_page(output, patient_info):
    # output_val = output[0]
    output_list = eval(output)
    # selected_columns_list = eval(selected_columns)
    patient_val_list = eval(patient_info)
    # Extract the single value from the list (assuming it's a single-item array)
    output_value = output_list[0] if output_list else None
    # print(output_value)
    # Determine content based on the output value
    if output_value == 1:
        content = "The prediction is 1. The patient is more likely to commit suicide"
    elif output_value == 0:
        content = "The prediction is 0. The patient is less likely to commit suicide"
    else:
        content = "Invalid output value."

    return render_template('output.html', content=content, output=output, patient_info = patient_val_list)


if __name__ == '__main__':
    app.run(debug=True)
