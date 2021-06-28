import pymongo
import requests
import api
import dbh,sh
import re
import datetime

def menu(sender):
    sh.session_status(sender,session_type='0',status='0')  
    message =  "*Previous session expired*\nHello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Packaged foods\n*5*.Beverages*0*.Cancel"
    api.reply_message(sender,message)
    return '', 200

def feedback(sender):
    sh.session_status(sender,session_type='8',status='0')  
    message = "Thank you for using Tau We’d love to hear what you think of our service. Your feedback will help us determine what features to add and how we can make the product better for you."
    api.reply_message(sender,message)
    return '', 200

def endchat(sender):
    sh.session_status(sender,session_type='0',status='0')  
    message = "Your feedback is important to us.thank you very much for the valuable feedback.We have forwarded your message to our engineers.\nHave a good day\nRegards Marve"
    api.reply_message(sender,message)
    return '', 200


def validatephone(phone_number):
    if len(phone_number) <= 9:
        return False

    if phone_number.isdigit():
        return True
    else:
        return False

    return True 

def validateemail(email):
    if(re.match("^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$", email) != None):
        return True
    else:
        return False

    # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    # if(re.search(regex,email)):  
    #     return True
          
    # else:  
    #     return False

def validatedate(sender,date_string):
    format = '%Y-%m-%d'
    try:
        datetime.datetime.strptime(date_string, format)
        return True

    except ValueError:
        # message = "This is the incorrect date string format. It should be YYYY-MM-DD"
        # api.reply_message(sender,message)
        return False

def greetuser(sender,senderName,message):
    #create new session
    dbh.db['Senders'].find_one_and_delete({'Sender': sender})
    record = {
        "Sender": sender,
        "Timestamp": datetime.datetime.now(),
        "session_type": "0",
        "Status": "0"
        }
    dbh.db['Senders'].insert_one(record)

    #message = "Hello "+ senderName +" 🙋🏽‍♂ ,I'm Marve, im going to help you do some amazing shopping, \nPlease select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Packaged foods\n*5*.Beverages*0*.Cancel \n\n *You can always terminate your current session by entering EXIT or return to main menu by entering MENU*"
    message = "Hello "+ senderName +" 🙋🏽‍♂ ,I'm Marve, im going to help you do some amazing shopping, \nPlease select one of the following options to purchase 👇 \n*1*.Product Review\n*2*.Product Purchase\n\n*You can always terminate your current session by entering EXIT or return to main menu by entering MENU*"
    payload = {
        "phone": sender,
        "filename": 'https://chikobvore.github.io/dura_online_shop/images/homepic.jpg',
        "caption": message,
        "body": 'https://chikobvore.github.io/dura_online_shop/images/homepic.jpg'
    }
    print(message)
    
    response = requests.post("https://api.chat-api.com/instance295364/sendFile?token=402ackxpfuoi7vzz", data=payload)
    return str(response.status_code)


def checkout(sender):
    
    products = []
    sh.session_status(sender,'1','1')
    message =  "*Your shopping cart*\n"

    i = 1
    total = 0
            
    for product in dbh.db['shopping_cart'].find({"sender": sender}):
        message = message +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nUnit Price: " + str(product['unit_price']) +"\nQuantity: " + str(product['quantity'])+ ""+"\nProduct Code: "+ product['product_code'] + "\nTotal Price"+ str(product['total_price']) +"\n\n"
        i = i + 1
        total = total + product['total_price']


    #message = message + "\n\n*Total units:* "+ str(i) +"\n*nSub Total:* " + str(product['total_price']) + "\n*Discounts:* 0.00" + "\n*Total Price*: " +str(product['total_price'])
    
    # for product in dbh.db['shopping_cart'].find({"sender": sender}):
    #     message = message +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"
    #     i = i + 1


    #recommendations = "\n*Other product recommendations comes here*"

    message = message + "\n\nType *Proceed* to proceed to pay or Menu to look for other products or *REMOVE* to remove products from your cart"
    api.reply_message(sender,message)
    return '', 200


def exit(sender):
    
    dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
    dbh.db['shopping_cart'].find_one_and_delete({'Sender': sender})
    sh.session_status(sender,'2','0') 
    message =  "*Please select one of the following options to purchase 👇 \n*1*.Groceries\n*2*.Household appliances\n*3*.Body care products\n*4*.Beverages\n*0*.Check Out \n\n*Exit* to terminate current session"
    api.reply_message(sender,message)
    return '', 200


def remove(sender):
    
    sh.session_status(sender,'7','0')
    message =  "Please enter product code"
    api.reply_message(sender,message)
    return '', 200


def addtocart(sender,response):
    total = 0

    mycart = response.split(',')
    mycart.append('0')
    mycart.append('1')

    product_existance = dbh.db['products'].count_documents({"product_code": mycart[0]}) 

    if product_existance > 0:
        product = dbh.db['products'].find_one({"product_code": mycart[0]})

        record = {
            "sender": sender,
            "product": product['product'],
            "product_code": product['product_code'],
            "unit_price": product['price'],
            "quantity": mycart[1],
            "total_price": float(product['price']) * float(mycart[1])
        }
        dbh.db['shopping_cart'].insert_one(record)

        if mycart[2]:

            record = {
                "sender": sender,
                "product": product['product'],
                "product_code": product['product_code'],
                "rating": mycart[2],
            }
            dbh.db['product_ratings'].insert_one(record)

            
            i = 0

            for rating in  dbh.db['product_ratings'].find({'product_code': product['product_code']}):
                total = total + float(rating['rating'])
                i = i + 1

            average_rating = float(total/i)
            
            details = dbh.db['products'].find_one({"product_code": product['product_code']})
            dbh.db['products'].update({"product_code": product['product_code']},
            {
                "product": details['product'],
                "type":  details['type'],
                "price":  details['price'],
                "description":  details['description'],
                "best_before":  details['best_before'],
                "md":  details['md'],
                "image_url":  details['image_url'],
                "product_code":  details['product_code'],
                "ratings": average_rating,
                "frequency": i
            })

            message =  "*"+ product['product'] + " successfully added to cart"+ "*\n\n"

            message =  message + "*Your shopping cart*\n"

            i = 1
            total = 0
                
            for product in dbh.db['shopping_cart'].find({"sender": sender}):
                message = message +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nUnit Price: " + str(product['unit_price']) +"\nQuantity: " + str(product['quantity'])+ ""+"\nProduct Code: "+ product['product_code'] + "\nTotal Price"+ str(product['total_price']) +"\n\n"
                i = i + 1
                total = total + product['total_price']

            i = i - 1

            recommendations ="\n*Other products recommended for you*\n"
            for product in dbh.db['products'].find().sort([("ratings", -1)]).limit(5):

                recommendations = recommendations +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] + "\nDescription: "+ product['description'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"
                i = i + 1
            message = message + recommendations +"\nTo add more to your cart,please provide details as follows *(product code,quantity,product ratings optional(0-10))*\n\nEnter *menu* to return to main menu or 0 to check out"
            api.reply_message(sender,message)
            return '', 200

        #sh.session_status(sender,'0','0') 

        message =  "*"+ product['product'] + " successfully added to cart"+ "*\n\n"

        message =  message + "*Your shopping cart*\n"

        i = 1
            
        for product in dbh.db['shopping_cart'].find({"sender": sender}):
            message = message +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nUnit Price: " + str(product['unit_price']) +"\nQuantity: " + str(product['quantity'])+ ""+"\nProduct Code: "+ product['product_code'] + "\nTotal Price"+ str(product['total_price']) +"\n\n"
            i = i + 1
            total = total + product['total_price']

        i = i - 1

        recommendations ="\n*Other products recommended for you*\n"
        for product in dbh.db['products'].find().sort([("ratings", -1)]).limit(5):

            recommendations = recommendations +"*"+ str(i) +"*" +"\nProduct: " + product['product'] + "\nPrice: " + product['price'] + "\nDescription: "+ product['description'] +  "\nProduct Code: "+ product['product_code'] +"\n\n"
            i = i + 1

        message = message + "\n\n*Total units:* "+ str(i) +"\n*nSub Total:* " + str(total) + "\n*Discounts:* 0.00" + "\n*Total Price*: " +str(total)
        message = message + recommendations +"\nTo add more to your cart,please provide details as follows *(product code,quantity,product ratings optional(0-10))*\n\nEnter *menu* to return to main menu or 0 to check out"
        api.reply_message(sender,message)
        return '', 200

