from fastapi import APIRouter, Request, Header
router = APIRouter()

@router.post("/github")
async def github_webhook(req: Request, x_hub_signature: str = Header(None)):
    payload = await req.json()
    # skeleton: map commit author email to employee and store Commit
    return {"ok": True}
