from flask import Flask
from flask_cors import CORS
from api import api_blueprint  

app = Flask(__name__)
CORS(app)  

app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
