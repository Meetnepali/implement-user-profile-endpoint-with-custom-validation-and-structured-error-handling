from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, validator, constr
from typing import Optional, Dict

app = FastAPI()

# In-memory storage for profiles
profiles: Dict[str, Dict] = {}

# Error format helper
def error_response(code: int, message: str, details: Optional[dict] = None):
    err = {
        "error": {
            "code": code,
            "message": message
        }
    }
    if details:
        err["error"]["details"] = details
    return err

# Profile schema
class UserProfile(BaseModel):
    username: constr(min_length=3, max_length=20)
    email: EmailStr
    age: int
    bio: Optional[str] = ""

    @validator("username")
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric.")
        return v

    @validator("age")
    def age_range(cls, v):
        if v < 13 or v > 120:
            raise ValueError("Age must be between 13 and 120.")
        return v

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Custom 422 structure
    details = []
    for err in exc.errors():
        details.append({
            "loc": err["loc"],
            "msg": err["msg"],
            "type": err["type"]
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(422, "Validation Failed", details)
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Centralized error format for not found and other HTTPExceptions
    details = getattr(exc, "detail", None)
    if isinstance(details, dict):
        # for detail containing structured error already
        message = details.get("message", str(details))
        extra = details.get("details", None)
    else:
        message = details if isinstance(details, str) else str(exc.detail)
        extra = None
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.status_code, message, extra)
    )

@app.post("/profiles/", status_code=201)
def create_profile(profile: UserProfile):
    if profile.username in profiles:
        # Conflict, username exists (still use error format)
        raise HTTPException(status_code=409, detail={"message": "Username already exists."})
    profiles[profile.username] = profile.dict()
    return {"profile": profile.dict()}

@app.get("/profiles/{username}")
def get_profile(username: str):
    profile = profiles.get(username)
    if not profile:
        raise HTTPException(status_code=404, detail={"message": f"Profile '{username}' not found."})
    return {"profile": profile}
