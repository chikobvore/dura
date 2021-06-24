import requests
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }
        
  response = requests.post("https://api.chat-api.com/instance293023/sendMessage?token=rwfxyccm1posex2l", data=payload)
  return str(response.status_code)
