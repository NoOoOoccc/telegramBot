# 导入需要的库
import logging
import threading
# 导入网易云音乐爬取脚本
import cloudMusic
# 导入图片处理
import pictureHandle
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
from telegram.ext import ConversationHandler

# 消息回复超时时间
MessageTimeOut = 600
# 异步线程数量
threadWorkers = 8


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
        # 获取文件的字节流
        photo_bytes = photo_file.download_as_bytearray()
        # 转换为jpeg格式
        byte_arr = pictureHandle.pictureToJPEG(photo_bytes)
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
            # 获取歌名
            songName = update.message.audio.title.title()
            # 获取歌手
            singer = update.message.audio.performer
            # 执行获取歌词脚本
            lyc = cloudMusic.getMusicId(singer + ' ' + songName, singer)
            print(lyc)
            update.message.reply_text(lyc, timeout=MessageTimeOut)
        except Exception as e:
            logging.error(e)
            update.message.reply_text('出现错误: {}'.format(e))


# 创建Updater实例，需要提供有效的Telegram bot API token
updater = Updater('6062648071:AAFlgKl1aHftCPy3nkwQ4cIuEZSm0ufHJAM', use_context=True, workers=threadWorkers)

# 将/start和/test命令的处理函数添加到dispatcher
updater.dispatcher.add_handler(MessageHandler(Filters.sticker, photo,run_async=True))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('test', test))
updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.groups, word_of_song, run_async=True))
# 开始监听新的更新
updater.start_polling()

# 使bot保持运行，直到收到停止信号
updater.idle()
