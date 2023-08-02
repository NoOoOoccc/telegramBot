# 导入需要的库
import logging

# 导入网易云音乐爬取脚本
import cloudMusic

# 导入图片处理
import pictureHandle

from telegram import Update
from telegram.ext import Updater, CommandHandler, Filters, CallbackContext, MessageHandler

# 消息回复超时时间
MessageTimeOut = 600
# 异步线程数量
threadWorkers = 8


def mp4ToGif(update: Update, context: CallbackContext) -> None:
    print("接收到视频,进入了mp4ToGif")
    if update.message.document:
        # 获取文件名
        file_name = update.message.document.file_name
        # 获取文件后缀
        file_extension = file_name.split('.')[-1]
        print("文件后缀是:", file_extension)
        if file_extension == "mp4":
            # 获取文件的唯一标识符
            file_id = update.message.document.file_id
            # 使用bot的get_file方法获取文件
            video_file = context.bot.get_file(file_id)
            # 获取文件的字节流
            video_bytes = video_file.download_as_bytearray()
            # 调用videoToGIF函数进行转换
            gif_bytes = pictureHandle.videoToGIF(video_bytes)
            # 发送转换后的GIF文件
            context.bot.send_document(update.message.chat_id, gif_bytes)


def photo(update: Update, context: CallbackContext):
    print("接收到贴纸,进入了photo")
    if update.message.sticker:
        print("开始转换贴纸")
        # 获取贴纸
        sticker = update.message.sticker
        print(sticker)
        # 获取文件ID
        file_id = sticker.file_id
        # 使用bot的get_file方法获取文件
        photo_file = context.bot.get_file(file_id)
        # 获取文件的后缀格式
        file_extension = photo_file.file_path.split('.')[-1]
        print(file_extension)
        # 获取文件的字节流
        photo_bytes = photo_file.download_as_bytearray()
        if file_extension == "webm":
            print("这是一个动态贴纸，格式是.webm")
            # 转换为gif格式
            byte_arr = pictureHandle.pictureToGIF(photo_bytes)
            # 回复图片
            context.bot.send_animation(update.message.chat_id, byte_arr)
        elif file_extension == "webp":
            print("这是一个静态贴纸，格式是.webp")
            # 转换为png格式
            byte_arr = pictureHandle.pictureToPNG(photo_bytes)
            # 回复图片
            context.bot.send_photo(update.message.chat_id, byte_arr)


def start(update: Update, context: CallbackContext) -> None:
    # 当接收到/start命令时，回复'你好，我将狠狠做掉yimouer'
    update.message.reply_text('你好，我将狠狠做掉yimouer')


# 定义/test命令的处理函数
def test(update: Update, context: CallbackContext) -> None:
    # 当接收到/test命令时，回复'测试成功'
    update.message.reply_text('测试成功')


def word_of_song(update: Update, context: CallbackContext) -> None:
    # 如果消息包含音频 根据消息标题获取歌名  到网易云进行搜索爬取歌词
    if update.message.audio is not None:
        try:
            print(update.message.audio)
            # 获取歌名
            songName = update.message.audio.title.title()
            # 获取歌手
            singer = update.message.audio.performer
            # 执行获取歌词脚本
            lyc = cloudMusic.getMusicId(songName, singer)
            print(lyc)
            update.message.reply_text(lyc, timeout=MessageTimeOut)
        except Exception as e:
            logging.error(e)
            update.message.reply_text('出现错误: {}'.format(e))


# 创建Updater实例，需要提供有效的Telegram bot API token
updater = Updater('6062648071:AAFlgKl1aHftCPy3nkwQ4cIuEZSm0ufHJAM', use_context=True,workers=threadWorkers)

# 将/start和/test命令的处理函数添加到dispatcher
updater.dispatcher.add_handler(MessageHandler(Filters.document, mp4ToGif))
updater.dispatcher.add_handler(MessageHandler(Filters.sticker & Filters.private, photo))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('test', test))
updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.groups, word_of_song, run_async=True))

# 开始监听新的更新
updater.start_polling()

# 使bot保持运行，直到收到停止信号
updater.idle()
