from fastapi import APIRouter
from fastapi import Depends
import requests
from bot_trainer.api.auth import Authentication
from bot_trainer.api.models import *
from bot_trainer.utils import Utility
router = APIRouter()
auth = Authentication()


@router.post("/questions", response_model=Response)
async def questions(request_data: RequestData, current_user: User = Depends(auth.get_current_user)):
    response = requests.post(Utility.environment['augmentation_url'], json=request_data.data)
    return response
