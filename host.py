from flask import Flask, Response, request
from hashlib import sha512
import json
import os
import requests
import base64
import math
import shutil

def extension(name: str):
    if "." in name:
        return name[name.index(".")+1:]
    else:
        return ""
    
def calc_bot(bc, wr):
    return round(1000 * math.log(1 + bc) * math.exp(-0.08 * wr), 2)

app = Flask(__name__)

@app.route("/")
def home():
    with open("home.html", "r") as f:
        response = Response(f.read())
        return response
    
@app.route("/resource/<filename>")
def resources(filename):
    response = Response()
    b = "r"
    if not filename in os.listdir():
        response.data = "This filename is not in the project path."
        response.headers["Content-type"] = "text/plain"
        return response
    match extension(filename):
        case "css":
            response.headers["Content-type"] = "text/css"
        case "html":
            response.headers["Content-type"] = "text/html"
        case "js":
            response.headers["Content-type"] = "text/javascript"
        case "png":
            response.headers["Content-type"] = "image/png"
            b = "rb"
        case _:
            response.headers["Content-type"] = "text/plain"

    with open(filename, b) as f:
        response.data = f.read()
        return response
    
@app.route("/admin/api/<endpoint>/<id>", methods=['POST', 'DELETE'])
def admin_api(endpoint, id):
    match endpoint:
        case "score":
            if request.method == "DELETE":
                username = request.headers.get("username")
                password = request.headers.get("password")
                if os.path.exists(f"server/accounts/{username}"):
                    with open(f"server/accounts/{username}/password", "r") as f:
                        if sha512(password.encode()).hexdigest() == f.read():
                            if os.path.exists(f"server/scores/{id}"):
                                shutil.rmtree(f"server/scores/{id}")
                                return "0"
                            else:
                                return "3"
                        else:
                            return "2"
                else:
                    return "1"
            elif request.method == "POST":
                username = request.headers.get("username")
                password = request.headers.get("password")
                if os.path.exists(f"server/accounts/{username}"):
                    with open(f"server/accounts/{username}/password", "r") as f:
                        if sha512(password.encode()).hexdigest() == f.read():
                            if os.path.exists(f"server/scores/{id}"):
                                with open(f"server/scores/{id}/verified", "w") as v:
                                    v.write("1")
                                return "0"
                            else:
                                return "3"
                        else:
                            return "2"
                else:
                    return "1"
    
@app.route("/account")
def account():
    with open("account.html", "r") as f:
        response = Response(f.read())
        return response
    
@app.route("/account/view/<username>")
def account_view(username):
    with open("account_view.html", "r") as f:
        response = Response(f.read())
        response.headers["username"] = username
        return response 
    
@app.route("/account/create")
def create_account():
    with open("create_account.html", "r") as f:
        response = Response(f.read())
        return response
    
@app.route("/account/signin")
def sign_in():
    with open("sign_in.html", "r") as f:
        response = Response(f.read())
        return response 
    
@app.route("/api/account/<endpoint>", methods=['GET', 'POST'])
def account_api(endpoint):
    match endpoint:
        case "create":
            username = request.headers.get("username")
            discord = request.headers.get("discord")
            password = request.headers.get("password")
            if len(username) > 0 and type(username) == str and len(password) > 5 and type(password) == str and len(discord) > 7 and type(discord) == str:
                if not os.path.exists("server/accounts"):
                    os.mkdir("server/accounts")
                if os.path.exists(f"server/accounts/{username}"):
                    return "2"
                else:
                    os.mkdir(f"server/accounts/{username}")
                    with open(f"server/accounts/{username}/password", "w") as f:
                        f.write(sha512(password.encode()).hexdigest())
                    with open(f"server/accounts/{username}/badges", "w") as f:
                        f.write("Unverified")
                    with open(f"server/accounts/{username}/discord", "w") as f:
                        f.write(discord)
                    with open(f"server/accounts/{username}/priority", "w") as f:
                        f.write("0")
                    return "1"
            else:
                return "3"
        case "login":
            username = request.headers.get("username")
            password = request.headers.get("password")
            if not os.path.exists(f"server/accounts/{username}"):
                return "0"
            else:
                with open(f"server/accounts/{username}/password", "r") as f:
                    if sha512(password.encode()).hexdigest() == f.read():
                        return "1"
                    else:
                        return "0"
        case "badges":
            username = request.headers.get("username")
            if os.path.exists(f"server/accounts/{username}"):
                with open(f"server/accounts/{username}/badges", "r") as f:
                    response = Response(f.read())
                    response.headers['Content-type'] = "text/plain"
                    return response
        case "accounts":
            data = []
            for account in os.listdir("server/accounts"):
                with open(f"server/accounts/{account}/badges", "r") as f:
                    with open(f"server/accounts/{account}/priority", "r") as p:
                        data.append({"username": account, "badges": f.read(), "priority": p.read()})

            return data
        case "view":
            username = request.args.get("username")
            if os.path.exists(f"server/accounts/{username}"):
                with open(f"server/accounts/{username}/badges", "r") as f:
                    badges = f.read()
                with open(f"server/accounts/{username}/discord", "r") as f:
                    discord = f.read()
                return {"exists": True, "username": username, "badges": badges, "discord": discord}
            else:
                return {"exists": False}
@app.route("/api/score/<endpoint>", methods=['GET', 'POST'])
def score_api(endpoint):
    match endpoint:
        case "create":
            username = request.headers.get("username")
            password = request.headers.get("password")
            player = request.headers.get("player")
            image = request.data.decode("utf-8")
            try:
                image = base64.b64decode(image[image.index(","):])
            except:
                return {"code": 3}
            for score in os.listdir("server/scores"):
                with open(f"server/scores/{score}/players", "r") as f:
                    players = f.read().split(";")
                    if players[0] == username and players[1] == player:
                        return {"code": 0}
                with open(f"server/accounts/{username}/badges", "r") as f:
                    if not "Verified" in f.read().split(" "):
                        return {"code": 2}
            if not os.path.exists(f"server/accounts/{username}"):
                return {"code": 1}
            else:
                with open(f"server/accounts/{username}/password", "r") as p:
                    if sha512(password.encode()).hexdigest() == p.read():
                        wg_id = requests.get(f"https://api.wotblitz.eu/wotb/account/list/?application_id=57dd901f84ee3371fc7a8a0543fef204&search={player}&type=exact").json()
                        if wg_id['meta']['count'] == 1:
                            stats = requests.get(f"https://api.wotblitz.eu/wotb/account/info/?application_id=57dd901f84ee3371fc7a8a0543fef204&account_id={wg_id['data'][0]['account_id']}").json()

                            bc = stats['data'][str(wg_id['data'][0]['account_id'])]['statistics']['all']['battles']
                            wr = (stats['data'][str(wg_id['data'][0]['account_id'])]['statistics']['all']['wins'] / bc) * 100
                            
                            score = calc_bot(bc, wr)

                            with open("server/score-index", "r") as f:
                                index = int(f.read()) + 1
                            with open("server/score-index", "w") as f:
                                f.write(str(index))
                            os.mkdir(f"server/scores/{index}")
                            with open(f"server/scores/{index}/players", "w") as f:
                                f.write(f"{username};{player}")
                            with open(f"server/scores/{index}/verified", "w") as f:
                                f.write("0")
                            with open(f"server/scores/{index}/wr", "w") as f:
                                f.write(str(wr))
                            with open(f"server/scores/{index}/bc", "w") as f:
                                f.write(str(bc))
                            with open(f"server/scores/{index}/score", "w") as f:
                                f.write(str(score))
                            with open(f"server/scores/{index}/proof.png", "wb") as f:
                                f.write(image)
                            return {"code": 4}
                        else:
                            return {"code": 5}
                    else:
                        return {"code": 2}
        case "scores":
            scores = []
            for score in os.listdir("server/scores"):
                with open(f"server/scores/{score}/players", "r") as f:
                    players = f.read().split(";")
                    sent_by = players[0]
                    player = players[1]
                with open(f"server/scores/{score}/verified", "r") as f:
                    if f.read() == "1":
                        verified = True
                    else:
                        verified = False
                with open(f"server/scores/{score}/bc", "r") as f:
                    bc = f.read()
                with open(f"server/scores/{score}/wr", "r") as f:
                    wr = f.read()
                with open(f"server/scores/{score}/score", "r") as f:
                    bot_score = f.read()
                scores.append({"player": player, "username": sent_by, "verified": verified, "winrate": round(float(wr), 2), "battles": int(bc), "score": float(bot_score), "id": score})
            return scores
        case "view":
            id = request.args.get("id")
            if os.path.exists(f"server/scores/{id}"):
                with open(f"server/scores/{id}/bc", "r") as f:
                    bc = int(f.read())
                with open(f"server/scores/{id}/wr", "r") as f:
                    wr = round(float(f.read()), 2)
                with open(f"server/scores/{id}/score", "r") as f:
                    bot_score = float(f.read())
                with open(f"server/scores/{id}/players", "r") as f:
                    players = f.read().split(";")
                    sent_by = players[0]
                    player = players[1]
                with open(f"server/scores/{id}/verified", "r") as f:
                    if f.read() == "1":
                        verified = True
                    else:
                        verified = False
                return {"player": player, "username": sent_by, "verified": verified, "winrate": wr, "battles":bc, "score": bot_score, "id": id, "exists": True}
            else:
                return {"exists": False}

@app.route("/score/image/<id>")
def score_image(id):
    if os.path.exists(f"server/scores/{id}"):
        with open(f"server/scores/{id}/proof.png", "rb") as f:
            response = Response(f.read())
            response.headers['Content-type'] = "image/png"
            return response
    else:
        with open("logo.png", "rb") as f:
            response = Response(f.read())
            response.headers['Content-type'] = "image/png"
            return response

@app.route("/score/view/<id>")
def view_score(id):
    with open(f"score_view.html", "r") as f:
        response = Response(f.read())
        return response

@app.route("/browse")
def browse():
    with open("browse.html", "r") as f:
        response = Response(f.read())
        return response
    
@app.route("/browse/<url>")
def browse_url(url):
    match url:
        case "accounts":
            with open("browse_accounts.html", "r") as f:
                response = Response(f.read())
                return response
        case "scores":
            with open("browse_scores.html", "r") as f:
                response = Response(f.read())
                return response
                    
@app.route("/submit")
def submit_score():
    with open("submit.html", "r") as f:
        response = Response(f.read())
        return response 
    
app.run(debug=True)