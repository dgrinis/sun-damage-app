from flask import Flask, request, render_template
import os
from simulate import simulate_sun_damage
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400

        filename = secure_filename(file.filename)
        original_path = os.path.join(UPLOAD_FOLDER, filename)
        result_path = os.path.join(RESULT_FOLDER, filename)

        file.save(original_path)

        success = simulate_sun_damage(original_path, result_path)
        if not success:
            return 'Simulation failed', 500

        return render_template('result.html',
            original_image=f'uploads/{filename}',
            simulated_image=f'results/{filename}'
        )

    return '''
    <!doctype html>
    <title>Upload Image</title>
    <h1>Upload an image to simulate sun damage</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
