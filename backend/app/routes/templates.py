# Import all necessary libraries at the top for better organization
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.responses import Response
from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId

# Import our custom modules
from app.models.models import TemplateCreate, TemplateResponse, TemplateUpdate, ApiResponse
from app.routes.auth import get_current_user, get_admin_user
from app.core.database import get_database
from app.utils.image_upload import save_upload_file, validate_image_file

router = APIRouter(prefix="/templates", tags=["Templates"])

@router.post("/", response_model=ApiResponse)
async def create_template(
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_admin_user)
):
    """Create a new template (Admin only)"""
    try:
        # Validate image file
        if not validate_image_file(image):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file. Only JPEG, PNG, GIF, and WebP are allowed."
            )
        
        # Store image in MongoDB and get image_id
        from app.core.database import store_image_in_mongo
        image_bytes = await image.read()
        image_id = await store_image_in_mongo(image_bytes, image.filename, image.content_type)
        
        # Generate full image URL endpoint
        import os
        base_url = os.getenv("BASE_URL", "http://localhost:8000")
        image_url = f"{base_url}/api/images/{image_id}"

        db = await get_database()

        # Create template document
        template_doc = {
            "title": title,
            "description": description,
            "image_url": image_url,
            "image_id": str(image_id),
            "created_by": current_user["id"],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }

        result = await db.templates.insert_one(template_doc)

        return ApiResponse(
            success=True,
            message="Template created successfully",
            data={"template_id": str(result.inserted_id)}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create template: {str(e)}"
        )

@router.get("/", response_model=List[TemplateResponse])
async def get_templates(current_user: dict = Depends(get_current_user)):
    """Get all templates"""
    try:
        db = await get_database()
        
        templates_cursor = db.templates.find({})
        templates = []
        
        async for template in templates_cursor:
            template_response = TemplateResponse(
                id=str(template["_id"]),
                title=template["title"],
                description=template["description"],
                image_url=template["image_url"],
                created_by=template["created_by"],
                created_at=template["created_at"],
                updated_at=template["updated_at"]
            )
            templates.append(template_response)
        
        return templates
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch templates: {str(e)}"
        )

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific template by ID"""
    try:
        db = await get_database()
        
        if not ObjectId.is_valid(template_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid template ID format"
            )
        
        template = await db.templates.find_one({"_id": ObjectId(template_id)})
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        return TemplateResponse(
            id=str(template["_id"]),
            title=template["title"],
            description=template["description"],
            image_url=template["image_url"],
            created_by=template["created_by"],
            created_at=template["created_at"],
            updated_at=template["updated_at"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch template: {str(e)}"
        )

@router.put("/{template_id}", response_model=ApiResponse)
async def update_template(
    template_id: str,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_admin_user)
):
    """Update a template (Admin only)"""
    try:
        db = await get_database()
        
        if not ObjectId.is_valid(template_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid template ID format"
            )
        
        # Check if template exists
        template = await db.templates.find_one({"_id": ObjectId(template_id)})
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        # Build update document
        update_doc = {"updated_at": datetime.now(timezone.utc)}
        
        if title:
            update_doc["title"] = title
        if description:
            update_doc["description"] = description
        if image:
            if not validate_image_file(image):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid image file. Only JPEG, PNG, GIF, and WebP are allowed."
                )
            update_doc["image_url"] = await save_upload_file(image)
        
        # Update template
        await db.templates.update_one(
            {"_id": ObjectId(template_id)},
            {"$set": update_doc}
        )
        
        return ApiResponse(
            success=True,
            message="Template updated successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update template: {str(e)}"
        )

@router.delete("/{template_id}", response_model=ApiResponse)
async def delete_template(
    template_id: str,
    current_user: dict = Depends(get_admin_user)
):
    """Delete a template (Admin only)"""
    try:
        db = await get_database()
        
        if not ObjectId.is_valid(template_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid template ID format"
            )
        
        # Delete template
        result = await db.templates.delete_one({"_id": ObjectId(template_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        return ApiResponse(
            success=True,
            message="Template deleted successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete template: {str(e)}"
        )
