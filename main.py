from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('test.html')



if __name__ == '__main__':
    app.run(debug=True) # Enable debug mode for development 