from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='http://localhost:5173')

@app.route('/api/data', methods=['GET'])
def users():
    return jsonify(
        {
            "users": [
                "Alice",
                "Bob",
                "Charlie"
            ]
        }
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)

# def get_data():
#     sample_data = {
#         "message": "Hello, World!",
#         "status": "success"
#     }
#     return jsonify(sample_data)

# if __name__ == '__main__':
#     app.run(host='', port=5000)


#FUCKFUCKFUCKUFKCUFKCU