# import subprocess
import sys
import json
import os
from PIL import Image

from antispoof import validate_image_file

try:
    
  fileName = sys.argv[1]
  fileNameCompress = "./temp/compressed_"+sys.argv[2]+".png"

  image = Image.open(fileName)

  width, height = image.size
  new_size = (width//2, height//2)
  resized_image = image.resize(new_size)

  resized_image.save(fileNameCompress, optimize=True, quality=20)

  # original_size = os.path.getsize(fileName)
  # compressed_size = os.path.getsize('compressed_image.jpg')

  # print("Original Size: ", original_size)
  # print("Compressed Size: ", compressed_size)

  # import base64
  # with open(fileName, "wb") as fh:
  #     fh.write(base64.b64decode(img_data.split(",")[1]))


  predict, score = validate_image_file(fileName,'./resources/anti_spoof_models', 0)
  # os.unlink(fileName)


  isReal = False
  if predict == 1:
    isReal = True
  data = {'status': True, "isReal": isReal, "score": score}

  print(json.dumps(data))
except Exception as e:
  data = {'status': False, "isReal": False, "score": 0, "errors": str(e)}
  print(json.dumps(data))


