from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS

from model.model import predict_image
from utils import allowed_file, process_image, plot_to_IOBytes

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Image size limited to 1024 Kb


@app.get('/')
def check_status():
  return "<p style='color:green'> Status : OK</p>"

@app.post('/predict')
def predict():
  '''Use POST method to submit an image file or a link.


  '''
  file = request.files.get('file', None)
  link = request.form.get('link', None)
  threshold = float(request.form.get('threshold', 0.8))
  lang = request.form.get('lang', 'en')

  if (file is None or file.filename == ''):
    if (link is None or link == ''):
      return jsonify({'error': 'No file or link found'}), 400
    if not allowed_file(link):
      return jsonify({'error': 'Extension not allowed'}), 400

  try:
    if file:
      if not allowed_file(secure_filename(file.filename)):
        return jsonify({'error': "Extension not allowed"}), 400
      image = file
    else:
      image = link

    image = process_image(image)
    prediction = predict_image(image, threshold=threshold, lang=lang)
    predictionIOBytes = plot_to_IOBytes(prediction)

    return send_file(predictionIOBytes, mimetype=f'image/png')

  except Exception as e:
    return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)