import face_recognition
import urllib.request as ur

def face_detect(image1, image2):
  isReal = False
  try:

    image1 = ur.urlopen(image1)
    image2 = ur.urlopen(image2)
    known_obama_image = face_recognition.load_image_file(image1)
    obama_face_encoding = face_recognition.face_encodings(known_obama_image)[0]
    known_encodings = [
      obama_face_encoding,
    ]
    image_to_test = face_recognition.load_image_file(image2)
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]
    face_distances = face_recognition.face_distance(known_encodings, image_to_test_encoding)
    for i, face_distance in enumerate(face_distances):
      if face_distance < 0.6:
          isReal = True
  except Exception as e:
    print("face recog")
    print(e)

  return isReal

