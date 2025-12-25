from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Upload


# ✅ SINGLE router (this is IMPORTANT)
router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

# ---------- SCHEMA ----------
class UploadText(BaseModel):
    type: str            # notes | thoughts | questions | ebook
    title: str
    content: str | None = None


# ---------- ROUTES ----------

@router.get("/test")
def test_upload():
    return {"status": "Upload router working"}


@router.post("/text")
def upload_text(data: UploadText, db: Session = Depends(get_db)):

    upload = Upload(
        type=data.type,
        title=data.title,
        content=data.content
    )

    db.add(upload)
    db.commit()
    db.refresh(upload)

    return {
        "message": "Content uploaded successfully",
        "id": upload.id
    }


