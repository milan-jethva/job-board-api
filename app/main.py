from fastapi import FastAPI,Depends 
from app.api import user,auth , job,application
from app.api import admin
app = FastAPI()

@app.get("/")
def start():
    return {"ok": "done"}

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(job.router)
app.include_router(application.router)
app.include_router(admin.router)