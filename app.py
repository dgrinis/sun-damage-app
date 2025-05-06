from flask import Flask, request, render_template, url_for
import os
from werkzeug.utils import secure_filename
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

        result_filename = f"sun_{filename}"
        result_path = os.path.join(RESULT_FOLDER, result_filename)

        # Apply simulation
        success = simulate_sun_damage(original_path, result_path)
        if not success:
            return 'No face detected.', 400

        # Pass relative static paths to the template
        return render_template('result.html',
                               original_image=url_for('static', filename=f'uploads/{filename}'),
                               result_image=url_for('static', filename=f'results/{result_filename}'))

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
