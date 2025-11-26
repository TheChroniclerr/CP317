from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='http://localhost:4200')

@app.route('/api/data', methods=['GET'])
def users():
    return jsonify(
        {
            "users": [
                "Alice",
                "Bob",
                "Charlie",
                "Diana"
            ]
        }
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)