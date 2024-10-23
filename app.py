from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2

app = Flask(__name__)
socketio = SocketIO(app)
ip = 'rtsp://admin:admin@10.98.160.135:8554/live'

# 初始化视频捕获
camera = cv2.VideoCapture(ip)  # 替换为你的摄像头索引或视频流URL

@app.route('/')
def index():
    return render_template('control.html')  # 使用之前的HTML文件

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            print("Frame read successfully")
            # 将图像编码为JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('message')
def handle_message(data):
    print(f'Received message: {data}')
    # 根据命令控制小车
    # 这里可以添加控制小车的逻辑

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000,allow_unsafe_werkzeug=True)
