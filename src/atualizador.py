# src/atualizador.py
from config.siope_layout import COL_TIPO, COL_CODIGO, COL_BIMESTRE
from src.leitor_stream import ler_linhas
from src.escritor_csv import escrever_linha
from src.auditoria import registrar_auditoria

def atualizar_arquivo(caminho_original, caminho_saida, novos_index, nome_arquivo, audit_file=None):
    substituidas = 0
    with open(caminho_saida, "w", encoding="latin1", newline="") as out:
        for numero_linha, cols in ler_linhas(caminho_original):

            if cols[COL_TIPO] == "D":
                chave = (cols[COL_CODIGO], cols[COL_BIMESTRE])
                if chave in novos_index:
                    cols_nova = novos_index[chave]
                    if audit_file is not None:
                        registrar_auditoria(audit_file, nome_arquivo, numero_linha, cols, cols_nova)
                    escrever_linha(out, cols_nova)
                    substituidas += 1
                    continue

            escrever_linha(out, cols)

    return substituidas