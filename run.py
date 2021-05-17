# coding=utf-8

######  欢迎使用脚本任务，首先让我们熟悉脚本任务的一些使用规则  ######
# 脚本任务支持两种运行方式 

# 1.shell 脚本. 在 run.sh 中编写项目运行时所需的命令，并在启动命令框中填写 bash run.sh <参数1> <参数2>使脚本任务正常运行.

# 2.python 指令. 在 run.py 编写运行所需的代码，并在启动命令框中填写 python run.py <参数1> <参数2> 使脚本任务正常运行.

#注：run.sh、run.py 可使用自己的文件替代。

###数据集文件目录
# datasets_prefix = '/root/paddlejob/workspace/train_data/datasets/'

# 数据集文件具体路径请在编辑项目状态下通过左侧导航「数据集」中文件路径拷贝按钮获取
# train_datasets =  '通过路径拷贝获取真实数据集文件路径 '

# 输出文件目录. 任务完成后平台会自动把该目录所有文件压缩为tar.gz包，用户可以通过「下载输出」可以将输出信息下载到本地.
# output_dir = "/root/paddlejob/workspace/output"

# 日志记录. 任务会自动记录环境初始化日志、任务执行日志、错误日志、执行脚本中所有标准输出和标准出错流(例如print()),用户可以在「提交」任务后,通过「查看日志」追踪日志信息.
import os
import cv2
import asyncio
import numpy as np
import paddlehub as hub

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

# 定义model
model = hub.Module(name='animegan_v2_shinkai_33', use_gpu=True)
module = hub.Module(name="ernie_gen_lover_words")
chatService = hub.Module(name='plato-mini')


def img_transform(img_path, img_name):
    """
    img_path: 图片的路径
    img_name: 图片的文件名
    """
    # 图片转换后存放的路径
    img_new_path = './image-new/' + img_name

    # 模型预测
    result = model.style_transfer(images=[cv2.imread(img_path)])

    # 将图片保存到指定路径
    cv2.imwrite(img_new_path, result[0])

    # 返回新图片的路径
    return img_new_path


async def on_message(msg: Message):
    if msg.self():
        return
    room = msg.room()
    print(room)
    
    if room and msg.type() == Message.Type.MESSAGE_TYPE_TEXT:
        
        content = msg.text()
        roomName = await room.topic()
        
        if msg.text() == 'hi' or msg.text() == '你好':
            await msg.say('这是自动回复: 机器人目前的功能是\n- 收到"ding", 自动回复"dong dong dong"\n- 收到"图片", 自动回复一张图片\n- 收到一张图片, 将这张图片转换为动漫风格并返回')
    
        if msg.text() == '情人节':
            test_texts = [ '小编带大家了解一下程序员情人节'];
            results = module.generate(texts=test_texts, use_gpu=True, beam_width=5);
            print("[results]: %s"%results)
            result_text = test_texts[0];
            await msg.say("".join(result_text))
      
        elif roomName == '测试':
            with chatService.interactive_mode(max_turn=3):
                human_utterance = content
                robot_utterance = chatService.predict(human_utterance)[0]
                print("[Bot]: %s"%robot_utterance)
                await msg.say(robot_utterance)
                
    if msg.text() == '图片':
        url = 'http://qrul2d5a1.hn-bkt.clouddn.com/image/street.jpg'
        
        # 构建一个FileBox
        file_box_1 = FileBox.from_url(url=url, name='xx.jpg')
        await msg.say(file_box_1)
        
    # 如果收到的message是一张图片
    if msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:

        # 将Message转换为FileBox
        file_box_2 = await msg.to_file_box()

        # 获取图片名
        img_name = file_box_2.name

        # 图片保存的路径
        img_path = './image/' + img_name

        # 将图片保存为本地文件
        await file_box_2.to_file(file_path=img_path)

        # 调用图片风格转换的函数
        img_new_path = img_transform(img_path, img_name)

        # 从新的路径获取图片
        file_box_3 = FileBox.from_file(img_new_path)

        await msg.say(file_box_3)


async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + qrcode)


async def on_login(user: Contact):
    print(user)


async def main():
    # 确保我们在环境变量中设置了WECHATY_PUPPET_SERVICE_TOKEN
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan',      on_scan)
    bot.on('login',     on_login)
    bot.on('message',   on_message)

    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())
