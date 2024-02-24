from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
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

if __name__ == '__main__':
    app.run(debug=True)
