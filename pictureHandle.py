import io
import os
from PIL import Image
from moviepy.editor import VideoFileClip

webm_path = 'C:/temp/temp.webm'
gif_path = 'C:/temp/temp.gif'

input_file = "C:/temp/input.mp4"
output_file = "C:/temp/output.gif"


def pictureToPNG(photo_bytes):
    img = Image.open(io.BytesIO(photo_bytes))
    img = img.convert("RGBA")
    # 将图片对象转换为字节流
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    # 回复图片
    return byte_arr


def pictureToGIF(tgs_bytes):
    # 将.webm文件保存到临时文件
    with open('C:/temp/temp.webm', 'wb') as f:
        f.write(tgs_bytes)
    print("保存webm文件成功")
    video = VideoFileClip(webm_path)
    video.write_gif(gif_path)
    print("转化webm文件成功")
    # gif_bytes = optimizeGIF(gif_path)
    # 读取.gif文件的字节流
    with open('C:/temp/temp.gif', 'rb') as f:
        gif_bytes = f.read()
    print("读取gif文件成功")
    # 删除临时文件
    os.remove(webm_path)
    os.remove(gif_path)
    print("删除临时文件文件成功")
    return gif_bytes


def videoToGIF(video_bytes: bytes) -> bytes:
    # 将视频字节流保存为临时文件
    with open(input_file, "wb") as file:
        file.write(video_bytes)
    # 转换为GIF格式
    video = VideoFileClip(input_file)
    video.write_gif(output_file)
    gif_bytes = optimizeGIF(output_file)
    # # 读取转换后的GIF文件
    # with open(output_file, 'rb') as gif_file:
    #     gif_bytes = gif_file.read()
    print("GIF文件大小：", len(gif_bytes) / 1024 / 1024, "M")
    # 删除临时文件
    os.remove(input_file)
    os.remove(output_file)
    # 返回转换后的GIF文件字节流
    return gif_bytes


def optimizeGIF(gif_path: str) -> bytes:
    # 打开GIF文件
    gif_image = Image.open(gif_path)
    # 创建一个字节流对象
    optimized_bytes = io.BytesIO()
    # 保存优化后的GIF文件到字节流对象
    gif_image.save(optimized_bytes, format="GIF", save_all=True, optimize=True, compress_level=9)
    # 获取优化后的GIF文件字节流
    optimized_bytes.seek(0)
    optimized_gif_bytes = optimized_bytes.read()
    # 关闭图像对象
    gif_image.close()
    # 返回优化后的GIF文件字节流
    return optimized_gif_bytes
