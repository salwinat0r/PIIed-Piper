from fastapi import FastAPI, UploadFile, File
from main import data_anonymizer
app = FastAPI(title= "PII Anonymizer ")


@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/upload")
async def pdf_upload(file: UploadFile = File(...)):
    contents = await file.read()

    temp_file_path = f"{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(contents)

    # Perform anonymization
    data_anonymizer(temp_file_path)

    # Return the anonymized PDF
    return {"Your file has been PIIPed :)"}