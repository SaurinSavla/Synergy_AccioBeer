from flask import Flask, render_template, request

app = Flask(__name__)

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

        # Here, you can process the uploaded CSV file as needed.
        # For simplicity, let's just print the content.
        content = file.read().decode('utf-8')
        print(f"Content of the uploaded CSV file:\n{content}")

        return "File uploaded successfully!"

    return render_template('upload_csv.html')

if __name__ == '__main__':
    app.run(debug=True)
