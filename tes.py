import random
import string

digits = "".join( [random.choice(string.digits) for i in range(15)] )
# chars = "".join( [random.choice(string.letters) for i in range(15)] )
print(digits)

import base64
# encoded_string = ''
with open("./temp/123123123.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

print(encoded_string.decode("utf-8"))