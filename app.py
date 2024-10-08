from flask import Flask, render_template, jsonify, request


app = Flask(__name__)

# Define the route for the home pagepython 
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
