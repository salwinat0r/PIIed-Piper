from fastapi import FastAPI, UploadFile, File
from main import data_anonymizer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse



app = FastAPI(title= "PII Anonymizer ")


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

    # Perform anonymization
    data_anonymizer(temp_file_path)

    # Return the anonymized PDF
    return {"Your file has been PIIped :)"}

@app.get("/download")
def download_pdf():
    file_path = "output.pdf"
    return FileResponse(file_path, filename="output.pdf")