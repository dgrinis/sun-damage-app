from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from simulate import simulate_sun_damage  # Make sure simulate.py exists

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

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

        # Get only the filenames, not full paths
        original_filename = os.path.basename(original_path)
        result_filename = os.path.basename(result_path)

        return render_template('result.html',
                               original_file=f'/static/uploads/{original_filename}',
                               result_file=f'/static/results/{result_filename}')

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
