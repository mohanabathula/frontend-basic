import cv2
import requests
import time
import datetime

# Capturing video using webcam
camera = cv2.VideoCapture(0)
# Set the desired webcam resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Server URL (Dummy Pod)
# dummy_url = 'http://frontend-dummy:30000/forward'
dummy_url = 'http://192.168.49.2:30045/forward'
# dummy_url = 'http://192.168.78.238:5001/forward'
# dummy_url = 'http://192.168.20.16:30044/forward'
# dummy_url = 'http://192.168.20.16:5001/forward'


frames_sent_to_server = 0

try:
    print('Attempting to connect to Dummy Server...')

    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame from the webcam.")
            break

        # Resize the frame for faster transmission and processing
        image = cv2.resize(frame, (320, 240))

        # Convert the frame to JPEG format
        success, buffer = cv2.imencode('.jpg', image)
        if not success:
            print("Failed to encode frame to JPEG format.")
            continue
        
        frame_data = buffer.tobytes()

        # Prepare headers with frame metadata
        headers = {
            'Content-Type': 'application/octet-stream',
            'Frame-Width': str(image.shape[1]),
            'Frame-Height': str(image.shape[0]),
            'Client-Timestamp': str(time.time())
        }

        try:
            # Send frame data to the dummy server and measure the response time
            start_time = time.time()
            response = requests.post(dummy_url, data=frame_data, headers=headers)
            end_time = time.time()

            delay = end_time - start_time
            print(f'Frame sent to dummy server (Status Code: {response.status_code})')
            print(response)
            print(f'Client-to-server delay: {delay:.4f} seconds')

            frames_sent_to_server += 1
            print("Total frames sent to server:", frames_sent_to_server)

            # Process server response
            if response.status_code == 200:
                try:
                    result = response.json()
                    print('Server response:', result)
                except ValueError:
                    print('Failed to decode server response as JSON.')
            else:
                print('Error: Invalid response from dummy server.')

            # Log the current time when the frame is sent
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print(f'Frame sent by client at: {current_time}')

        except requests.RequestException as e:
            print(f"Error sending request to dummy server: {e}")

        # Display the frame in a window (optional for testing)
        cv2.imshow("TRANSMITTING TO CACHE SERVER", image)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f'{label}: {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Release the webcam and close all OpenCV windows
    camera.release()
    cv2.destroyAllWindows()

print("Total frames sent to the dummy server:", frames_sent_to_server)
