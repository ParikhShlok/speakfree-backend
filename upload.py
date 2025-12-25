from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import Upload

router = APIRouter()

class UploadText(BaseModel):
    type: str
    title: str
    content: str | None = None

@router.post("/upload/text")
def upload_text(data: UploadText, db: Session = Depends(get_db)):

    upload = Upload(
        type=data.type,
        title=data.title,
        content=data.content
    )

    db.add(upload)
    db.commit()
    db.refresh(upload)

    return {"message": "Content uploaded successfully"}
