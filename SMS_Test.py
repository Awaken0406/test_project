import requests

# 发送短信的参数

resp = requests.post('https://textbelt.com/text', {
  'phone': '+8618813754417',
  'message': 'Hello world again!!!',
  'key': 'textbelt',
})
print(resp.json())
