from flask import Flask;
from flask import request;

app = Flask(__name__);


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Handle POST request
        # Example: Authentication logic
        return 'POST request to login'
    else:
        # Handle GET request
        return 'GET request to login'





if __name__ == "__main__":
    app.run(debug=True);