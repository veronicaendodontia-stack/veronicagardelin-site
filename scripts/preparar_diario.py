#!/usr/bin/env python3
"""Prepara publicações aprovadas para o Diário, sem publicar automaticamente.

Uso local: python scripts/preparar_diario.py --origem /caminho/privado --destino /caminho/saida
A origem deve ser uma cópia autorizada do repositório privado de rascunhos.
Requer: pip install pyyaml
"""
import argparse
import json
import shutil
from pathlib import Path
import yaml

CATEGORIAS = {"casos", "bastidores", "reflexoes"}

def preparar(origem: Path, destino: Path) -> int:
    rascunhos = origem / "diario" / "rascunhos"
    saida_imagens = destino / "diario" / "imagens"
    publicacoes = []
    if not rascunhos.is_dir():
        raise ValueError("Pasta de rascunhos não encontrada")
    for arquivo in sorted(rascunhos.glob("*.y*ml")):
        dados = yaml.safe_load(arquivo.read_text(encoding="utf-8"))
        if not isinstance(dados, dict) or dados.get("pronto") is not True:
            continue
        categoria = dados.get("categoria")
        legenda = dados.get("legenda")
        if categoria not in CATEGORIAS or not isinstance(legenda, str) or not legenda.strip():
            raise ValueError(f"Rascunho aprovado inválido: {arquivo.name}")
        foto = dados.get("fotografia") or ""
        url_foto = ""
        if foto:
            if not isinstance(foto, str):
                raise ValueError(f"Fotografia inválida: {arquivo.name}")
            caminho_relativo = foto.lstrip("/")
            if not caminho_relativo.startswith("diario/imagens/"):
                raise ValueError(f"Caminho de imagem inesperado: {arquivo.name}")
            imagem = (origem / caminho_relativo).resolve()
            raiz = (origem / "diario" / "imagens").resolve()
            if raiz not in imagem.parents or not imagem.is_file():
                raise ValueError(f"Imagem ausente ou inválida: {arquivo.name}")
            saida_imagens.mkdir(parents=True, exist_ok=True)
            shutil.copy2(imagem, saida_imagens / imagem.name)
            url_foto = "./diario/imagens/" + imagem.name
        publicacoes.append({"categoria": categoria, "legenda": legenda.strip(),
                            "fotografia": url_foto, "publicado": True})
    saida = destino / "diario" / "publicacoes.json"
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps(publicacoes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(publicacoes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--origem", type=Path, required=True)
    parser.add_argument("--destino", type=Path, required=True)
    args = parser.parse_args()
    print(f"{preparar(args.origem, args.destino)} publicações aprovadas preparadas.")
