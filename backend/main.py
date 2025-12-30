import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import Base, engine, SessionLocal
from . import models, schemas
from .extraction import extract_text_from_pdf, extract_sds_data, extract_sds_llama

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI SDS Parser")

# CORS (frontend access)
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploaded_sds"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===========================
#      STANDARD UPLOAD
# ===========================

@app.post("/upload", response_model=schemas.SDSBase)
async def upload_sds(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_path)
    extracted = extract_sds_data(text)

    doc = models.SDSDocument(
        filename=file.filename,
        supplier=extracted.supplier,
        raw_text=text,
        extracted=extracted.dict(),
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return schemas.SDSBase(
        id=doc.id,
        filename=doc.filename,
        created_at=doc.created_at,
        supplier=doc.supplier,
        extracted=extracted,
    )
   # return results


@app.get("/sds", response_model=List[schemas.SDSListItem])
def list_sds(db: Session = Depends(get_db)):
    return db.query(models.SDSDocument).order_by(models.SDSDocument.created_at.desc()).all()


@app.get("/sds/{sds_id}", response_model=schemas.SDSDetail)
def get_sds(sds_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.SDSDocument).filter(models.SDSDocument.id == sds_id).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="SDS not found")
    
    return schemas.SDSDetail(
        id=doc.id,
        filename=doc.filename,
        created_at=doc.created_at,
        supplier=doc.supplier,
        raw_text=doc.raw_text,
        extracted=schemas.SDSExtracted(**doc.extracted)  # <-- Properly closed here
    )


# ===========================
#      AI LLaMA Extract
# ===========================

@app.post("/extract-ai")
async def extract_ai(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    text = extract_text_from_pdf(file_path)

    # AI extraction
    extracted = extract_sds_llama(text)

    # Save to DB similar to normal upload
    doc = models.SDSDocument(
        filename=file.filename,
        supplier=extracted.supplier,
        raw_text=text,
        extracted=extracted.dict(),
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {"message": "AI extraction complete", "id": doc.id}

@app.delete("/sds/{sds_id}")
def delete_sds(sds_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.SDSDocument).filter(models.SDSDocument.id == sds_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="SDS not found")

    db.delete(doc)
    db.commit()
    return {"message": "SDS deleted successfully"}




