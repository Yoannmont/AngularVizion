from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from model.model import process_image, predict_image
import requests
import json

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'upload'
PREDICTIONS_FOLDER = 'predictions'
ALLOWED_EXTENSIONS = {".png", '.jpg', '.jpeg', '.webp', '.gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PREDICTIONS_FOLDER'] = PREDICTIONS_FOLDER

for folder in [UPLOAD_FOLDER, PREDICTIONS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)


#Tools functions
def allowed_file(filename):
    return os.path.splitext(os.path.basename(filename))[1].lower() in ALLOWED_EXTENSIONS

def format_form(data):
    data_keys = [*dict(data).keys()]
    data_values = [*dict(data).values()]
    if len(data_values) == 1 and data_values[0] == '':
        formatted_data = json.loads(data_keys[0])
        return formatted_data
    else :
        return data

@app.post('/predict')
def predict():
    file = request.files.get('file', None)
    formatted_form = format_form(request.form)
    link = formatted_form.get('link', None)
    threshold = float(request.form.get('threshold',0.8))
    print(request.form)
    

    if (file is None or file.filename == ''):
        if (link is None or link==''):
            return jsonify({'error' : 'No file or link found'}), 400
        if not allowed_file(link):
            return jsonify({'error' : 'Extension not allowed'}), 400
        image_filename = secure_filename(os.path.basename(link))
        response = requests.get(link)
        
        file = open(os.path.join(app.config['UPLOAD_FOLDER'],image_filename), "wb+")
        file.write(response.content)
    else :
        if not allowed_file(file.filename):
            return jsonify({'error' : "Extension not allowed"}), 400
        image_filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
    
    try:
        image_filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image, processor = process_image(file)
        
        prediction_filename = f'{os.path.splitext(image_filename)[0]}_prediction{os.path.splitext(image_filename)[1]}'
        prediction_filepath = os.path.join(app.config['PREDICTIONS_FOLDER'], prediction_filename)

        predict_image(image, processor, threshold=threshold, path_to_save_to = prediction_filepath)

        return send_file(prediction_filepath, mimetype='image/gif')
    except Exception as e:
        return jsonify({'error' : e}), 400
    # finally:
        
    #     for path in [image_filepath, prediction_filepath]:
    #         if os.path.exists(path):
    #             os.unlink(path)


if __name__ == "__main__":
    app.run(debug=True)