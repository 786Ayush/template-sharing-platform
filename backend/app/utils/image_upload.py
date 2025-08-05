import os
import base64
import time
from typing import Optional
from fastapi import UploadFile, HTTPException
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary (optional - for production image hosting)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

async def save_upload_file(upload_file: UploadFile) -> str:
    """
    Save uploaded file and return the file path or URL.
    For simplicity, we'll save files locally. In production, use cloud storage.
    """
    try:
        # Store image in MongoDB and return full image URL
        from app.core.database import store_image_in_mongo
        image_bytes = await upload_file.read()
        image_id = await store_image_in_mongo(image_bytes, upload_file.filename, upload_file.content_type)
        
        # Generate full URL
        base_url = os.getenv("BASE_URL", "http://localhost:8001")
        return f"{base_url}/api/images/{image_id}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

async def upload_to_cloudinary(upload_file: UploadFile) -> Optional[str]:
    """
    Upload file to Cloudinary and return the URL.
    This is optional and requires Cloudinary credentials.
    """
    try:
        if not all([
            os.getenv("CLOUDINARY_CLOUD_NAME"),
            os.getenv("CLOUDINARY_API_KEY"),
            os.getenv("CLOUDINARY_API_SECRET")
        ]):
            # Fall back to local storage
            return await save_upload_file(upload_file)
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            upload_file.file,
            folder="template_sharing",
            resource_type="image"
        )
        return result.get("secure_url")
    except Exception as e:
        # Fall back to local storage
        return await save_upload_file(upload_file)

def validate_image_file(upload_file: UploadFile) -> bool:
    """Validate if the uploaded file is an image"""
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
    return upload_file.content_type in allowed_types
