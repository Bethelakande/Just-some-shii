from fastapi import APIRouter, HTTPException,Depends, Request
from ..database.db import create_challenge_quota
from ..database.models import get_db
from svix.webhooks import Webhook
import os
import json


load_dotenv()
router = APIRouter()

@router.post("/clerk")
async def clerk_webhook(request: Request, db = Depends(get_db)):
    try:
        webhook = os.getenv("CLERK_WEBHOOK_SECRET")
        if not webhook:
            raise HTTPException(status_code=500, detail="Webhook not found")


        body = await request.body()
        payload = body.decode("utf-8")
        header = dict(request.headers)

        try:
            wh = Webhook(webhook)
            wh.verify(payload, header)

            data = json.loads(payload)

            if data.get("type") != "user.created":

                return {"status": "ignored"}

            user_id = data.get("object").get("id")
            create_challenge_quota(db, user_id)
            return {"status": "success"}
        except Exception as e:
            logging.error(f"Error verifying webhook: {str(e)}")
            return {"status": "error"}
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return {"status": "error"}


