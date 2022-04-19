import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import easyocr

reader = easyocr.Reader(['en'], True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FILE_DIR = 'files'

app = Flask(__name__)


cwd = os.getcwd()
if not os.path.exists(cwd + '/' + FILE_DIR):
    os.makedirs(cwd + '/' + FILE_DIR)

FILE_DIR = cwd + '/' + FILE_DIR


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/get-text', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = FILE_DIR + '/' + secure_filename(file.filename)
            file.save(filename)
            parsed = reader.readtext(filename)
            text = '<br/>\n'.join(map(lambda x: x[1], parsed))
            # handle file upload
            return jsonify({"result": text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
