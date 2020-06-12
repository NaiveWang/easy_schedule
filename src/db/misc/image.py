from PIL import Image
from io import BytesIO

def img2bytes(fileobj):
    try:
        img = Image.open(fileobj)
        # proof with image
        buff = BytesIO()
        img.save(buff, format = "JPEG")
        return True, buff.getvalue()
    except Exception:
        return False, None
