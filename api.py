import requests
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }
        
  response = requests.post("https://api.chat-api.com/instance295364/sendMessage?token=402ackxpfuoi7vzz", data=payload)
  return str(response.status_code)
