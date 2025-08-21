# backend/routers/agent.py
from fastapi import APIRouter, HTTPException
from backend.logging_config import logger
from backend.schemas import ChatMessageRequest, ChatMessageResponse, PlanResponse
from backend.services.nlp import parse_goal_text, _extract_year, _extract_amount, _extract_event_name  # type: ignore
from backend.services.planner import plan_event
from backend.services.market import fetch_index_summary

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)

@router.post("/chat", response_model=ChatMessageResponse)
def chat(req: ChatMessageRequest):
    text = (req.message or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="message cannot be empty")

    reply_lines = []
    plan_data: PlanResponse | None = None  # type: ignore[assignment]
    market = None

    # Try parsing a goal from free text
    try:
        event_name, today_cost, target_year = parse_goal_text(text)
        p = plan_event(event_name, float(today_cost), int(target_year))
        plan_data = PlanResponse(**p)
        reply_lines.append(
            f"Planned '{plan_data.event_name}' for {plan_data.target_year}. Future cost ≈ ₹{int(plan_data.future_cost):,}. "
            f"You'd need ≈ ₹{int(plan_data.monthly_saving_needed):,}/month."
        )
    except Exception as e:
        logger.info("parse_goal_text failed; attempting fallback parsing", extra={"err": str(e)})
        # Fallback: best-effort extraction; only plan if both amount and year are present
        try:
            event_name_fb = _extract_event_name(text)
            amount_fb = _extract_amount(text)
            year_fb = _extract_year(text)
            if amount_fb is not None and year_fb is not None:
                p = plan_event(event_name_fb, float(amount_fb), int(year_fb))
                plan_data = PlanResponse(**p)
                reply_lines.append(
                    f"Planned '{plan_data.event_name}' for {plan_data.target_year}. Future cost ≈ ₹{int(plan_data.future_cost):,}. "
                    f"You'd need ≈ ₹{int(plan_data.monthly_saving_needed):,}/month."
                )
        except Exception as e2:
            logger.info("Fallback parsing also failed", extra={"err": str(e2)})

    # If the user asks about the market, fetch summary
    lowered = text.lower()
    market_keywords = {"market", "nifty", "sensex", "index", "stock", "stocks", "indices", "nse", "bse"}
    if any(k in lowered for k in market_keywords):
        try:
            market = fetch_index_summary()
            n = market.get("NIFTY_50", {})
            s = market.get("SENSEX", {})
            reply_lines.append(
                f"Market: NIFTY 50 {n.get('last_price', '—')} {n.get('currency', '')}, "
                f"SENSEX {s.get('last_price', '—')} {s.get('currency', '')}."
            )
        except Exception as e:
            logger.warning("Market summary fetch failed", extra={"err": str(e)})

    if not reply_lines:
        reply_lines.append(
            "I can help set goals from natural language (e.g., 'Plan wedding Dec 2026 for 8L') and share market summaries. Ask me!"
        )

    return ChatMessageResponse(
        reply=" ".join(reply_lines),
        plan=plan_data,
        market_summary=market,
    )
