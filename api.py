import requests
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }
        
  response = requests.post("https://api.chat-api.com/instance291149/sendMessage?token=2837i4q31ild1lzg", data=payload)
  return str(response.status_code)
