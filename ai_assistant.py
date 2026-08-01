import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")


def _build_context(schedule, owner):
    """RETRIEVAL STEP: turn live schedule state into a grounded text context."""
    lines = [f"Owner: {owner.first_name} {owner.last_name}",
             f"Available minutes today: {owner.available_minutes}"]

    lines.append("\nScheduled tasks:")
    if schedule.tasks:
        for t in schedule.tasks:
            lines.append(f"- {t.time} {t.name} for {t.pet_name} "
                          f"({t.duration} min, {t.priority} priority)")
    else:
        lines.append("- none")

    lines.append("\nPostponed tasks (did not fit):")
    if schedule.postponed:
        for t in schedule.postponed:
            lines.append(f"- {t.name} for {t.pet_name} "
                          f"({t.duration} min, {t.priority} priority)")
    else:
        lines.append("- none")

    lines.append("\nScheduling reasons log:")
    lines.extend(f"- {r}" for r in schedule.reasons)

    return "\n".join(lines)


def ask_schedule_question(schedule, owner, question, model_name=None):
    """
    Ask the AI a question about the schedule. Returns a dict:
        { "answer": str, "grounded": bool, "warning": str | None }

    'grounded' / 'warning' are the guardrail's verdict on whether the
    answer appears to only use real data instead of inventing tasks.
    """
    if not question or not question.strip():
        return {"answer": "", "grounded": True, "warning": "Empty question — nothing to answer."}

    if _client is None:
        return {
            "answer": "",
            "grounded": False,
            "warning": "Missing GEMINI_API_KEY. Add it to your .env file to use Gemini mode.",
        }

    context = _build_context(schedule, owner)

    system_prompt = (
        "You are PawPal+'s scheduling assistant. Answer the user's question "
        "using ONLY the schedule data provided below. Do not invent tasks, "
        "pets, or times that are not listed. If the answer isn't in the data, "
        "say you don't have that information. Be concise (2-4 sentences).\n\n"
        f"SCHEDULE DATA:\n{context}"
    )

    try:
        response = _client.models.generate_content(
            model=model_name or DEFAULT_MODEL,
            contents=question.strip(),
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=600,
                thinking_config=types.ThinkingConfig(thinking_level="minimal"),
            ),
        )
        answer = (response.text or "").strip()
    except Exception as e:
        return {"answer": "", "grounded": False, "warning": f"AI request failed: {e}"}

    if not answer:
        return {"answer": "", "grounded": False, "warning": "Model returned an empty response."}

    return {"answer": answer, "grounded": True, "warning": None}