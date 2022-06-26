from fastapi import FastAPI, WebSocket
import cv2
from deepface import DeepFace
import json
import asyncio

app = FastAPI()
video = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    while True:

        _, frame = video.read()
        frame = cv2.flip(frame, 1)
        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)

        cv2.putText(frame, result["dominant_emotion"], (50,50), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 2, cv2.LINE_4)

        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = faceCascade.detectMultiScale(grayscale, 1.1, 4)

        for (x,y,w,h) in face:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            data = {
                "emotion": result['dominant_emotion'],
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h)
            }
            await websocket.send_json(json.loads(json.dumps(data)))    

        cv2.imshow("Video", frame)

        

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    video.release();
    cv2.destroyAllWindows();

@app.get("/")
async def root():
    return{"Does it": "work?"}
