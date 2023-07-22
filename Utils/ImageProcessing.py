import base64
class ByteImage:
    def __init__(self , file_path):
        self.file_path = file_path


    def getBase64(self):
        with open(self.file_path , "rb") as img_file:
            img_strg = base64.b64encode(img_file.read()).decode("utf-8")

        return img_strg
