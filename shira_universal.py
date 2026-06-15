from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
@app.route('/status')
def home():
    return jsonify({
        "shira": "ativa",
        "servidor": "Render",
        "status": "online",
        "potestas": "in umbra"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
