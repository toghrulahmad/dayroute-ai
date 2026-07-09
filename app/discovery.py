import os
import json
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatAnthropic(
    model="claude-sonnet-4-5",
    temperature=0.3,
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

discover_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Sən səyahət ekspertisən. İstifadəçinin verdiyi şəhər üçün "
        "mütləq görülməli 10 turist yerini təklif et. "
        "YALNIZ JSON formatında cavab ver, başqa heç nə yazma. "
        "Format: bir JSON array, hər elementdə: "
        "name (yerin tam adı, xəritədə tapıla bilən formada), "
        "category (məs: tarixi, təbiət, muzey, bazar), "
        "visit_duration_minutes (tövsiyə olunan ziyarət müddəti, dəqiqə)."
    )),
    ("human", "Şəhər: {city}"),
])

parser = StrOutputParser()

discovery_chain = discover_prompt | llm | parser


def discover_places(city: str) -> list[dict]:
    try:
        raw_result = discovery_chain.invoke({"city": city})
    except Exception as e:
        raise RuntimeError(f"AI modelinə müraciət uğursuz oldu: {e}")

    cleaned = raw_result.strip()
    if cleaned.startswith("```"):
        parts = cleaned.split("```")
        cleaned = parts[1] if len(parts) > 1 else cleaned
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        raise RuntimeError("AI modeli düzgün formatda cavab qaytarmadı, yenidən cəhd et")

    if not isinstance(result, list) or len(result) == 0:
        raise RuntimeError("AI modeli yer siyahısı qaytarmadı")

    return result

explain_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Sən səyahət ekspertisən. İstifadəçiyə bir günlük marşrut təklif edilib. "
        "Sənə seçilən yerlər, çıxarılan yerlər və ümumi vaxt veriləcək. "
        "Qısa, dostcasına, 3-4 cümləlik izahat yaz (Azərbaycan dilində): "
        "niyə bu yerlər seçildi, niyə digərləri sığmadı. "
        "Yalnız mətn qaytar, JSON yox."
    )),
    ("human", (
        "Seçilən yerlər: {selected}\n"
        "Çıxarılan yerlər: {excluded}\n"
        "Ümumi vaxt: {total_time} dəqiqə\n"
        "Vaxt limiti: {time_limit} dəqiqə"
    )),
])

explain_chain = explain_prompt | llm | parser


def explain_route(selected: list[dict], excluded: list[dict], total_time: float, time_limit: int) -> str:
    selected_names = ", ".join(p["name"] for p in selected)
    excluded_names = ", ".join(p["name"] for p in excluded) if excluded else "yoxdur"

    return explain_chain.invoke({
        "selected": selected_names,
        "excluded": excluded_names,
        "total_time": total_time,
        "time_limit": time_limit,
    })