import re
import json
from state import State


def summarize_conversation(state: State, llm_summary):
    """
    This function is triggered ONLY after call_status == 'END'
    It performs post-call analytics and returns a structured summary.
    """

    conversation = state["conversation"]

    summary_prompt = """
You are a post-call reporting assistant for the Dial 122 Emergency Response System (Demo).

You will receive the full conversation between:
- Caller (citizen)
- Dial-122 female call-handling officer

Your task is to produce a STRUCTURED OPERATIONAL SUMMARY for review and audit.

Extract the following fields as TOP-LEVEL JSON KEYS.
If a field is not available or unclear, set it to null.

{
  "CallDisposition": "Emergency Confirmed / False Alarm / Information Only / Call Dropped / Unclear",
  "EmergencyType": "Medical / Accident / Fire / Crime / Domestic Violence / Women Related / Child Related / Traffic / Other",
  "CallerName": null,
  "CallerPhoneNumber": null,
  "Location": null,
  "Landmark": null,
  "InjuriesReported": true/false/null,
  "NumberOfPeopleInvolved": null,
  "WeaponsOrFireMentioned": true/false/null,
  "RiskLevel": "High / Medium / Low",
  "Language": "Hindi / Hinglish",
  "AgentActionSummary": "Short factual description of what the agent did",
  "OverallSummary": "2–3 line neutral factual summary of the call"
}

IMPORTANT RULES:
- Output ONLY valid JSON.
- Do NOT include markdown.
- Do NOT add explanations or commentary.
- Do NOT hallucinate missing information.
- Keep tone neutral, factual, and operational.
"""

    messages = [
        {"role": "system", "content": summary_prompt},
        {"role": "user", "content": str(conversation)}
    ]

    response = llm_summary.invoke(messages)
    raw_summary = response.content

    # ---- JSON cleanup & safety (as in your original logic) ----
    try:
        cleaned = re.sub(r"\bNone\b", "null", raw_summary)
        parsed = json.loads(cleaned)
        final_summary = json.dumps(parsed, ensure_ascii=False)
    except Exception:
        # If parsing fails, return raw model output safely
        final_summary = raw_summary

    return final_summary
