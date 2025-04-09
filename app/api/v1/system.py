from fastapi import APIRouter, Depends
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.deps import get_db
import logging


router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "ok", "message": "Server is alive."}

# @router.get("/health", summary="Health check")
# def health_check(db: Session = Depends(get_db)):
#     version = db.execute(text("SELECT version()")).scalar()
#     current_db = db.execute(text("SELECT current_database()")).scalar()
#     return {
#         "status": "ok",
#         "database": current_db,
#         "db_version": version
#     }
@router.get("/health", summary="Health Check", description="Check DB connectivity")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))  # ✅ wrap with text()
        return {"status": "ok"}
    except Exception as e:
        import logging
        logging.error(f"Health check failed: {e}")
        return {
            "error": "An unexpected error occurred",
            "type": "ServerError",
            "detail": str(e),
        }


@router.get("/version")
async def version():
    return {
        "version": settings.APP_VERSION,
        "environment": settings.ENV
    }