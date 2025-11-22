from fastapi import FastAPI
from backend.app.routes import auth,social

app = FastAPI(title="InfluenceAI Backend", version="0.1")
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(social.router, prefix="/social", tags=["Social"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to InfluenceAI Backend"}


# run with
# uvicorn app.main:app --reload