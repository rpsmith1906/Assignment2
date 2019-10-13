#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

def getid(html, id):
    extract = BeautifulSoup(html, "html.parser")
    data = extract.find(id=id)
    return data

def login(user, pword, twofa, search, id_field) :
    addr = 'http://127.0.0.1:5000'

    login_data =  {'username':user, 'password':pword, 'twofapassword':twofa}
    r = requests.post(addr + "/register", login_data)

    print (r.text)
    data = getid(r.text, id_field)
    assert data != None, "Missing id='result' in the html response"
    print (data.text)
    return (search in data.text)

#def test_login():
resp = login("spellcheck_test", "password", "17572028962", "success", "success")
#    assert resp, "Successfully logged in"

#def test_bad_login():
#    resp = login("rpsmith", "ac123", "", "Incorrect", "result")
#    assert resp, "Incorrectly supplied password"
