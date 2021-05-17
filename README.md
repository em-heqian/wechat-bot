# wechat-bot 聊天机器人
本来准备在本地部署的使用nodejs开发wechaty，然后调用paddlehub的模型生成回复语句，但是最后没能生成，要么wechaty连接不上网关要么会报invalid server，最后参考细菌在在阿里云上部署了一台虚拟主机，最后终于可以实现聊天机器人了。
效果图
![](https://ai-studio-static-online.cdn.bcebos.com/9c50e5194abd4572b11e7dc55fbc6df3f66b08e8b79c497fb8ed43f70692cf56)
没有小号 就自己和自己聊 😂
![](https://ai-studio-static-online.cdn.bcebos.com/61b0218b6b36439db74312c3a3fa63536e528b3cdc9d4ba39b50eaca7dac1250)
也可以支持图片转漫画风格

###  1、第一步现在阿里云上部署了python网关
>>> apt update

>>> apt install docker.io

>>> docker pull wechaty/wechaty:latest

>>> export WECHATY_LOG="verbose"

>>> export WECHATY_PUPPET="wechaty-puppet-wechat"

>>> export WECHATY_PUPPET_SERVER_PORT="8080"

>>> export WECHATY_TOKEN="puppet_padlocal_xxxxxx" # 这里输入你自己的token

>>> docker run -ti --name wechaty_puppet_service_token_gateway --rm -e WECHATY_LOG -e WECHATY_PUPPET -e WECHATY_TOKEN -e WECHATY_PUPPET_SERVER_PORT -p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" wechaty/wechaty:latest

###  2、本来准备接入智能客服的，结果没有找到很好的模型，自己引入了一下情人节生成情话，和图片动漫化的模型，完成了一个简单的聊天回复机器人
