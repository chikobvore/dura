import requests
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }
  response = requests.post("https://api.chat-api.com/instance295364/sendMessage?token=402ackxpfuoi7vzz", data=payload)
  return str(response.status_code)

def greetuser(sender,message):
  sh.session_status(sender,session_type='0',status='0')
  
  payload = {
    "phone": sender,
    "filename": 'https://chikobvore.github.io/dura_online_shop/images/homepic.jpg',
    "caption": message,
    "body": 'https://chikobvore.github.io/dura_online_shop/images/homepic.jpg'
      }
            
  response = requests.post("https://api.chat-api.com/instance295364/sendFile?token=402ackxpfuoi7vzz", data=payload)
  return str(response.status_code)

