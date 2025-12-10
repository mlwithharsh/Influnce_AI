from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import auth, social

app = FastAPI(title="InfluenceAI Backend", version="0.1")

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(social.router, prefix="/social", tags=["Social"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to InfluenceAI Backend"}