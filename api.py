import requests
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }
        
  response = requests.post("https://api.chat-api.com/instance293806/sendMessage?token=033877aij04aikvw", data=payload)
  return str(response.status_code)
