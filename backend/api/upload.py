from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.middleware.auth import get_current_user
from backend.services.file_service import FileService

router = APIRouter()
file_service = FileService()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict[str, str]:
    content = await file.read()
    try:
        text = file_service.extract_text(file.filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return {"filename": file.filename, "text": text[:2000]}
