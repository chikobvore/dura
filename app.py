from datetime import date
import pymongo
from flask import Flask, redirect, render_template, request, session, url_for
import datetime,requests
import sh,api,main
import sys,os,random
from paynow import Paynow
import pandas as pd

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

            dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
            dbh.db['shopping_cart'].find_one_and_delete({'sender': sender})
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
            
            response = requests.post("https://api.chat-api.com/instance268730/sendFile?token=du0bwpcfom4gs5kf", data=payload)
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
                dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
                dbh.db['shopping_cart'].find_one_and_delete({'sender': sender})
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
            
                    response = requests.post("https://api.chat-api.com/instance268730/sendFile?token=du0bwpcfom4gs5kf", data=payload)
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
            
                    response = requests.post("https://api.chat-api.com/instance268730/sendFile?token=du0bwpcfom4gs5kf", data=payload)
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
            
                    response = requests.post("https://api.chat-api.com/instance268730/sendFile?token=du0bwpcfom4gs5kf", data=payload)
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
            
                    response = requests.post("https://api.chat-api.com/instance268730/sendFile?token=du0bwpcfom4gs5kf", data=payload)
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
            
                    response = requests.post("https://api.chat-api.com/instance268730/sendFile?token=du0bwpcfom4gs5kf", data=payload)
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

                    product_existance = dbh.db['products'].count_documents({"product": response})

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
                    if response == 'Proceed' or response == 'proceed' or response == 'PROCEED':

                        sh.session_status(sender,session_type='PAYMENT',status='0')
                        
                        message =  "*Make Payment*\nPlease select your payment method👇 \n *1*.Ecocash. \n *2*.Telecash\n *3*.One Money\n\n*0*.Cancel"
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

            elif state['session_type'] == "PAYMENT":

                if state['Status'] == '0':

                    state = dbh.db['Senders'].find_one({"Sender": sender})
                    sh.session_status(sender,state['session_type'],status='1A')

                    if response == '1':
                        payment_method = 'ecocash'
                    elif response == '2':
                        payment_method = 'telecash'
                    elif response == '3':
                        payment_method = 'onemoney'
                    else:
                        message = "*invalid input*\nplease select a valid payment method\n*1*.Ecocash\n*2*.Telecash\n*3*.One Money\n*0*.Cancel transaction"
                        api.reply_message(sender,message)
                        return '', 200

                    
                    record = {
                            "Sender": sender,
                            "reference_no": random.randint(10000,99999),
                            "pay_number": '',
                            "email": "",
                            "amount": "",
                            "Purpose": "",
                            "Payment_method": payment_method,
                            "Date_paid": datetime.datetime.now()
                            }
                    dbh.db['pending_payments'].insert_one(record)

                    message =  "*Make Payment*\nPlease provide your phone number for payment"
                    api.reply_message(sender,message)
                    return '', 200

                if state['Status'] == '1A':

                    state = dbh.db['Senders'].find_one({"Sender": sender})
                    sh.session_status(sender,state['session_type'],status='1')
                    details = dbh.db['pending_payments'].find_one({"Sender": sender})

                    dbh.db['pending_payments'].update({"Sender": sender},
                        {
                                "Sender": sender,
                                "account": "",
                                "reference_no": details['reference_no'],
                                "pay_number": response,
                                "email": '',
                                "amount": "",
                                "Purpose": "",
                                "Payment_method": details['Payment_method'],
                                "Date_paid": datetime.datetime.now()
                            })

                    message =  "*Make Payment*\nPlease provide your email address"
                    api.reply_message(sender,message)
                    return '', 200
                
                elif state['Status'] == '1':
                    if main.validateemail(email=response):
                        
                        state = dbh.db['Senders'].find_one({"Sender": sender})
                        sh.session_status(sender,state['session_type'],status='2')
                        details = dbh.db['pending_payments'].find_one({"Sender": sender})
                        dbh.db['pending_payments'].update({"Sender": sender},
                        {
                                "Sender": sender,
                                "reference_no": details['reference_no'],
                                "pay_number": details['pay_number'],
                                "email": response,
                                "amount": "",
                                "Purpose": "",
                                "Payment_method": details['Payment_method'],
                                "Date_paid": datetime.datetime.now()
                            })

                        message =  "*Payment Details*\nPlease enter amount"
                        api.reply_message(sender,message)
                        return '', 200

                    else:
                        message =  "Please enter a valid email address"
                        api.reply_message(sender,message)
                        return '', 200

                elif state['Status'] == '2':
                    
                    state = dbh.db['Senders'].find_one({"Sender": sender})
                    sh.session_status(sender,session_type=state['session_type'],status='3')

            
                    
                    products = []
                    message =  "*Confirm Payment*\n\n*Shopping Cart\n*" 
                    i = 1
                    price = 0

                    for product in dbh.db['shopping_cart'].find({"sender": sender}):
                        message = message +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"
                        i = i + 1
        
                    
                    
                    details = dbh.db['pending_payments'].find_one({"Sender": sender})
                    dbh.db['pending_payments'].update({"Sender": sender},
                    {
                            "Sender": sender,
                            "reference_no": details['reference_no'],
                            "pay_number": details['pay_number'],
                            "email": details['email'],
                            "amount": response,
                            "Purpose": "",
                            "Payment_method": details['Payment_method'],
                            "Date_paid": datetime.datetime.now()
                        })

                    message2 = "*Confirm Payment*\n\nPlease confirm details below\n\n*Phone No*: "+ details['pay_number'] + "\n*Email*: "+  details['email'] + "\n*Amount*: "+  response +  "\n\nPress 1 to continue or 0 to cancel"
                    message = message + message2
                    api.reply_message(sender,message)
                    return '', 200

                elif state['Status'] == '3':
                    if response == '0':

                        dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
                        dbh.db['shopping_cart'].find_one_and_delete({'sender': sender})
                        message = "Transaction cancelled 😔"
                        api.reply_message(sender,message)
                        return main.menu(sender)

                    details = dbh.db['pending_payments'].find_one({"Sender": sender})
                    #paynow = Paynow(9415,'3d7f4aed-ab06-42f5-b155-0e12e41fc714','https://tauraikatsekera.herokuapp.com/chatbot/payments', 'https://tauraikatsekera.herokuapp.com/chatbot/payments')
                    paynow = Paynow(10724,'31008a64-6945-43d6-aed2-000961c04d5a','https://tauraikatsekera.herokuapp.com/chatbot/payments', 'https://tauraikatsekera.herokuapp.com/chatbot/payments')
                    payment = paynow.create_payment(details['reference_no'], details['email'])
    
                    payment.add(details['Purpose'], details['amount'])
                    response = paynow.send_mobile(payment, details['pay_number'], details['Payment_method'])


                    if(response.success):
                        poll_url = response.poll_url
                        print("Poll Url: ", poll_url)
                        # Get the poll url (used to check the status of a transaction). You might want to save this in your DB
                        r=requests.get(poll_url)
                        actualResponse = r.text
                        
                        tr = actualResponse.split("&")
                    
                        diction = {}
                        
                        for string in tr:
                            values = string.split("=")
                            print(values)
                            diction[values[0]] = values[1]

                        #get date
                        mytime = str(pd.to_datetime('now'))``
                        mydate = mytime.split(' ')
                        mydate[0]


        
                        record = {
                            "Sender": sender,
                            "reference_no": details['reference_no'],
                            "paynow_ref": diction['paynowreference'],
                            "pay_number": details['pay_number'],
                            "email": details['email'],
                            "amount": details['amount'],
                            "Purpose": details['Purpose'],
                            "Service_code": details['Service code'],
                            "Status": "PAID",
                            "Date_paid": mydate[0]
                            }
                        dbh.db['payments'].insert_one(record)
                        dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
                        dbh.db['shopping_cart'].find_one_and_delete({'sender': sender})

                        message = "*Payment Confirmation*: Success\n*Reference number*: "+diction['paynowreference']+ "\n\n*Please note that the money will reflect in your account after next end-of-day settlement.*\n\nTo view the transaction online please follow this link\n"+poll_url
                        api.reply_message(sender,message)
                        return main.feedback(sender)

                    else:
                        details = dbh.db['pending_payments'].find_one({"Sender": sender})
                        record = {
                            "Sender": sender,
                            "account": details['account'],
                            "reference_no": details['reference_no'],
                            "paynow_ref": diction['paynowreference'],
                            "pay_number": details['pay_number'],
                            "email": details['email'],
                            "amount": details['amount'],
                            "Purpose": details['Purpose'],
                            "Status": "FAILED",
                            "Date_paid": mydate[0]
                            }
                        dbh.db['payments'].insert_one(record)
                        dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
                        message = "Transaction Failed"
                        api.reply_message(sender,message)
                        return main.feedback(sender)
                


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
