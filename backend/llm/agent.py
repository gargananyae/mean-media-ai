import json
import os
import requests

from backend.llm.prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE
)


OLLAMA_URL = "http://localhost:11434/api/generate"


def _format_data(data):
    """
    Convert Python dictionaries/lists into readable JSON.
    """
    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )


def _validate_analysis(result, recommendations):
    """
    Validate and repair the LLM response.

    The deterministic recommendation engine is the source of truth.
    The LLM is only allowed to explain those recommendations.
    """

    # -----------------------------------------
    # FALLBACK STRUCTURE
    # -----------------------------------------

    if not isinstance(result, dict):
        result = {}

    validated = {
        "executive_summary": result.get(
            "executive_summary",
            ""
        ),

        "strengths": (
            result.get("strengths", [])
            if isinstance(result.get("strengths", []), list)
            else []
        ),

        "weaknesses": (
            result.get("weaknesses", [])
            if isinstance(result.get("weaknesses", []), list)
            else []
        ),

        "priorities": [],

        "geo_insight": result.get(
            "geo_insight",
            ""
        ),

        "next_steps": (
            result.get("next_steps", [])
            if isinstance(result.get("next_steps", []), list)
            else []
        )
    }

    # -----------------------------------------
    # AUTHORITATIVE RECOMMENDATIONS
    # -----------------------------------------

    # These are the ONLY recommendations the AI
    # is allowed to discuss as priorities.

    deterministic_ids = []

    for recommendation in recommendations:

        recommendation_id = recommendation.get("id")

        if recommendation_id:
            deterministic_ids.append(
                recommendation_id
            )

    # -----------------------------------------
    # MATCH AI PRIORITIES TO REAL RECOMMENDATIONS
    # -----------------------------------------

    ai_priorities = result.get(
        "priorities",
        []
    )

    if not isinstance(ai_priorities, list):
        ai_priorities = []

    used_ids = set()

    for recommendation in recommendations:

        recommendation_id = recommendation.get(
            "id"
        )

        if not recommendation_id:
            continue

        # Try to find the AI's explanation
        # for this recommendation.

        matching_priority = None

        for priority in ai_priorities:

            if not isinstance(priority, dict):
                continue

            if priority.get(
                "recommendation_id"
            ) == recommendation_id:

                matching_priority = priority
                break

        # -----------------------------------------
        # USE AI EXPLANATION IF AVAILABLE
        # -----------------------------------------

        if matching_priority:

            action = matching_priority.get(
                "action",
                recommendation.get(
                    "recommendation",
                    ""
                )
            )

            why_it_matters = matching_priority.get(
                "why_it_matters",
                "This issue was identified by the deterministic Mean Media analysis engine."
            )

        # -----------------------------------------
        # OTHERWISE USE DETERMINISTIC DATA
        # -----------------------------------------

        else:

            action = recommendation.get(
                "recommendation",
                ""
            )

            why_it_matters = (
                "This issue was identified by "
                "the deterministic Mean Media "
                "analysis engine based on the "
                "measured website features."
            )

        validated["priorities"].append({

            "rank": len(
                validated["priorities"]
            ) + 1,

            "recommendation_id":
                recommendation_id,

            "action":
                action,

            "why_it_matters":
                why_it_matters
        })

        used_ids.add(
            recommendation_id
        )

        # Maximum 3 priorities
        if len(
            validated["priorities"]
        ) >= 3:

            break

    # -----------------------------------------
    # LIMIT STRENGTHS / WEAKNESSES
    # -----------------------------------------

    validated["strengths"] = (
        validated["strengths"][:3]
    )

    validated["weaknesses"] = (
        validated["weaknesses"][:3]
    )

    # -----------------------------------------
    # ENSURE AREA VALUES ARE VALID
    # -----------------------------------------

    valid_areas = {
        "SEO",
        "CONTENT",
        "TECHNICAL",
        "GEO"
    }

    for item in validated["strengths"]:

        if not isinstance(item, dict):
            continue

        if item.get("area") not in valid_areas:

            item["area"] = "CONTENT"

    for item in validated["weaknesses"]:

        if not isinstance(item, dict):
            continue

        if item.get("area") not in valid_areas:

            item["area"] = "CONTENT"

    return validated


def generate_ai_analysis(
    url,
    scores,
    features,
    recommendations
):
    """
    Generate structured AI interpretation of
    deterministic Mean Media analysis.

    IMPORTANT:

    The deterministic engine remains the source
    of truth.

    Ollama is only used to explain the results.
    """

    # -----------------------------------------
    # BUILD PROMPT
    # -----------------------------------------

    prompt = USER_PROMPT_TEMPLATE.format(
        url=url,
        scores=_format_data(scores),
        features=_format_data(features),
        recommendations=_format_data(
            recommendations
        )
    )

    # -----------------------------------------
    # OLLAMA REQUEST
    # -----------------------------------------

    payload = {
        "model": os.getenv(
            "LLM_MODEL",
            "llama3.2:3b"
        ),

        "prompt": (
            SYSTEM_PROMPT
            + "\n\n"
            + prompt
        ),

        "stream": False,

        "format": "json"
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

    except requests.exceptions.ConnectionError:

        return {
            "executive_summary":
                "AI analysis is currently unavailable because the local LLM service is not running.",

            "strengths": [],

            "weaknesses": [],

            "priorities": [],

            "geo_insight": "",

            "next_steps": []
        }

    except requests.exceptions.RequestException as error:

        return {
            "executive_summary":
                f"AI analysis could not be generated: {str(error)}",

            "strengths": [],

            "weaknesses": [],

            "priorities": [],

            "geo_insight": "",

            "next_steps": []
        }

    # -----------------------------------------
    # READ OLLAMA RESPONSE
    # -----------------------------------------

    try:

        response_data = response.json()

        raw_output = response_data.get(
            "response",
            ""
        )

    except Exception:

        raw_output = ""

    # -----------------------------------------
    # PARSE JSON
    # -----------------------------------------

    try:

        result = json.loads(
            raw_output
        )

    except json.JSONDecodeError:

        result = {
            "executive_summary":
                raw_output,

            "strengths": [],

            "weaknesses": [],

            "priorities": [],

            "geo_insight": "",

            "next_steps": []
        }

    # -----------------------------------------
    # VALIDATE AGAINST DETERMINISTIC ENGINE
    # -----------------------------------------

    return _validate_analysis(
        result,
        recommendations
    )