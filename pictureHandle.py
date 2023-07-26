from PIL import Image
import io


def pictureToJPEG(photo_bytes, ):
    img = Image.open(io.BytesIO(photo_bytes))
    # 将图片转换为JPG格式
    img = img.convert('RGB')
    # 将图片对象转换为字节流
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='JPEG')
    byte_arr.seek(0)
    # 回复图片
    return byte_arr
