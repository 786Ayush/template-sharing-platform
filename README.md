# Template Sharing Platform

A full-stack web application for sharing templates with role-based access control.

## 🚀 Live Demo

- **Frontend**: [https://template-sharing-platform-aai2qv98m-ayushs-projects-b553b367.vercel.app](https://template-sharing-platform-aai2qv98m-ayushs-projects-b553b367.vercel.app)
- **Backend API**: [https://template-sharing-platform1.onrender.com](https://template-sharing-platform1.onrender.com)
- **API Documentation**: [https://template-sharing-platform1.onrender.com/docs](https://template-sharing-platform1.onrender.com/docs)

## 🏗️ Architecture

- **Backend**: FastAPI (Python) deployed on Render
- **Frontend**: React (TypeScript) deployed on Vercel
- **Database**: MongoDB Atlas
- **File Storage**: MongoDB GridFS + Cloudinary (for images)
- **Authentication**: JWT tokens
- **Styling**: Tailwind CSS

## ✨ Features

- 🔐 **User Authentication**: Register/Login with JWT tokens
- 👥 **Role-based Access Control**: Admin and User roles
- 📄 **Template Management**: Full CRUD operations
- 🖼️ **Image Upload**: MongoDB GridFS + Cloudinary integration
- 📱 **Responsive Design**: Mobile-first with Tailwind CSS
- 🛡️ **Security**: CORS protection, input validation
- 🚀 **Production Ready**: Deployed on Render + Vercel

## Local Development

### Prerequisites

- Python 3.8+
- Node.js 14+
- MongoDB Atlas account
- Cloudinary account (for image storage)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file with your configuration:
   ```env
   MONGODB_URL=your_mongodb_connection_string
   DATABASE_NAME=template_sharing_db
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   BASE_URL=http://localhost:8000
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

5. Start the backend server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create/update `.env.local` file:
   ```env
   REACT_APP_API_URL=http://localhost:8000/api
   ```

4. Start the frontend development server:
   ```bash
   npm start
   ```

## Deployment

### Backend Deployment (Render)

1. Push your code to GitHub
2. Go to [Render](https://render.com) and sign in
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: `template-sharing-backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

6. Add environment variables in Render dashboard:
   - `MONGODB_URL`: Your MongoDB connection string
   - `DATABASE_NAME`: template_sharing_db
   - `SECRET_KEY`: Generate a secure secret key
   - `ALGORITHM`: HS256
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: 30
   - `BASE_URL`: https://your-service-name.onrender.com
   - `CLOUDINARY_CLOUD_NAME`: Your Cloudinary cloud name
   - `CLOUDINARY_API_KEY`: Your Cloudinary API key
   - `CLOUDINARY_API_SECRET`: Your Cloudinary API secret

### Frontend Deployment (Vercel)

#### Method 1: Vercel CLI
1. Install Vercel CLI globally:
   ```bash
   npm i -g vercel
   ```

2. Deploy from the frontend directory:
   ```bash
   cd frontend
   vercel --prod
   ```

3. Set environment variables in Vercel dashboard:
   - `REACT_APP_API_URL`: https://your-backend-service.onrender.com/api

#### Method 2: Vercel Dashboard
1. Go to [Vercel](https://vercel.com) and sign in
2. Import your GitHub repository
3. Set the root directory to `frontend`
4. Add environment variable:
   - `REACT_APP_API_URL`: https://your-backend-service.onrender.com/api

## Environment Variables

### Backend (.env)
```env
MONGODB_URL=mongodb+srv://...
DATABASE_NAME=template_sharing_db
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BASE_URL=https://your-backend-url.onrender.com
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Frontend (.env)
```env
REACT_APP_API_URL=https://your-backend-url.onrender.com/api
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

### Templates
- `GET /api/templates` - Get all templates
- `GET /api/templates/{id}` - Get template by ID
- `POST /api/templates` - Create new template (admin only)
- `PUT /api/templates/{id}` - Update template (admin only)
- `DELETE /api/templates/{id}` - Delete template (admin only)

### Images
- `GET /api/images/{image_id}` - Get image by ID

## File Structure

```
template-sharing-platform/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── auth.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   └── models.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   └── templates.py
│   │   ├── utils/
│   │   │   └── image_upload.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   └── types/
│   ├── package.json
│   ├── vercel.json
│   └── .env
├── render.yaml
├── deploy.sh
└── README.md
```

## Technologies Used

### Backend
- FastAPI
- Python 3.8+
- MongoDB with Motor (async driver)
- JWT for authentication
- Cloudinary for image storage
- Uvicorn ASGI server

### Frontend
- React 18
- TypeScript
- Redux Toolkit
- React Router
- Axios
- Tailwind CSS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please create an issue in the GitHub repository or contact the development team.

---

**Note**: Make sure to update the CORS origins in your backend after getting your Vercel deployment URL!
