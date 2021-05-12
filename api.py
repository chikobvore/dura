import requests
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }
        
  response = requests.post(" https://api.chat-api.com/instance268730/sendMessage?token=du0bwpcfom4gs5kf", data=payload)
  return str(response.status_code)
