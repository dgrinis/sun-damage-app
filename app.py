from flask import Flask, request, render_template
import os
from simulate import simulate_sun_damage  # Make sure this file exists!
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400

        filename = secure_filename(file.filename)
        original_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(original_path)

        result_path = simulate_sun_damage(original_path)
        if result_path is None:
            return 'No face detected.', 400

        return render_template('result.html', original_path='/' + original_path, result_path='/' + result_path)

    return '''
    <!doctype html>
    <title>Sun Damage Simulator</title>
    <h1>Upload a Selfie</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
