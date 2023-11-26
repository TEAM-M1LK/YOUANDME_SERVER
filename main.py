from fastapi import FastAPI, File, UploadFile,HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import judgment
import shutil
import os

app = FastAPI(openapi_prefix="/server")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 실제 배포 시에는 원하는 Origin을 명시합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/server/upload")
def upload(file: UploadFile = File(...)):
    try:
        shutil.rmtree('./file')
    except: pass
    os.makedirs('./file', exist_ok=True)
    try:
        file_name = file.filename
        with open(f'./file/{file_name}', "wb") as file_object:
            file_object.write(file.file.read())
        return judgment.run(file_name)

    except Exception as e:
        return f"파일을 읽는 중 오류 발생: {str(e)}"
    
if __name__ == "__main__":
    # ssl_context.load_cert_chain(certfile="/etc/letsencrypt/live/www.clubblaclist.kro.kr/fullchain.pem", keyfile="/etc/letsencrypt/live/www.clubblacklist.kro.kr/privkey.pem")

    import uvicorn
    # uvicorn main:app --reload

    uvicorn.run(app, host="0.0.0.0", port=8000)