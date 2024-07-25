import flask

app = flask.Flask(__name__)

@app.route("/b")
def home():
    with open("bc.tar.xz", "rb") as f:
        response = flask.Response(f.read())
        response.headers['Content-type'] = "application/x-xz"
        return response
    
app.run()