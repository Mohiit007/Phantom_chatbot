from fastapi import APIRouter, HTTPException
from backend.schemas import ParseTextRequest, ParseTextResponse
from backend.services.nlp import parse_goal_text

router = APIRouter(prefix="/nlp", tags=["NLP"])


@router.post("/parse", response_model=ParseTextResponse)
def parse_text(request: ParseTextRequest):
    try:
        event_name, today_cost, target_year = parse_goal_text(request.text)
        return ParseTextResponse(event_name=event_name, today_cost=today_cost, target_year=target_year)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) 