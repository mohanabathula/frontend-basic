from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# URL of the detection pod
DETECTION_POD_URL = 'http://192.168.20.16:30050/video_feed'

@app.route('/forward', methods=['POST'])
def forward_request():
    try:
        # Receive frame from the client
        print("Enter try loop")
        frame_data = request.data  # Raw frame data from client
        client_timestamp = float(request.headers.get('Client-Timestamp', time.time()))

        # Forward the frame and headers to the detection pod without any modification
        headers = {
            'Client-Timestamp': str(client_timestamp)
        }

        # Include optional frame dimensions if present
        if 'Frame-Width' in request.headers and 'Frame-Height' in request.headers:
            headers['Frame-Width'] = request.headers['Frame-Width']
            headers['Frame-Height'] = request.headers['Frame-Height']

        # Forward the frame to the detection pod
        detection_response = requests.post(
            DETECTION_POD_URL,
            data=frame_data,   # Forward raw frame data as-is
            headers=headers
        )

        # Check for errors from the detection pod
        if detection_response.status_code != 200:
            print(f"Error from detection pod: {detection_response.status_code}")
            return jsonify({'error': 'Error from detection pod'}), 500

        if 'application/json' in detection_response.headers.get('Content-Type', ''):
            results = detection_response.json()
            print("Parsed JSON response:", results)
        else:
            # Handle plain text response
            print("Non-JSON response received from detection pod")
            results = {"message": detection_response.text}

        # Calculate delay (client to server)
        print("time calculation")
        server_timestamp = time.time()
        server_to_client_delay = server_timestamp - client_timestamp
        print('Delay time (server to client):', server_to_client_delay)
        print("_____________________________________")

        return jsonify(results)

    except Exception as e:
        print("Error processing frame:", e)
        return jsonify({'error': 'Error processing frame'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
