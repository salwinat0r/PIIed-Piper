from fastapi import FastAPI, UploadFile, File
from main import data_anonymizer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import Response
from starlette import status
import mimetypes
import redis
import os

app = FastAPI(title= "PII Anonymizer ")

redis_host = "localhost"
redis_port = 6379
redis_db = 0
redis_key = "output_pdf"

# Establish Redis connection
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)


app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000/",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"msg": "Ground control to Major Tom 🚀"}

@app.post("/upload")
async def pdf_upload(file: UploadFile = File(...)):
    contents = await file.read()

    temp_file_path = f"{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(contents)

    # Perform anonymization and get the anonymized content
    anonymized_contents = data_anonymizer(temp_file_path)
    os.remove("output.pdf")
    try:
        os.remove(temp_file_path)  # Use os.unlink instead of os.remove for Windows
    except Exception as e:
        print(f"Error while deleting the temporary file: {e}")

    # Store the anonymized PDF content in Redis
    redis_client.set(redis_key, anonymized_contents)

    return {"Your file has been PIIped :)"}


@app.get("/download")
def download_pdf():
    pdf_contents = redis_client.get(redis_key)

    if not pdf_contents:
        return {"error": "PDF not found in Redis."}

    # Get the MIME type of the PDF
    response = Response(content=pdf_contents)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = 'inline; filename="output.pdf"'

    return response