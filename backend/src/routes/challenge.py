from fastapi import APIRouter, HTTPException,Depends, Request, File, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.db import   (
    create_Challenge,
    get_challenges,
    create_challenge_quota,
    get_challenge_quota,
    reser_quota_if_needed
)
from ..ai_generator import generate_challenge
from ..utils import authenticate_and_get_user_details
from ..database.models import Challenge, get_db
import json
from datetime import datetime
import shutil
import os
from ..vector import vectorize

router = APIRouter()


class CreateChallenge(BaseModel):
    difficulty: str


    class Config:
        json_schema_extra = {
            "example": {
                "difficulty": "easy"
            }
        }

@router.get("/my-history")
async def my_history(request: Request, db: Session = Depends(get_db)):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("User_id")

    challenges = get_challenges(db, user_id)
    return {"challenges": challenges} 
    
@router.get("/quota")
async def quota(request: Request, db: Session = Depends(get_db)):
    print('request: ',request)
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("User_id")

    quota = get_challenge_quota(db, user_id)
    if not quota:
        return {"user_id": user_id,"quota_remaining":0,"last_reset_date":datetime.now()}
    quota = reser_quota_if_needed(db, quota)
    return {"quota": quota}

@router.post("/create_challenge")
async def create_challenge( request: CreateChallenge, request_obj: Request, db: Session = Depends(get_db)):
    try:
        print('request: ',request_obj)
        user_details = authenticate_and_get_user_details(request_obj)
        user_id = user_details.get("User_id")

        print('difficulty: ', request.difficulty)

        quota = get_challenge_quota(db, user_id)
        if not quota:
            quota = create_challenge_quota(db, user_id)
            #quota = get_challenge_quota(db, user_id)
        print('quota: ',quota)
        

        retriever = vectorize(insert_document=True)
        text = retriever.invoke(f"You are a questioner of ten years experience; Get relevant questions from the uploaded document of difficulty level {request.difficulty}; Give the information and suggested questions and their titles you can ask based of the section of information you are bringing out; also give the right answer to the question based of the document")
        Challenge = generate_challenge(request.difficulty,text)

        print('Challenge: ',Challenge)

        quota = reser_quota_if_needed(db, quota)
        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Quota Not Available")
        quota.quota_remaining -= 1
        db.commit()
        db.refresh(quota)

        new_challenge = create_Challenge(db=db, 
        created_by=user_id, 
        difficulty=request.difficulty, 
        title=Challenge["title"], 
        options=json.dumps(Challenge["options"]), 
        correct_answer_id=Challenge["correct_answer_id"], 
        explanation=Challenge["explanation"])

        return {"id": new_challenge.id,
        "difficulty": new_challenge.difficulty,
        "title": new_challenge.title,
        "options": new_challenge.options,
        "correct_answer_id": new_challenge.correct_answer_id,
        "explanation": new_challenge.explanation,
        "timestamp": new_challenge.date_created.strftime("%Y-%m-%d %H:%M:%S")}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        print("=================Debug Info starting upload=================")
        print('file info: ', {
            'filename': file.filename,
            'content_type': file.content_type,
        })
        upload_dir = "uploads/"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    