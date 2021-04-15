import requests
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }

  response = requests.post("https://api.chat-api.com/instance255056/sendMessage?token=3x4b68jyfkipt9q5", data=payload)
  return str(response.status_code)