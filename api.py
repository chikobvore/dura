import requests
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }
        
  response = requests.post(" https://api.chat-api.com/instance257796/sendMessage?token=01pa5s42i13nmqhr", data=payload)
  return str(response.status_code)