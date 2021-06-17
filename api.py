import requests
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }
        
  response = requests.post("https://api.chat-api.com/instance289638/sendMessage?token=dzm32w8u4tumnjhg", data=payload)
  return str(response.status_code)
