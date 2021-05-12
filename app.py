from datetime import date
import pymongo
from flask import Flask, redirect, render_template, request, session, url_for
import datetime,requests
import sh,api
import sys,os,random
from paynow import Paynow

# client = messagebird.Client('QQRgKx3QvpSV6SpEVewDvWJGK', features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANdbh.dbOX])
# # Enable conversations API whatsapp sandbox# client = messagebird.Client('1ekjMs368KTRlP0z6zfG9P70z', #features = [messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])

app = Flask(__name__)
import dbh

@app.route('/',methods=["get","post"])
def index():

    if request.method == 'GET':
        return render_template('index.html')
    else:

        payload = request.get_json()
        sender = payload['messages'][0]['author'].split('@')[0]
        senderName = payload['messages'][0]['senderName']
        message_id = payload['messages'][0]['id']
        response = payload['messages'][0]['body']
        
        if sender == '263714502462':
            return '', 200

        existance = dbh.db['Senders'].count_documents({"Sender": sender})

        if response == 'EXIT' or response == 'exit' or response == 'Exit':
            sh.session_status(sender,'0','0') 
            message =  "*Please select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Packaged foods\n*5*.Beverages*0*.Cancel"
            api.reply_message(sender,message)
            return '', 200

        #check if session exist
        if existance < 1:
            #create new session
            record = {
                "Sender": sender,
                "Timestamp": datetime.datetime.now(),
                "session_type": "0",
                "Status": "0"
                }
            dbh.db['Senders'].insert_one(record)

            message = "Hello "+ senderName +" 🙋🏽‍♂ , \nThank you for contacting Dura Online services,I'm Tina, i'm a virtual assistant,\nFor any emergency 👇 \n📞 Dial Number: +263714502462 \n\nPlease select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Packaged foods\n*5*.Beverages*0*.Cancel"
            payload = {
                "phone": sender,
                "filename": 'https://chikobvore.github.io/dura_online_shop/images/111.jpg',
                "caption": message,
                "body": 'https://chikobvore.github.io/dura_online_shop/images/111.jpg'
            }
            
            response = requests.post("https://api.chat-api.com/instance268730/sendFile?token= du0bwpcfom4gs5kf", data=payload)
            print('....replied: '+ sender + '...........')
            return str(response.status_code)

        else:
            response = response
            state = dbh.db['Senders'].find_one({"Sender": sender})

            date2 = datetime.datetime.now()
            date1 = state['Timestamp']

            time_delta = (date2 - date1)

            total_seconds = time_delta.total_seconds()

            minutes = total_seconds/60
            if minutes > 15:
                sh.session_status(sender,'0','0')
                message =  "*Previous session expired*\nHello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Packaged foods\n*5*.Beverages*0*.Cancel"
                api.reply_message(sender,message)
                return '', 200


            if state['session_type'] == "0":
                
                if response == "1":
                    sh.session_status(sender,'1','0')           

                    message = "*Grocery Products*,\n Please type in the grocery products you are looking forward to"
                    payload = {
                        "phone": sender,
                        "filename": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg',
                        "caption": message,
                        "body": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
                    }
            
                    response = requests.post("https://api.chat-api.com/instance268730/sendFile?token= du0bwpcfom4gs5kf", data=payload)
                    print('....replied: '+ sender + '...........')
                    return str(response.status_code)

                elif response == "2":
                    sh.session_status(sender,'1','0')           

                    message = "*Household Products*,\n Please type in the grocery products you are looking forward to"
                    payload = {
                        "phone": sender,
                        "filename": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg',
                        "caption": message,
                        "body": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
                    }
            
                    response = requests.post("https://api.chat-api.com/instance268730/sendFile?token= du0bwpcfom4gs5kf", data=payload)
                    print('....replied: '+ sender + '...........')
                    return str(response.status_code)
                elif response == "3":
                    sh.session_status(sender,'1','0')           

                    message = "*Body care Products*,\n Please type in the grocery products you are looking forward to"
                    payload = {
                        "phone": sender,
                        "filename": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg',
                        "caption": message,
                        "body": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
                    }
            
                    response = requests.post("https://api.chat-api.com/instance268730/sendFile?token= du0bwpcfom4gs5kf", data=payload)
                    print('....replied: '+ sender + '...........')
                    return str(response.status_code)

                elif response == "4":
                    sh.session_status(sender,'1','0')           

                    message = "*Packaged foods*,\n Please type in the grocery products you are looking forward to"
                    payload = {
                        "phone": sender,
                        "filename": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg',
                        "caption": message,
                        "body": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
                    }
            
                    response = requests.post("https://api.chat-api.com/instance268730/sendFile?token= du0bwpcfom4gs5kf", data=payload)
                    print('....replied: '+ sender + '...........')
                    return str(response.status_code)

                elif response == "5":
                    sh.session_status(sender,'1','0')           

                    message = "*Beverages*,\n Please type in the grocery products you are looking forward to"
                    payload = {
                        "phone": sender,
                        "filename": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg',
                        "caption": message,
                        "body": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
                    }
            
                    response = requests.post("https://api.chat-api.com/instance268730/sendFile?token= du0bwpcfom4gs5kf", data=payload)
                    print('....replied: '+ sender + '...........')
                    return str(response.status_code)
                elif response == "0":

                    products = []
                    sh.session_status(sender,'1','1') 
                    message =  "*Your shopping cart*\n" 
                    i = 1
                    for product in dbh.db['shopping_cart'].find({"sender": sender}):
                        message = message +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"
                        i = i + 1

                    message = message + "\n\nType Proceed to pay or EXIT to look for other products"
                    api.reply_message(sender,message)
                    return '', 200
                else:
                    #invalid response from user
                    sh.session_status(sender,'0','0')  
                    message =  "*Previous session expired*\nHello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Packaged foods\n*5*.Beverages\n*0*.Cancel"
                    api.reply_message(sender,message)
                    return '', 200

            elif state['session_type'] == "1" or state['session_type'] == "2" or state['session_type'] == "3" or state['session_type'] == "4" or state['session_type'] == "5":

                if state['Status'] == '0':

                    product_existance = dbh.db['products'].count_documents({"product": response.lower()})

                    if product_existance > 0:

                        products = []
                        sh.session_status(sender,'1','1') 
                        message =  "*Groceries*\n\nRecommended for you\n" 
                        i = 1
                        for product in dbh.db['products'].find({"product": response}).sort([("ratings", -1)]):
                            message = message +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] + "\nDescription: "+ product['description'] +  "\nProduct Code: "+ product['product_code']  +"\nratings: "+ str(product['ratings']) + "⭐"+"\n\n"
                            i = i + 1

                        message = message + "\n\nEnter product code to add to your cart or EXIT to look for other products"
                        api.reply_message(sender,message)
                        return '', 200
                    else:
                        message =  "We sorry we dont have that product in stock at the moment"
                        api.reply_message(sender,message)
                        return '', 200

                elif state['Status'] == '1':
                    if response == 'EXIT' or response == 'exit' or response == 'Exit':
                        sh.session_status(sender,'0','0') 
                        message =  "*Please select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Packaged foods\n*5*.Beverages*0*.Cancel"
                        api.reply_message(sender,message)
                        return '', 200
                    else:                    
                        product_existance = dbh.db['products'].count_documents({"product_code": response}) 

                        if product_existance > 0:
                            product = dbh.db['products'].find_one({"product_code": response})

                            record = {
                                "sender": sender,
                                "product": product['product'],
                                "product_code": product['product_code'],
                                "price": product['price'] 
                            }
                            dbh.db['shopping_cart'].insert_one(record)
                            sh.session_status(sender,'0','0') 

                            message =  "*"+ product['product'] + " successfully added to cart"+ "*"
                            message = message + "\n\n*Please select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Packaged foods\n*5*.Beverages\n*0*.Check out"
                            api.reply_message(sender,message)
                            return '', 200

                        else:
                            message =  "Sorry product code not found"
                            api.reply_message(sender,message)
                            return '', 200

@app.route('/groceries',methods = ['GET','POST']) 
def groceries():
    groceries = []
    if request.method == 'POST':
        product = {
                "product": request.form['product'],
                "type": 'groceries',
                "price": request.form['price'],
                "description": request.form['description'],
                "best_before": request.form['bb'],
                "md": request.form['md'],
                "image_url": '',
                "product_code": request.form['product_code'],
                "ratings": 0,
                "frequency": 0
                }
        dbh.db['products'].insert_one(product)

        for product in dbh.db['products'].find({"type": "groceries"}):
                groceries.append(product)

        return render_template('groceries.html',groceries = groceries)
    
    else:
        for product in dbh.db['products'].find({"type": "groceries"}):
            groceries.append(product)

        return render_template('groceries.html',groceries = groceries)


        
@app.route('/households',methods = ['GET','POST']) 
def households():
    groceries = []
    if request.method == 'POST':
        product = {
                "product": request.form['product'],
                "type": 'households',
                "price": request.form['price'],
                "description": request.form['description'],
                "best_before": request.form['bb'],
                "md": request.form['md'],
                "image_url": '',
                "product_code": request.form['product_code'],
                "ratings": 0,
                "frequency": 0
                }
        dbh.db['products'].insert_one(product)

        for product in dbh.db['products'].find({"type": "households"}):
                groceries.append(product)

        return render_template('households.html',groceries = groceries)
    
    else:
        for product in dbh.db['products'].find({"type": "households"}):
            groceries.append(product)

        return render_template('households.html',groceries = groceries)


@app.route('/bodyproducts',methods = ['GET','POST']) 
def bodyproducts():
    groceries = []
    if request.method == 'POST':
        product = {
                "product": request.form['product'],
                "type": 'bodyproducts',
                "price": request.form['price'],
                "description": request.form['description'],
                "best_before": request.form['bb'],
                "md": request.form['md'],
                "image_url": '',
                "product_code": request.form['product_code'],
                "ratings": 0,
                "frequency": 0
                }
        dbh.db['products'].insert_one(product)

        for product in dbh.db['products'].find({"type": "bodyproducts"}):
                groceries.append(product)

        return render_template('bodyproducts.html',groceries = groceries)
    
    else:
        for product in dbh.db['products'].find({"type": "bodyproducts"}):
            groceries.append(product)

        return render_template('bodyproducts.html',groceries = groceries)




@app.route('/packagedfoods',methods = ['GET','POST']) 
def packagedfoods():
    groceries = []
    if request.method == 'POST':
        product = {
                "product": request.form['product'],
                "type": 'packagedfoods',
                "price": request.form['price'],
                "description": request.form['description'],
                "best_before": request.form['bb'],
                "md": request.form['md'],
                "image_url": '',
                "product_code": request.form['product_code'],
                "ratings": 0,
                "frequency": 0
                }
        dbh.db['products'].insert_one(product)

        for product in dbh.db['products'].find({"type": "packagedfoods"}):
                groceries.append(product)

        return render_template('packagedfoods.html',groceries = groceries)
    
    else:
        for product in dbh.db['products'].find({"type": "packagedfoods"}):
            groceries.append(product)

        return render_template('packagedfoods.html',groceries = groceries)

@app.route('/beverages',methods = ['GET','POST']) 
def beverages():
    groceries = []
    if request.method == 'POST':
        product = {
                "product": request.form['product'],
                "type": 'beverages',
                "price": request.form['price'],
                "description": request.form['description'],
                "best_before": request.form['bb'],
                "md": request.form['md'],
                "image_url": '',
                "product_code": request.form['product_code'],
                "ratings": 0,
                "frequency": 0
                }
        dbh.db['products'].insert_one(product)

        for product in dbh.db['products'].find({"type": "beverages"}):
                groceries.append(product)

        return render_template('beverages.html',groceries = groceries)
    
    else:
        for product in dbh.db['products'].find({"type": "beverages"}):
            groceries.append(product)

        return render_template('beverages.html',groceries = groceries)


@app.route('/dashboard') 
def dashboard():
    return render_template('index.html')
        
if __name__ == '__main__':
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run(host= '0.0.0.0', debug = True)
