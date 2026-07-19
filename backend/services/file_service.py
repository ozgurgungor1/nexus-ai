import csv
import io
import json
from pathlib import Path

import pandas as pd
from docx import Document
from PyPDF2 import PdfReader


class FileService:
    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".doc",
        ".xls",
        ".xlsx",
        ".txt",
        ".csv",
        ".json",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".mp3",
        ".wav",
        ".ogg",
        ".mp4",
        ".mov",
        ".mkv",
    }
    MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".mp3", ".wav", ".ogg", ".mp4", ".mov", ".mkv"}

    def __init__(self) -> None:
        self.storage_dir = Path(__file__).resolve().parents[2] / "uploads"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def extract_text(self, filename: str, content: bytes) -> str:
        extension = Path(filename).suffix.lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {extension}")

        if extension in self.MEDIA_EXTENSIONS:
            return (
                "Medya dosyası başarıyla yüklendi. "
                "Bu dosyayı sohbet içinde kullanmak için dosya URL'sini kullanabilirsiniz."
            )

        if extension == ".pdf":
            return self._extract_pdf(content)
        if extension in {".docx", ".doc"}:
            return self._extract_docx(content)
        if extension in {".xls", ".xlsx"}:
            return self._extract_excel(content)
        if extension == ".txt":
            return content.decode("utf-8", errors="replace")
        if extension == ".csv":
            return self._extract_csv(content)
        if extension == ".json":
            return self._extract_json(content)
        raise ValueError(f"Unsupported file type: {extension}")

    def save_file(self, user_id: int, filename: str, content: bytes) -> str:
        safe_filename = Path(filename).name
        user_folder = self.storage_dir / f"user_{user_id}"
        user_folder.mkdir(parents=True, exist_ok=True)
        target_path = user_folder / safe_filename
        target_path.write_bytes(content)
        return f"/uploads/user_{user_id}/{safe_filename}"

    def _extract_pdf(self, content: bytes) -> str:
        reader = PdfReader(io.BytesIO(content))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)

    def _extract_docx(self, content: bytes) -> str:
        document = Document(io.BytesIO(content))
        return "\n\n".join(paragraph.text for paragraph in document.paragraphs)

    def _extract_excel(self, content: bytes) -> str:
        data = pd.read_excel(io.BytesIO(content), engine="openpyxl")
        return data.to_csv(index=False)

    def _extract_csv(self, content: bytes) -> str:
        return content.decode("utf-8", errors="replace")

    def _extract_json(self, content: bytes) -> str:
        payload = json.loads(content.decode("utf-8", errors="replace"))
        return json.dumps(payload, indent=2, ensure_ascii=False)
