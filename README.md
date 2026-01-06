# Automação SIOPE (CSV) — Substituição por (código, bimestre)

Projeto em Python para automatizar a atualização de valores em CSVs exportados do SIOPE,
evitando trabalho manual no escritório.

## Estrutura de pastas

- `data/original/` → CSVs exportados do SIOPE (originais)
- `data/novos_valores/` → CSVs com valores corrigidos
- `data/output/` → CSVs finais prontos para importação no SIOPE
- `logs/` → auditoria e relatórios

> Observação: os CSVs não sobem para o GitHub (estão no `.gitignore`).

## Como usar

### 1) Coloque os arquivos
- Coloque os CSVs exportados do SIOPE em: `data/original/`
- Coloque os CSVs com valores corrigidos em: `data/novos_valores/`

### 2) (Opcional) Confirmar layout real do SIOPE
```bash
python src/inspecionar_layout.py