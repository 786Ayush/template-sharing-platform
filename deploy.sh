#!/bin/bash

echo "🚀 Starting deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_status "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    print_warning "You have uncommitted changes. Committing them now..."
    git add .
    git commit -m "Pre-deployment commit: $(date)"
fi

print_status "Git repository is ready for deployment!"

echo ""
echo "📋 Deployment Checklist:"
echo "========================"
echo ""
echo "🔧 BACKEND DEPLOYMENT (Render):"
echo "1. Go to https://render.com and sign in"
echo "2. Click 'New +' and select 'Web Service'"
echo "3. Connect your GitHub repository"
echo "4. Use the following settings:"
echo "   - Name: template-sharing-backend"
echo "   - Root Directory: (leave empty)"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r backend/requirements.txt"
echo "   - Start Command: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "5. Add these environment variables in Render:"
echo "   - MONGODB_URL: (your MongoDB connection string)"
echo "   - DATABASE_NAME: template_sharing_db"
echo "   - SECRET_KEY: (generate a secure key)"
echo "   - ALGORITHM: HS256"
echo "   - ACCESS_TOKEN_EXPIRE_MINUTES: 30"
echo "   - BASE_URL: https://your-backend-service-name.onrender.com"
echo "   - CLOUDINARY_CLOUD_NAME: (your Cloudinary cloud name)"
echo "   - CLOUDINARY_API_KEY: (your Cloudinary API key)"
echo "   - CLOUDINARY_API_SECRET: (your Cloudinary API secret)"
echo ""

echo "🌐 FRONTEND DEPLOYMENT (Vercel):"
echo "1. Install Vercel CLI: npm i -g vercel"
echo "2. From the frontend directory, run: vercel"
echo "3. Follow the prompts:"
echo "   - Link to existing project: N"
echo "   - Project name: template-sharing-platform-frontend"
echo "   - Directory: ./frontend"
echo "   - Override settings: N"
echo ""
echo "4. Set environment variable in Vercel dashboard:"
echo "   - REACT_APP_API_URL: https://your-backend-service-name.onrender.com/api"
echo ""

echo "🔄 ALTERNATIVE - Deploy Frontend with Vercel CLI:"
echo "Run this command from the project root:"
echo "cd frontend && vercel --prod"
echo ""

print_status "All files have been prepared for deployment!"
print_warning "Remember to update the CORS origins in your backend after you get your Vercel URL!"

echo ""
echo "📁 Files created/updated:"
echo "- render.yaml (backend deployment config)"
echo "- frontend/vercel.json (frontend deployment config)"
echo "- frontend/.env (updated with production API URL)"
echo "- frontend/.env.local (local development API URL)"
echo "- backend/app/main.py (updated CORS origins)"
echo ""

print_status "Deployment preparation complete! 🎉"
