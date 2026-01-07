# config/regras.py

# módulos que você quer rodar hoje
ATIVAR_RECEITA_TOTAL = True
ATIVAR_DESPESA_2384 = True

# IDs mais comuns no seu CSV atual:
PLANILHA_RECEITA_TOTAL = "1"
PLANILHA_DESPESA_2384 = "2384"

# Política quando faltar fonte:
# - "skip": não atualiza e só loga
# - "error": falha a execução
FALTA_FONTE = "skip"