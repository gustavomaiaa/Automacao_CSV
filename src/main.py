# src/main.py
import os
from src.indexador import indexar_novos
from src.atualizador import atualizar_arquivo
from src.auditoria import escrever_cabecalho_auditoria

PASTA_ORIGINAL = "data/original"
PASTA_NOVOS = "data/novos_valores"
PASTA_SAIDA = "data/output"
PASTA_LOGS = "logs"

def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    os.makedirs(PASTA_LOGS, exist_ok=True)

    print("Indexando novos valores...")
    novos_index = {}

    for arquivo in os.listdir(PASTA_NOVOS):
        if arquivo.endswith(".csv"):
            novos_index.update(indexar_novos(os.path.join(PASTA_NOVOS, arquivo)))

    print(f"Registros novos indexados: {len(novos_index)}")

    caminho_auditoria = os.path.join(PASTA_LOGS, "auditoria_substituicoes.csv")
    total_subs = 0

    with open(caminho_auditoria, "w", encoding="latin1", newline="") as audit:
        escrever_cabecalho_auditoria(audit)

        for arquivo in os.listdir(PASTA_ORIGINAL):
            if arquivo.endswith(".csv"):
                print(f"Processando {arquivo}...")
                subs = atualizar_arquivo(
                    os.path.join(PASTA_ORIGINAL, arquivo),
                    os.path.join(PASTA_SAIDA, arquivo),
                    novos_index,
                    nome_arquivo=arquivo,
                    audit_file=audit
                )
                total_subs += subs
                print(f"  -> substituições: {subs}")

    print(f"Processamento concluído. Total de substituições: {total_subs}")
    print(f"Auditoria gerada em: {caminho_auditoria}")

if __name__ == "__main__":
    main()