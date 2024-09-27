# Create application instance
from flask import Flask

# Call class constructor, inputting 
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'