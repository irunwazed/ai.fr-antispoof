from flask import Flask, json, render_template, request, jsonify
from waitress import serve

from flask_cors import CORS, cross_origin
import datetime
import json

import os

import datetime
from antispoof import validate_image, validate_image_file

from face_recog import face_detect
import base64
import subprocess

from PIL import Image

app = Flask(__name__)
cors = CORS(app, origins=["*"] , support_credentials=False)

def send_json(data, status = 200):
  response = app.response_class(
    response=json.dumps(data),
    status=status,
    mimetype='application/json'
  )
  return response
 
@app.route('/')
def home():
  data = {'status': True, 'message': []}
  return send_json(data)


@app.route('/take')
def take():
  data = {'status': True, 'message': []}
  return render_template('index.html')


@app.route('/check-image', methods = ['POST'])
def checkImage():
  try:
    id = request.form.get('id')
    image = request.form.get('image')
    predict, score = validate_image(image,'./resources/anti_spoof_models', 0)
    isReal = False
    if predict == 1:
      isReal = True
    data = {'status': True, "isReal": isReal, "score": score}
    return send_json(data)
  except Exception as e:
    return send_json({'status': False, 'isReal': False, "score": 0})
  


@app.route('/check-image2', methods = ['POST'])
def checkImage2():
  try:
    id = request.form.get('id')
    image = request.form.get('image')
    # print(id)
    
    fileName = "./temp/"+id+".png"
    fileNameCompress = "./temp/compressed_"+id+".png"
    with open(fileName, "wb") as fh:
        fh.write(base64.b64decode(image.split(",")[1]))

    
    image = Image.open(fileName)

    width, height = image.size
    new_size = (width//2, height//2)
    resized_image = image.resize(new_size)

    resized_image.save(fileNameCompress, optimize=True, quality=20)

    predict, score = validate_image_file(fileNameCompress,'./resources/anti_spoof_models', 0)
    os.unlink(fileName)
    os.unlink(fileNameCompress)


    isReal = False
    if predict == 1:
      isReal = True
    data = {'status': True, "isReal": isReal, "score": score}
    
    return send_json(data)
  except Exception as e:
    return send_json({'status': False, 'isReal': False, "score": 0, "errors": str(e)})
  
@app.route('/face-detect', methods = ['POST'])
def api_face_detect():
  try:
    image_src = request.form.get('image_src')
    image_dst = request.form.get('image_dst')
    status = face_detect(image_src, image_dst)

    if status == False:
      return send_json({'status': False, "message": "Muka Tidak Dikenali!"})
    
    return send_json({'status': status})

  except Exception as e:
    return send_json({'status': False})
  

  
@app.route('/face-detect-antispoof', methods = ['POST'])
def api_face_detect_and_antispoof():
  try:
    image_src = request.form.get('image_src')
    image_dst = request.form.get('image_dst')
    if image_src == None:
      image_src = request.json.get('image_src')

    if image_dst == None: 
      image_dst = request.json.get('image_dst')

    # print(question)
    status = face_detect(image_src, image_dst)

    if status == False:
      return send_json({'status': False, "message": "Muka Tidak Dikenali!"})


    predict, score = validate_image(image_src,'./resources/anti_spoof_models', 0)
    
    isReal = False
    if predict == 1:
      isReal = True
    
    if isReal == False:
      return send_json({'status': False, "message": "Menggukanan Foto!"})

    return send_json({'status': status, 'predict': str(predict), 'score': str(score)})
    

  except Exception as e:
    print(e)
    return send_json({'status': False, 'errors':str(e)})

PORT = os.environ.get("ENV_PORT")
if __name__ == '__main__':
  app.run(debug=True, port=9000, host='0.0.0.0')
  # serve(app, host="0.0.0.0", port=9003)