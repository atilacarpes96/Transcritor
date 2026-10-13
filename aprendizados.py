"""Addon de aprendizados: guarda o que cada video transcrito ensinou e ajuda a lembrar depois.

Os arquivos ficam em aprendizados\\ (fora do git, sao pessoais). Os modelos estao em
aprendizados-modelo\\.

Uso:
  python aprendizados.py iniciar                       cria aprendizados\\ com o INDICE.md
  python aprendizados.py novo "assunto" [--url URL] [--titulo T] [--data AAAA-MM-DD]
                                                       cria o arquivo do video a partir do modelo
  python aprendizados.py listar                        mostra os videos registrados
  python aprendizados.py buscar termo [termo ...]      procura nos aprendizados e nas transcricoes

O texto das licoes quem escreve e o Claude (skill "transcrever-youtube", passo 4) ou voce.
"""

import argparse
import datetime
import glob
import os
import re
import shutil
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.join(AQUI, "aprendizados")
MODELOS = os.path.join(AQUI, "aprendizados-modelo")
PASTA_VIDEOS = os.path.join(AQUI, "videos")
INDICE = os.path.join(PASTA, "INDICE.md")


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60]


def sem_acento(texto):
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


def iniciar(_args=None):
    os.makedirs(PASTA, exist_ok=True)
    if not os.path.exists(INDICE):
        shutil.copy(os.path.join(MODELOS, "INDICE.md"), INDICE)
        print(f"criado {INDICE}")
    else:
        print(f"ja existe {INDICE}")


def novo(args):
    iniciar()
    data = args.data or datetime.date.today().isoformat()
    caminho = os.path.join(PASTA, f"{data}-{slug(args.assunto)}.md")
    if os.path.exists(caminho):
        sys.exit(f"ja existe {caminho}")
    with open(os.path.join(MODELOS, "MODELO.md"), encoding="utf-8") as f:
        texto = f.read()
    d = datetime.date.fromisoformat(data)
    texto = (texto.replace("{titulo}", args.titulo or args.assunto)
                  .replace("{url}", args.url or "")
                  .replace("{data}", d.strftime("%d/%m/%Y")))
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)
    print(caminho)
    print("Lembre de acrescentar uma linha nas duas tabelas do INDICE.md.")


def listar(_args):
    arquivos = sorted(glob.glob(os.path.join(PASTA, "????-??-??-*.md")), reverse=True)
    if not arquivos:
        print("nenhum aprendizado ainda (use: python aprendizados.py novo \"assunto\")")
    for a in arquivos:
        with open(a, encoding="utf-8") as f:
            titulo = f.readline().lstrip("# ").strip()
        print(f"{os.path.basename(a)[:10]}  {titulo}")


def buscar(args):
    termos = [sem_acento(t) for t in args.termos]
    alvos = glob.glob(os.path.join(PASTA, "*.md")) + \
        glob.glob(os.path.join(PASTA_VIDEOS, "**", "*.txt"), recursive=True)
    achou = 0
    for a in sorted(alvos):
        try:
            with open(a, encoding="utf-8") as f:
                linhas = f.readlines()
        except (OSError, UnicodeDecodeError):
            continue
        for n, linha in enumerate(linhas, 1):
            l = sem_acento(linha)
            if all(t in l for t in termos):
                print(f"{os.path.relpath(a, AQUI)}:{n}: {linha.strip()[:160]}")
                achou += 1
    if not achou:
        print("nada encontrado")


def main():
    p = argparse.ArgumentParser(description="Aprendizados dos videos transcritos")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("iniciar").set_defaults(f=iniciar)
    n = sub.add_parser("novo")
    n.add_argument("assunto")
    n.add_argument("--url")
    n.add_argument("--titulo")
    n.add_argument("--data")
    n.set_defaults(f=novo)
    sub.add_parser("listar").set_defaults(f=listar)
    b = sub.add_parser("buscar")
    b.add_argument("termos", nargs="+")
    b.set_defaults(f=buscar)
    args = p.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
