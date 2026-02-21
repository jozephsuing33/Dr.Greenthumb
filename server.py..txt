from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/scan-garden")
async def scan(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    h, w, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    beds = []
    for i, cnt in enumerate(contours):
        if cv2.contourArea(cnt) > 1000:
            x, y, bw, bh = cv2.boundingRect(cnt)
            beds.append({
                "id": i,
                "x": f"{(x/w)*100}%", "y": f"{(y/h)*100}%",
                "width": f"{(bw/w)*100}%", "height": f"{(bh/h)*100}%"
            })
    return {"beds": beds}
