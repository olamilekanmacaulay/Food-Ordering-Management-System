from abc import ABCMeta, abstractmethod
#abstractmethod and ABC metaclass is imported into the program

from random import randint
#a randit module is imported here

from time import gmtime, strftime

import datetime
#the datetime module is imported here

import sqlite3
#this is used to import sql database inyo the program

import re
#this is used to import into the program a module called regex

conn = sqlite3.connect('IconMaclekVirtualRestaurant1.sql')
cur = conn.cursor()
#connection to the sql database is done here


register_admintable = '''CREATE TABLE IF NOT EXISTS admin_details(
                                admin_ID INTEGER PRIMARY KEY,
                                first_name TEXT,
                                last_name TEXT,
                                admin_password TEXT)
                                '''
cur.execute(register_admintable)
#a table is created called admin_details is created here which contains the admin details such as names, adminID and password

admin_login_history = '''CREATE TABLE IF NOT EXISTS admin_history(
                                admin_ID TEXT,
                                Date_and_time TEXT,
                                logged_out TEXT)
                                '''
cur.execute(admin_login_history)
#a table is created called admin_history is created here which contains the admin details such as adminID and date and time of log in

foods_for_sale = '''CREATE TABLE IF NOT EXISTS foods_available(
                                foods TEXT PRIMARY KEY,
                                price INTEGER)
                                '''
cur.execute(foods_for_sale)
#a table named foods_available  is created here, this table is used to store the foods available for sale and each price

create_food = '''INSERT INTO foods_available(foods, price)
                            VALUES
                            ('Jollof Rice', 1000),
                            ('Ofada Rice', 1200),
                            ('Fried Rice', 1300),
                            ('Semovita', 500),
                            ('Amala', 500),
                            ('Pounded Yam', 500),
                            ('Egunsi Soup', 500),
                            ('Okro Soup', 500),
                            ('Vegetable Soup', 500),
                            ('Pizza', 5000),
                            ('Ice Cream', 1000),
                            ('Meat Pie', 500)'''
try:
    cur.execute(create_food)
    conn.commit()
   #the execution of create_food is used to insert the above foods and prices into the foods_available table already created. then the try and except block means to execute the code if there's no integrity error and if there is, it should just be passed without crashing.
except sqlite3.IntegrityError:
    pass

register_customertable  = '''CREATE TABLE IF NOT EXISTS user_details(
        User_ID INTEGER PRIMARY KEY,
        first_Name TEXT,
        last_Name TEXT,
        address TEXT,
        password TEXT,
        phone_Number TEXT)
        '''
cur.execute(register_customertable)
#a user_details table is created here which does same function like the admin_details table, but this accepts user details instead of admin details


cushistorytable = '''CREATE TABLE IF NOT EXISTS history(
                    user_ID TEXT,
                    food_Ordered TEXT,
                    price INTEGER,
                    date_ordered TEXT)
                    '''
cur.execute(cushistorytable)
# a history table is created here which include the user id, food ordered, price and date ordered


class Customer(metaclass = ABCMeta):
    @abstractmethod
    def register():
        return 0


    @abstractmethod
    def logIn():
        return 0

    @abstractmethod
    def checkDetails():
        return 0

    @abstractmethod
    def makeOrder():
        return 0

    @abstractmethod
    def makePayment():
        return 0

    @abstractmethod
    def checkHistory():
        return 0


#an abstract base class is created here which the class CustomerServices is made to inherit fromit, this is to ensure that none of the methods under customerService class are being missed out, they are made to return 0 cos they dont really have a definition of their own

class CustomerServices(Customer):

    def register(self, userID):
        try:
            self.userID = userID
            print()
            print("Account creation has been successful")
            print(f"Your log in details are:\n1.user ID = {userID}. \n2.password = {password} ")
            #this will print out the userID and the password
            
            Query1 = cur.execute('''INSERT INTO user_details (User_ID, first_Name, last_Name, address, password,  phone_Number) VALUES(?,?,?,?,?,?)''',(userID, firstName, lastName, address, password, phoneNumber))
            conn.commit()
     #query1 inserts the USERID and so to a table user_details.
            return True
            #the method register is made to prompt a user to input his/her details such as password, phonenumber, address, names and the details are added to a table already created called user details

        except sqlite3.IntegrityError:
            print('Glitch in our system, try again')
            return False
           # the try and except block make sure to avoid a user using userID that has once been generated for another user and to avoid the system from being crashed if the system notices.

    def logIn(self):
        #a login mehod of class customerservice is made
        query1 = cur.execute("SELECT user_ID, password from user_details")
        
        #user_ID and password saved in the user details are selected
        data = query1.fetchall()
        details = {}
        for dat in data:
            details[dat[0]] = dat[1]
        #this is used to fetch the userID and password in the table and a dictionary is made where the userID is the key and the password is the value
        
        if userID in details.keys() and details[userID] == password:
            print("Login Successful")
            return True
        #if the user ID provided by the user is in tbe dictionary key and the password is the value then the login is successful and else the log in is not succesful and a message saying wrong details will be printed.
        
        else:
            print("Wrong details")
            return False


    def checkDetails(self, userID):
        self.userID = userID
        Query = '''SELECT * FROM user_details WHERE User_ID == {}'''.format(userID)
        query = cur.execute(Query)
        query = query.fetchall()
        #the user details table is selected here and made to print 
        print("user ID: ", query[0][0])
        print("First Name: ", query[0][1])
        print("Last Name: ", query[0][2])
        print("Address: ", query[0][3])
        print("Phone Number: ", query[0][5])
        #since the brings out a datatype like a list, and then the userID and so are printed using indexes. since the user is inserted first, it will be in index [0] and others follows same way


    def makeOrder(self, totalitems, details):
        totalamount = 0
        #totalamount is the total price of the foods bought
        
        for i in totalitems:
            totalamount = totalamount + details[i]
            #for every item in the totalitems list, add the former price of total amount to it. the prices of the foods are the value in the details dictionart
        return totalamount
        # the total amount should be returned


#this method is used to check if an atm number is valid or not by using luhm's algorithm after that the total amount of items bought is deducted from the account

    def makePayment(self, numbers, totalitems, totalamount,h):
        print()
        self.totalitems = totalitems
        self.numbers = numbers
        
        try:
            atmcheck = [int((int(number)*2)/10) + (int(number)*2)%10 for number in numbers[::-1][1::2]] + [int(number) for number in numbers[::-1][::2]]
            print("Valid card number!") if sum(atmcheck)%10 == 0 and h != 'check' else "Invalid card number!"
           # the validation of the card is done here using lumh's algorithm

            now = datetime.datetime.now()#this is used to get the time
            if h =='check':
                pass
            else:
                print(f"you ordered for {totalitems} at {now} and a fee of {totalamount} has been deducted from your bank account")
            return True
        except ValueError:
            print("Invalid details") #a value error is handled here and prevented using exception handling. 
            return False

    def checkHistory(self):
        print()
        query = '''SELECT * FROM history WHERE user_ID == {}'''.format(userID)
        query = cur.execute(query).fetchall()
        #all the data in the table history where the userID is thst of the particular user is fetched
        
        for det in query:
            print('\nyou bought \nFood-->{}\nPrice-->{}\nDate-->{}'.format(det[1],det[2],det[3]))
            #this wll print out the food bought, time and date in that format for every order taken.
            #this method will be used to to select the history details from the history table


class Admin(metaclass = ABCMeta):
    @abstractmethod
    def registerAdmin():
        return 0


    @abstractmethod
    def loginAdmin():
        return 0

    @abstractmethod
    def addFood():
        return 0

    @abstractmethod
    def removeFood():
        return 0

    @abstractmethod
    def viewOrders():
        return 0

#an abstract base class is created here which the class AdminServices is made to inherit from it, this is to ensure that none of the methods under AdminService class are being missed out




class AdminServices(Admin):
    
    #this works same way like the register method in the customerService class
    def registerAdmin(self, adminID):
        
        try:
            print()
            self.adminID = adminID
            print("Account creation is successful")
            print(f"Your log in details are:\n1.adminID = {self.adminID}.\n2.password = {adminPassword} ")
            Query4 = cur.execute("INSERT INTO admin_details  VALUES (?,?,?,?)", (adminID, adminFirstName, adminLastName, adminPassword))
            conn.commit()
            return True
        
    
        except sqlite3.IntegrityError:
            print('Glitch in our sytem, its not you, its us, Try Again')
            return False
    
    #this works same way like the login method in the CustomerService class			
    def loginAdmin(self):
        
        query1 = cur.execute("SELECT admin_ID, admin_Password from admin_details")
        data = query1.fetchall()
        details = {}
        
        for dat in data:
            details[dat[0]] = dat[1]
            
        if adminID in details.keys() and details[adminID] == adminPassword:
            print("Login Successful")
            return True
        
        else:
            
            print("Wrong details")
            return False
         

    def addFood(self, food, price):
        
        try:
            Query2 = cur.execute('''INSERT INTO foods_available(foods, price) VALUES(?, ?)''',(food, price))
            conn.commit()
            print('{} has been added to the menu'.format(food))
            #this method is used to insert new food and price into foods available table		
            
        except sqlite3.IntegrityError:
            print('Food already in menu')
            return False
            #the try block executes this code by adding new good into the foods_available table, which may arise in an integrity error if the food already exists in the table.so the except block made sure that error is handled and food already in menu is printed if it food already exists poop

    def removeFood(self, food):
        
        show_foods = "SELECT * FROM foods_available"
        #the data in foods available are extracted here
        foods = cur.execute(show_foods)
        data = foods.fetchall()
        
        details = {}#a dictionary is created
        
        for dat in data:
            details[dat[0]] = dat[1]
            
        if  food in details.keys():
        	#if food is in the foods_available(extracted foods are already in details)
            Query3= "DELETE FROM foods_available WHERE foods ='"+ food +"'"
            #the name of the food inputed will be deletedfrom the foods_available table
            cur.execute(Query3)
            conn.commit()
            print('{} has been removed from the menu'.format(food))
            #this method deletes food and prices from the foods_available table
            
        else:
            print('You can not remove food that is not on the menu')
            #else(if the food is not in the table, print a message that says "you can't remove food......')



    def viewOrders(self, query4):
        
        if len(query4) > 0:
        #if history is more than 0, i.e a transaction has been made
            for det in query4:
                print('\nuserID "{}" bought \nFood-->{}\nPrice-->{}\nDate-->{}'.format(det[0],det[1],det[2],det[3]))
            #this method prints out the history made by all the customers 
            
        else:
            print('No orders yet') #print "no orders yet"

admin = AdminServices()
#an object of AdminServices class is made here

customer = CustomerServices()
#an object of CustomerService class is made here

print("WELCOME TO ICON MACLEK VIRTUAL RESTAURANT")
print("YOUR SATISFACTION IS OUR UTMOST CONCERN")
print('_'*60)

while True:
#this is used to create a loop

    print("Enter 1 to continue as an admin\nEnter 2 to continue as a customer\nEnter 3 to exit")
    print("Don't go on as an admin if you are not")
    
    continuePhase = input()
    #the user is prompt to enter a number here


    if continuePhase == str(1):
        
        while True:
            
            print()
            print("Enter 1 to register if you are a new user")
            print("Enter 2 to log in if you have an existing account")
            print("Enter 3 to go back to the previous menu")
            
            adminChoice = input()
            #if the input is 1, a while loop is also created, and the user is prompt to enter another input, this will take the user to register or log in or exit

            if adminChoice == str(1):
                
                adminID = randint(100000, 999999)
                #a random integer number between the range of 100000 and 999999 is generated here
                
                print("Enter your first name")
                adminFirstName = input().title()
                #.title() capitalizes the first letter in each word in the user input
                while not adminFirstName.isalpha():
                    adminFirstName = input('First Name: ').title()
                   #if the input are not alphabets, the user is prompt to write it again
                    
                print()
                
                print("Enter your last name")
                adminLastName = input().title()
                while not adminLastName.isalpha():
                    adminLastName = input('Last Name: ').title()
                #the title() works by capitalizing the first letters in each word
                
                print()
                
                print("Enter your password, password must be at least 6 characters long")
                #the user is prompt to enter his names, then password

                while True:
                    
                    adminPassword = input()
                    
                    if len(adminPassword) < 6 or " " in adminPassword:
                        print("Password weak. Make sure there is no space in your password")
                        
                    else:
                        
                        break
                #if the length of the password is not up to 6 or there's a space in the password, an invalid password message will be generated and the user will be made to input another password, this will continue until the user enter the desired password'
                
                admin.registerAdmin(adminID)
                #the register method is then call on the admin object

            elif adminChoice == str(2):
                
                print("Enter your adminID")
                adminID = input()
                while not adminID.isnumeric():
                    adminID = input('Check your ID')
                    #if the input by the user are not numbers, the user is prompt to write it again

                adminID = int(adminID)
                #the input is then converted to integer here

                print("Enter your password")
                adminPassword = input()
                #the user is promt to enter his password
                print()
                adminloginstatus = admin.loginAdmin()
                #the login method is called on the admin class


                if adminloginstatus == True:
                    #if the return value of the invoking of the login method is True, then a loop is created which continually accepts input from the user.
                    logged_in = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    query = cur.execute('''INSERT INTO admin_history(admin_ID, Date_and_time) VALUES(?, ?)''',(adminID, logged_in))
                    conn.commit()
            
                    while True:
                    
                        print()
                        print("Enter 1 to add to list of foods Available")
                        print("Enter 2 to remove from list of foods Available")
                        print("Enter 3 to view order(s)")
                        print("Enter 4 to go to the previous menu")
                        print()

                        adminChoice = input()

                        if adminChoice == str(1):
                            
                            print()
                            
                            print("Enter the added food")
                            food = input().title()
                            while not food.isalpha():
                                food = input('Check the food name: ').title()
                                
                            print("Enter the food's price")
                            price = input()
                            while not price.isnumeric():
                                price = input('Check the price: ')
                            admin.addFood(food, price)#the addfood method is invoked on the admin object
    #if the input is 1, the user is prompt to enter the name of the food and its price after which the addFoof will add the food and price to the goods_available table


                        elif adminChoice == str(2):
            
                            print()
                
                            print("Enter the removed food")
                            food = input().title()
                            while not food.isalpha():
                                food = input('Check the food name: ').title()
                            admin.removeFood(food)#the removeFood method is invoked on the admin object, the food and its price will be removed from the foods_available table.
#if the input is 2, the user is prompt to enter the food that should be deleted

                        elif adminChoice == str(3):
        
                            print()
            
                            print("Enter date(yyyy-mm--dd)")
                            dateOrdered = input()

                            Query4 = '''SELECT * FROM history WHERE date_ordered ==''' + "'" + dateOrdered +"'"
                            query4 = cur.execute(Query4)
                            
                            while not re.match(re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$'),dateOrdered):
                                print("invalid input")
                                dateOrdered = input('enter date (yyyy-mm-dd): ')
                            admin.viewOrders(query4.fetchall())


        #the view order method is invoked on the admin class and the data selected will be printed out

                        elif adminChoice == str(4):
                            logged_out = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                            query = cur.execute('''INSERT INTO admin_history(admin_ID, logged_out) VALUES(?, ?)''',(adminID, logged_out))
                            conn.commit()
                            break #this will break from the while loop created above

                        else:
                            print("Invalid Input")
                            #if anything else is entered by the user, a invalid input message will be printed

            elif adminChoice == str(3):
               
                break #if the adminchoice is 3, then then the while loop created for the input which make the program go back to the previous entry

            else:
                print("Invalid Input")
                ##if anything else is entered by the user, a invalid input message will be printed

    elif continuePhase == str(2):
        
        while True:
            
            print("Enter 1 to register if you are a new user")
            print("Enter 2 to log in if you have an existing account")
            print("Enter 3 to go back to the previous menu")
            userChoice = input()
            print()

            if userChoice == str(1):
                
                userID = randint(100000, 999999)
                #a random integer number between the range of 100000 and 999999 is generated here
                
                print("Enter your first name")
                firstName = input().title()
                while not firstName.isalpha():
                    firstName = input('First Name: ').title()
                    
                print()
                
                print("Enter your last name")
                lastName = input().title()
                while not lastName.isalpha():
                    lastName = input('Last Name: ').title()
                #the user is prompt to enter his names
                
                print()
                
                print("Enter your password, password must be at least 6 characters long")

                while True:
                    
                    password = input()#the user is prompt to enter his password
                    
                    if len(password) < 6 or " " in password: #if the length of the password is not up to 6 or there is a space in the password inputed,, print password weak and the user is made to enter another because of the while loop
                        print("Password weak")
                        
                    else:
                        break#else if the password is greater than 6, then break from the loop
                        
                print()
                
                print("Enter your address, as this will help us locate you\nMake sure a well described address is given to avoid late or no delivery of your order")
                address = input()
                
                print()

                print("Enter your phoneNumber.\nMake sure the number can be accessed")
                
                while True:
                    
                    phoneNumber = input()
                    while not phoneNumber.isnumeric():
                        phoneNumber = input('Check the phone number entered')
                   
                #a phone number should be strictly numbers
                
                    if len(phoneNumber) != 11 or " " in phoneNumber:
                        print("Invalid Number, check if the Number is a valid number")
                    
                    else:
                        
                        if phoneNumber.startswith("090") or phoneNumber.startswith("070")  or phoneNumber.startswith("080") or phoneNumber.startswith("081"):
                            
                            break
                            
                        else:
                            
                            print("Invalid Number, Check if the Number is Correct")
#before inputing the user's phone number a while loop is created so that the user can re enter the number if the number entered by the user is not validated. the loop breaks if the phone number starts with the correct digits and if its 11 in number and it contains no space

                customer.register(userID)#the register method is called on the customer class here.
    
                print()

            elif userChoice == str(2):
                
                #user_ID and password saved in the user details are selected
                #the user is prompt to enter the userID he/she is registered with
                
                print("Enter your userID")
                userID = input()
                while not userID.isnumeric():
                    userID = input('Check your ID')
                userID = int(userID)
                
                
                print("Enter your password")
                password = input()
                #the user is prompt to enter the password he registered with.
                
                loginStatus = customer.logIn()
                #the log in is invoked here and assigned to a variable called loginStatus
                
                print()
                
                if loginStatus is True:
                    
                #if loginStatus returns true, a while loop is created, then input is taken from the user and the input is assigned to a variable called userChoice
                    
                    while True:
                        
                        print()
                        print("Enter 1 to Order")
                        print("Enter 2 to check history")
                        print("Enter 3 to check customer details")
                        print("Enter 4 to go to the previous menu")
                        print()
                        
                        userChoice = input()
                        
                        print()

            #while log in, a loopbis created where you can order, check history and chevk customer details, the user is prompt to enter a number, and the input is assigned to a variable called userChoice

                        if userChoice == str(1):
                    
                            totalitems = []
                        
                            show_foods = "SELECT * FROM foods_available"
                            #the data in foods available are extracted here
                            foods = cur.execute(show_foods)
                            data = foods.fetchall()
                            
                            details = {}#a dictionary is created
                            for dat in data:
                                details[dat[0]] = dat[1]
                            #the foods are made the keys and the prices of the foods are made the values in the dictionary assigned to a variable called details.
                            
                            while True:
                                
                                print("Enter your food, Enter quit to stop ordering")
                                foodordered = input().title()
                                
                                if foodordered == "Quit":
                                    
                                    break
                                    
                                else:
                                    
                                    p = '''SELECT foods,price FROM foods_available where foods =='''+ "'"+foodordered+"'"
                                    p = cur.execute(p).fetchall()
                                    
                                    if len(p) > 0:
                                        print(f'{foodordered} added to cart')
                                        totalitems.append(foodordered)
                                        
                                    else:
                                        
                                        print(f"{foodordered} not available")
                                        
                            totalamount = customer.makeOrder(totalitems, details)
                            #the totalamount is returned when makeorder method is invoked on the customer class
                            
                            if totalamount > 0:
                                
                                print("Enter your correct atm details, enter 1 to go to the previous menu ")
                                
                                while True:
                                    
                                    numbers = input()
                                    while not numbers.isnumeric():
                                        numbers = input('Check your atm details')
                                    if numbers == str(1):
                                        break
                                    elif len(numbers) != 16 and customer.makePayment(numbers, totalitems,totalamount,'check'):

                                        print("Wrong card numbers Enter atm details again,Press 1 to exit (your cart will be emptied)")

                                    else:

                                        customer.makePayment(numbers, totalitems,totalamount,'here')
                                        

                                    #the user is prompt to enter his atm card numbers, if the number is not up to 16, the loop makes the user re-enter it. then the makepayment method is invoked on the customer object if only the total amount of item bought is greater than zero i.e if any item is bought, if not the program breaks to the previous one.
                                        dateordered = str(datetime.date.today()) #dateordered is generated here using the datetime module
                                        totalitems = ' and '.join(totalitems)
            #totalitems is made a string here by joining the items together by and if they're more than one
                                        query1 = cur.execute('''INSERT INTO history(user_ID, food_Ordered,price, date_ordered) VALUES(?,?,?,?)''',(userID,totalitems,totalamount,dateordered))
                                        conn.commit()
                                #the userID, food, price of food ordered and the date is inserted into the history table
                                        
                                        break
                                    #the loop breaks here


                        elif userChoice == str(2):
                            
                            print("checking history")
                            customer.checkHistory()
            #the checkhistory method is invoked on the customer object if the user choice is 2

                        elif userChoice == str(3):
                    
                            print()
                            customer.checkDetails(userID)
            #the checkDetails method is invoked on the customer object if the user choice is 3



                        elif userChoice == str(4):
                            break#the loop breaks if the userchoice is 4 and it returns to the previous entry

                        else:
                            print("Invalid Input")
                            #if anything else is inputed apart from 1,2,3 or 4 then an invalid input message is printed



            elif userChoice == str(3):
                break #if the user input is 3, the loop breaks

            else:
                print("invalid input")
    #if anything else is inputed apart from 1,2,or 3 then an invalid input message is printed


    elif continuePhase == str(3):
        break
        #if the continuephase is 3, then the program exits from the loop and the program ends

    else:
        print("Invalid Input")
        #if anything else is inputed apart from 1,2,or 3 then an invalid input message is printed

conn.close()
#the connection to sql is closed here