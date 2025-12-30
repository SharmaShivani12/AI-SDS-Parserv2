import fitz   # PyMuPDF
import requests, json
from .schemas import SDSExtracted

OLLAMA_URL = "http://localhost:11434/api/generate"

# -------------------------------
# PDF → TEXT EXTRACTOR
# -------------------------------
def extract_text_from_pdf(file_path: str) -> str:
    """Extract raw text from PDF using PyMuPDF"""
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text


# -------------------------------
# LLaMA SDS EXTRACTOR
# -------------------------------
def ask_llama(prompt: str, model="llama3"):
    """Send prompt to local LLaMA through Ollama"""
    payload = {
        "model": model,
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    
    res = requests.post(OLLAMA_URL, json=payload)
    return res.json()["response"]


def extract_sds_llama(text: str) -> SDSExtracted:
    prompt = f"""
You are a Safety Data Sheet (SDS) extraction assistant.
Extract key chemical safety information from the SDS text below
and return it in **valid JSON only**.

Return the output EXACTLY like this:

{{
 "product_name": string or null,
 "supplier": string or null,
 "cas_numbers": [string],
 "hazard_statements": [string],
 "precautionary_statements": [string],
 "signal_word": string or null,
 "pictograms": [string]
}}

SDS TEXT:
{text[:6000]}
"""

    response = ask_llama(prompt)

    # model sometimes wraps output in ``` or code blocks — clean it
    cleaned = response.strip().replace("```json", "").replace("```", "")

    data = json.loads(cleaned)

    return SDSExtracted(
        product_name=data.get("product_name"),
        supplier=data.get("supplier"),
        cas_numbers=data.get("cas_numbers", []),
        hazard_statements=data.get("hazard_statements", []),
        precautionary_statements=data.get("precautionary_statements", []),
        signal_word=data.get("signal_word"),
        pictograms=data.get("pictograms", [])
    )


# -------------------------------
# COMPATIBILITY FUNCTION
# Normal extraction route calls this
# -------------------------------
def extract_sds_data(text: str) -> SDSExtracted:
    """For now route default extraction to LLaMA"""
    return extract_sds_llama(text)
