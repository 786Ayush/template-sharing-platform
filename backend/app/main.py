from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.core.database import connect_to_mongo, close_mongo_connection
from app.routes import auth, templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Template Sharing Platform API",
    description="A platform for sharing templates with role-based access control",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",
        "https://template-sharing-platform-frontend.vercel.app",  # Production frontend URL
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Mount static files (for serving uploaded images)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(templates.router, prefix="/api")

# Image serving endpoint - serves images stored in MongoDB
@app.get("/api/images/{image_id}")
async def get_image(image_id: str):
    """Serve image from MongoDB by image_id"""
    from fastapi.responses import Response
    from bson import ObjectId
    from app.core.database import get_database
    
    try:
        db = await get_database()
        
        # Check if the image_id is a valid MongoDB ObjectId
        if not ObjectId.is_valid(image_id):
            raise HTTPException(status_code=400, detail="Invalid image ID format")
        
        # Find the image document in the database
        image_doc = await db.images.find_one({"_id": ObjectId(image_id)})
        if not image_doc:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Return the image data with the correct content type
        return Response(
            content=image_doc["data"], 
            media_type=image_doc.get("content_type", "image/png")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch image: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Template Sharing Platform API", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
