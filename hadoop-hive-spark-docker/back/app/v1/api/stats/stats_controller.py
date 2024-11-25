from fastapi import APIRouter, status, Request, Depends
from fastapi.responses import JSONResponse
from app.v1.api.users.users_service import current_active_user

router = APIRouter(prefix="/stats", tags=["v1/stats"])

@router.post("/")
async def get_stats(
    request: Request,
    user=Depends(current_active_user)
):
    try:
        payload = await request.json()
        
        return JSONResponse(content=payload, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content="BAD_REQUEST", status_code=status.HTTP_400_BAD_REQUEST)
