import base64

from flask import Flask, request, render_template, make_response

app = Flask(__name__)

@app.route('/')

def index():

        print request.cookies

        return render_template('index.html')

if __name__ == '__main__':

    app.run(host='192.168.122.117',port=5019, debug=True)