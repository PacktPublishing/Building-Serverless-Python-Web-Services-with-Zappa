from bottle import Bottle, run

app = Bottle()

@app.route('/hello')
def hello():
    return "Hello World!\n"
