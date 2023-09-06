import secrets, pymysql
conn = pymysql.connect(
    host = "localhost", 
    port = 3306, 
    db = "py_charmer_hackfest", 
    user = "root", 
    passwd = "msahani852"
)

cursor = conn.cursor()

def UsernameDuplicateChecking(username: str, placeholder='student'):
    '''
    This function will check whether in the database there is 
    any duplicate username or not
    True: if duplicate is there in the database
    False: if duplicate is not present
    '''
    q = "SELECT CASE WHEN (SELECT ID FROM "+ placeholder +" WHERE user_name='"+ username +"') THEN 'TRUE' ELSE 'FALSE' END AS isAvailable"
    cursor.execute(q)
    records=cursor.fetchall()[0][0]
    if(records=="TRUE"):
        return True
    return False

def EmailDuplicateChecking(email: str, placeholder='student'):
    '''
    This function will check whether in the database there is 
    any duplicate email or not
    True: if duplicate is there in the database
    False: if duplicate is not present
    '''
    q = "SELECT CASE WHEN (SELECT ID FROM "+ placeholder +" WHERE email='"+ email +"') THEN 'TRUE' ELSE 'FALSE' END AS isAvailable"
    cursor.execute(q)
    records=cursor.fetchall()[0][0]
    if(records=="TRUE"):
        return True
    return False

def UserRegistration(username: str, first_name: str, last_name: str, email: str, password: str, phone: str, interval: str, placeholder = 'student'):
    # check whether the username is present in the database or not
    if(UsernameDuplicateChecking(username, placeholder) or EmailDuplicateChecking(email, placeholder)):
        print("User already exists in the database")
        return "User already exists"
    else:
        # the username is unique
        access_token = secrets.token_hex(25)
        val = (username, first_name, last_name, email, password, access_token, phone, interval)
        insertQuery = "INSERT INTO " + placeholder + " (user_name,first_name,last_name,email,pass_word,acc_token,contact,reportingTime) Values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insertQuery, val)
        conn.commit()
        print("Data is stored!")
        return "Data stored successfully"

def UserLogin(email: str, pwd: str, placeholder : str):
    '''
    This function will return True if the given credentials are valid
    otherwise it will return False
    '''
    #checking the email and pwd is present in the database or not
    query = "SELECT acc_token FROM " + placeholder + " where email= '" + email + "' AND pass_word ='" + pwd + "'"
    cursor.execute(query)
    records=cursor.fetchall()
    return records

def CreateUrl(username: str, url: str):
    '''
    This is important for the chrome extension
    This function will store the data of that particular url in the database
    '''
    pass

def DeleteUrl(username: str, url: str):
    '''
    This is important for the chrome extension
    This function will delete the url from teh database
    '''
    pass
