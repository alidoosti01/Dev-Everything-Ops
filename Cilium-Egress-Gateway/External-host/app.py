from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def forward_request():
    destination_url = "http://188.1xx.xxx.xx:8080"  # Your destination URL

    # Forward the request to the destination
    if request.method == 'POST':
        response = requests.post(destination_url, json=request.json)
    else:
        response = requests.get(destination_url, params=request.args)

    # Return the response back to the pod
    return response.content, response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
