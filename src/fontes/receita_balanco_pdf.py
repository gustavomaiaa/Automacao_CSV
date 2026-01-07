import re
import pdfplumber

CODE_RE = re.compile(r"^\s*(\d(?:\.\d+)+)\s+")
NUM_RE  = re.compile(r"-?\d{1,3}(?:\.\d{3})*,\d{2}")

def br_to_float(s: str) -> float:
    s = (s or "").strip()
    if not s:
        return 0.0
    return float(s.replace(".", "").replace(",", "."))

def code_to_siope8(code_dot: str) -> str:
    digits = re.sub(r"\D", "", code_dot or "")
    return digits[:8] if len(digits) >= 8 else ""

def extrair_receita_balanco(pdf_path: str):
    """
    Retorna: { codigo8: (orcada, ate_mes) }
    """
    res = {}
    last = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(layout=True) or ""
            for raw in text.splitlines():
                line = raw.strip()

                m = CODE_RE.match(line)
                if m:
                    c8 = code_to_siope8(m.group(1))
                    if c8:
                        last = c8
                    continue

                nums = NUM_RE.findall(line)
                if last and len(nums) >= 5:
                    orcada = br_to_float(nums[0])
                    ate_mes = br_to_float(nums[4])
                    res[last] = (orcada, ate_mes)
                    last = ""

    return res