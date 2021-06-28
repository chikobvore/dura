from datetime import date
import pymongo
from flask import Flask, redirect, render_template, request, session, url_for
import datetime,requests
import sh,api,main
import sys,os,random
from paynow import Paynow
import pandas as pd
import dbh

app = Flask(__name__)

@app.route('/',methods=["get","post"])
def index():

    if request.method == 'GET':
        return render_template('index.html')
    
    payload = request.get_json()
    sender = payload['messages'][0]['author'].split('@')[0]
    senderName = payload['messages'][0]['senderName']
    message_id = payload['messages'][0]['id']
    response = payload['messages'][0]['body']

    if sender == '263787060171':
        return '', 200
        

    if response == 'EXIT' or response == 'exit' or response == 'Exit':
        message = "Hello "+ senderName +" 🙋🏽‍♂ ,I'm Marve, im going to help you do some amazing shopping, \nPlease select one of the following options to purchase 👇 \n*1*.Product Review\n*2*.Product Purchase\n\n*You can always terminate your current session by entering EXIT or return to main menu by entering MENU*"
        return main.greetuser(sender,senderName,message)
        
    if response == 'REMOVE' or response == 'Remove' or response == 'remove':
        return main.remove(sender)

    if response == 'menu' or response == 'Menu' or response == 'MENU':
        return main.menu(sender)

    if response == 'Proceed' or response == 'proceed' or response == 'PROCEED':
        sh.session_status(sender,session_type='PAYMENT',status='0')
                        
        message =  "*Make Payment*\nPlease select your payment method👇 \n *1*.Ecocash. \n *2*.Telecash\n *3*.One Money\n\n*0*.Cancel"
        api.reply_message(sender,message)
        return '', 200

    
    if response == '0':
        return main.checkout(sender)

    existance = dbh.db['Senders'].count_documents({"Sender": sender})
        
    if existance < 1:
        
        #create new session
        message = "Hello "+ senderName +" 🙋🏽‍♂ ,I'm Marve, im going to help you do some amazing shopping, \nPlease select one of the following options to purchase 👇 \n*1*.Product Review\n*2*.Product Purchase\n\n*You can always terminate your current session by entering EXIT or return to main menu by entering MENU*"
        return main.greetuser(sender,senderName,message)

    else:
        response = response
        state = dbh.db['Senders'].find_one({"Sender": sender})

        date2 = datetime.datetime.now()
        date1 = state['Timestamp']

        time_delta = (date2 - date1)

        total_seconds = time_delta.total_seconds()

        minutes = total_seconds/60
        if minutes > 15:
            dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
            dbh.db['shopping_cart'].find_one_and_delete({'sender': sender})

            message = "Hello "+ senderName +" 🙋🏽‍♂ ,I'm Marve, im going to help you do some amazing shopping, \nPlease select one of the following options to purchase 👇 \n*1*.Product Review\n*2*.Product Purchase\n\n*You can always terminate your current session by entering EXIT or return to main menu by entering MENU*"
            return main.greetuser(sender,senderName,message)
  
            # message = "*Previous session expired*\nHello "+ senderName +" 🙋🏽‍♂ ,I'm Marve, im going to help you do some amazing shopping, \nPlease select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Packaged foods\n*5*.Beverages*0*.Cancel \n\n *You can always terminate your current session by entering EXIT or return to main menu by entering MENU*"
            # api.reply_message(sender,message)
            # return '', 200              
        if state['session_type'] == "0":
            if response == "1":
                sh.session_status(sender,'1','1')

                existance = dbh.db['shopping_cart'].count_documents({"sender": sender})
                if existance  < 1:
                    sh.session_status(sender,'2','0') 
                    message = "*You have no previous purchases*\n\nPlease select one of the following options to purchase 👇\n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Beverages\n*0*.Check Out\n\n*You can always terminate your current session by entering EXIT or return to main menu by entering MENU*"
                    api.reply_message(sender,message)
                    return '', 200
                else:
                    message = "*How do you want to rate the following products you purchased*\n\n"
                    for product in dbh.db['shopping_cart'].find({"sender": sender}):
                        message = message +"*"+ product['product_code'] +"*" +"\nProduct: " + product['product'] +"\nProduct Code: "+ product['product_code']+ "\n\n"
                    
                    message = message + "\n\nTo provide your rating,please enter Product code and your rating ie *(product code, your rating)*"
                    api.reply_message(sender,message)
                    return '', 200

            elif response == "2":
                #product purchase
                sh.session_status(sender,'2','0') 
                message = "Hello "+ senderName +" 🙋🏽‍♂\nPlease select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Beverages\n*0*.Check Out\n\n*You can always terminate your current session by entering EXIT or return to main menu by entering MENU*"
                api.reply_message(sender,message)
                return '', 200

            else:
                message = "invalid response from user"
                api.reply_message(sender,message)
                return '', 200
        
        if state['session_type'] == "1":

            if state['Status'] == "1":

                sh.session_status(sender,'1','2') 
                mycart = response.split(',')
                record = {
                    "Sender": sender,
                    "product_code": mycart[0],
                    "rating": mycart[1],
                    "review_text": " "
                    }
                dbh.db['ratings'].insert_one(record)

                message = "Briefly comment on the product"
                api.reply_message(sender,message)
                return '', 200

            elif state['Status'] == "2":
                sh.session_status(sender,'0','0') 
                details = dbh.db['ratings'].find_one({"Sender": sender})
                dbh.db['ratings'].update({"Sender": sender},
                {
                    "Sender": sender,
                    "product_code":details['product_code'],
                    "rating": details['rating'],
                    "review_text": response
                })
                return main.endchat(sender)
            

        if state['session_type'] == "2":
                
                if response == "1":
                    sh.session_status(sender,'2A','1')           

                    message = "*Grocery Products*,\n Please type in the grocery products you would like to purchase"
                    payload = {
                        "phone": sender,
                        "filename": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg',
                        "caption": message,
                        "body": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
                    }
            
                    response = requests.post("https://api.chat-api.com/instance295364/sendFile?token=402ackxpfuoi7vzz", data=payload)
                    print('....replied: '+ sender + '...........')
                    return str(response.status_code)

                elif response == "2":
                    sh.session_status(sender,'2A','2')           

                    message = "*Household Products*,\n Please type in the household products you would like to purchase"
                    payload = {
                        "phone": sender,
                        "filename": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg',
                        "caption": message,
                        "body": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
                    }
            
                    response = requests.post("https://api.chat-api.com/instance295364/sendFile?token=402ackxpfuoi7vzz", data=payload)
                    print('....replied: '+ sender + '...........')
                    return str(response.status_code)
                elif response == "3":
                    sh.session_status(sender,'2A','3')           

                    message = "*Body care Products*,\n Please type in the Body care products you would like to purchase"
                    payload = {
                        "phone": sender,
                        "filename": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg',
                        "caption": message,
                        "body": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
                    }
            
                    response = requests.post("https://api.chat-api.com/instance295364/sendFile?token=402ackxpfuoi7vzz", data=payload)
                    print('....replied: '+ sender + '...........')
                    return str(response.status_code)

                elif response == "4":
                    sh.session_status(sender,'2A','4')           

                    message = "*Beverages*,\n Please type in the Beverages products you would like to purchase"
                    payload = {
                        "phone": sender,
                        "filename": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg',
                        "caption": message,
                        "body": 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
                    }
            
                    response = requests.post("https://api.chat-api.com/instance295364/sendFile?token=402ackxpfuoi7vzz", data=payload)
                    print('....replied: '+ sender + '...........')
                    return str(response.status_code)
                elif response == "0":
                    return main.checkout(sender)

                    
                else:
                    #invalid response from user
                    dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
                    dbh.db['shopping_cart'].find_one_and_delete({'sender': sender})
                    
                    sh.session_status(sender,'0','0') 

                    message =  "*Previous session expired*\nHello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Packaged foods\n*5*.Beverages\n*0*.Check out\n*Exit* to terminate current session"
                    api.reply_message(sender,message)
                    return '', 200

        if state['session_type'] =="2A":
            
            products = response.split(',')
            notfound = ''
            others = ''
             

            for item in products:
                product_existance = dbh.db['products'].count_documents({"product": item.lower()})

                if product_existance > 0:

                    products = []
                    sh.session_status(sender,'2B','0') 
                    message =  "*Products*\n\nRecommended for you\n" 
                    i = 1


                    for product in dbh.db['products'].find({"product": item.lower()}).sort([("ratings", -1)]):
                        message = message +"*"+ product['product_code'] +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] + "\nDescription: "+ product['description'] +  "\nProduct Code: "+ product['product_code']  +"\nratings: "+ str(product['ratings']) + "⭐"+"\n\n"
                        i = i + 1


                    message = message + "\n\nTo add product to your cart, please provide details as follows\n*(product code,quantity,product ratings (optional 0-10))*"
                    api.reply_message(sender,message)
                            
                else:
                    
                    notfound = notfound + ","+ item.lower()
                    others = ''

                    if state['Status'] == "1":

                        sh.session_status(sender,'2B','0') 
                        for product in dbh.db['products'].find({"type": "groceries"}).sort([("ratings", -1)]).skip(2).limit(5):
                            others = others +"*"+ product['product_code'] +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] + "\nDescription: "+ product['description'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"
            
                    if state['Status'] == "2":
                        
                        sh.session_status(sender,'2B','0') 

                        for product in dbh.db['products'].find({"type": "households"}).sort([("ratings", -1)]).skip(2).limit(5):
                            others = others +"*"+ product['product_code'] +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] + "\nDescription: "+ product['description'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"
              

                    if state['Status'] == "3":
                        sh.session_status(sender,'2B','0') 

                        for product in dbh.db['products'].find({"type": "bodyproducts"}).sort([("ratings", -1)]).skip(2).limit(5):
                            others = others +"*"+ product['product_code'] +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] + "\nDescription: "+ product['description'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"
                              

                    if state['Status'] == "4":

                        sh.session_status(sender,'2B','0') 
                        for product in dbh.db['products'].find({"type": "beverages"}).sort([("ratings", -1)]).skip(2).limit(5):
                            others = others +"*"+ product['product_code'] +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] + "\nDescription: "+ product['description'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"

            itemsnotfound = "Sorry,*"+ notfound +"* could not be found,\n\nAvailable Products\n"+ others

            if notfound == "":
                return '', 200
            else:
                itemsnotfound  = itemsnotfound + "\n\nTo add product to your cart, please provide details as follows\n*(product code,quantity,product ratings (optional 0-10))*"
                api.reply_message(sender,message = itemsnotfound)
                return '', 200

        if state['session_type'] == "2B":
            return main.addtocart(sender,response)

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

                details = dbh.db['pending_payments'].find_one({"Sender": sender})

                for product in dbh.db['shopping_cart'].find():
                    record = {
                        "Sender": sender,
                        "product": product['product'],
                        "product_code": product['product_code'],
                        "quantity": product['quantity']
                    }
                    dbh.db['shopping_history'].insert_one(record)

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
                            "reference_no": random.randint(10000,99999),
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
                            "reference_no": random.randint(10000,99999),
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
                    message = message +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nUnit Price: " + str(product['unit_price']) +"\nQuantity: " + str(product['quantity'])+ ""+"\nProduct Code: "+ product['product_code'] + "Total Price"+ str(product['total_price']) +"\n\n"
                    i = i + 1
    
                
                
                details = dbh.db['pending_payments'].find_one({"Sender": sender})
                dbh.db['pending_payments'].update({"Sender": sender},
                {
                        "Sender": sender,
                        "reference_no": random.randint(10000,99999),
                        "pay_number": details['pay_number'],
                        "email": details['email'],
                        "amount": response,
                        "Purpose": "",
                        "Payment_method": details['Payment_method'],
                        "Date_paid": datetime.datetime.now()
                    })

                i = 1
                message2 ="\n\n *Other products recommended for you comes here*"
                for product in dbh.db['products'].find().sort([("ratings", -1)]).limit(5):
                    message2 = message2 +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] + "\nDescription: "+ product['description'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"
                    i = i + 1

                #message2 ="\n\n*Other products recommended for you comes here*\n\n"

                products = pd.DataFrame(dbh.db['product_ratings'].find())

                message3 = "*Confirm Payment*\n\nPlease confirm details below\n\n*Phone No*: "+ details['pay_number'] + "\n*Email*: "+  details['email'] + "\n*Amount*: "+  response +  "\n\nPress 1 to continue or 0 to cancel"
                message = message + message2 + message3
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
                payment = paynow.create_payment('test order', 'muchingamiri@gmail.com')

                payment.add('CHATBOT PAYMENT', 2)
                response = paynow.send_mobile(payment,'0784451537','ecocash')


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
                    mytime = str(pd.to_datetime('now'))
                    mydate = mytime.split(' ')
                    mydate[0]
    
                    record = {
                        "Sender": sender,
                        "reference_no": random.randint(10000,99999),
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
                        "reference_no":  random.randint(10000,99999),
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
            
        elif state['session_type'] == "7":
            sh.session_status(sender,'1','1') 
            dbh.db['shopping_cart'].find_one_and_delete({'sender': sender,'product_code': response})

            products = []
            message =  response + " successfully removed\n\n"+"*Your shopping cart*\n" 
            i = 1
                
            for product in dbh.db['shopping_cart'].find({"sender": sender}):
                message = message +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nUnit Price: " + str(product['unit_price']) +"\nQuantity: " + str(product['quantity'])+ ""+"\nProduct Code: "+ product['product_code'] + "\nTotal Price"+ str(product['total_price']) +"\n\n"
                i = i + 1
                
            i = 1
            recommendations ="\n*Other products recommended for you*\n"
            for product in dbh.db['products'].find().sort([("ratings", -1)]).skip(2).limit(5):
                recommendations = recommendations +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] + "\nDescription: "+ product['description'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"
                i = i + 1

            #recommendations = "\n*Other product recommendations comes here*"

            message = message + recommendations + "\n\nType *Proceed* to proceed to pay or EXIT to look for other products or *REMOVE* to remove products from your cart"
            api.reply_message(sender,message)
            return '', 200


if __name__ == '__main__':
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run(host= '0.0.0.0', debug = True)