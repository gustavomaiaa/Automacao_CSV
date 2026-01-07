import re
import pdfplumber
from collections import defaultdict

NUM_RE = re.compile(r"-?\d{1,3}(?:\.\d{3})*,\d{2}")
NAT_RE = re.compile(r"^(\d\.\d\.\d{2}\.\d{2}\.\d{2})\b")

def br_to_float(s: str) -> float:
    s = (s or "").strip()
    if not s:
        return 0.0
    return float(s.replace(".", "").replace(",", "."))

def extrair_despesa_educacao(pdf_path: str):
    """
    Retorna: { codigo8: [dot_atual, empenh, liq, pago] }
    """
    soma = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for raw in text.splitlines():
                line = re.sub(r"\s+", " ", raw.strip())
                m = NAT_RE.match(line)
                if not m:
                    continue

                codigo8 = m.group(1).replace(".", "")
                nums = NUM_RE.findall(line)
                if len(nums) < 5:
                    continue

                last5 = nums[-5:]
                dot_atual = br_to_float(last5[1])
                emp = br_to_float(last5[2])
                liq = br_to_float(last5[3])
                pag = br_to_float(last5[4])

                acc = soma[codigo8]
                acc[0] += dot_atual
                acc[1] += emp
                acc[2] += liq
                acc[3] += pag

    return soma