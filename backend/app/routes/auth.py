from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone
from app.models.models import UserCreate, UserLogin, Token, UserResponse, ApiResponse
from app.core.auth import get_password_hash, verify_password, create_access_token, verify_token
from app.core.database import get_database

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post("/register", response_model=ApiResponse)
async def register(user: UserCreate):
    """Register a new user"""
    try:
        db = await get_database()
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = get_password_hash(user.password)
        user_doc = {
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "password": hashed_password,
            "created_at": datetime.now(timezone.utc)
        }
        
        result = await db.users.insert_one(user_doc)
        
        return ApiResponse(
            success=True,
            message="User registered successfully",
            data={"user_id": str(result.inserted_id)}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Authenticate user and return access token"""
    try:
        db = await get_database()
        
        # Find user by email
        user = await db.users.find_one({"email": user_credentials.email})
        if not user or not verify_password(user_credentials.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user["email"], "role": user["role"]}
        )
        
        # Prepare user response
        user_response = UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            username=user["username"],
            role=user["role"],
            created_at=user["created_at"]
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    try:
        payload = verify_token(credentials.credentials)
        email = payload.get("sub")
        
        db = await get_database()
        user = await db.users.find_one({"email": email})
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "id": str(user["_id"]),
            "email": user["email"],
            "username": user["username"],
            "role": user["role"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_admin_user(current_user: dict = Depends(get_current_user)):
    """Ensure current user is admin"""
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
