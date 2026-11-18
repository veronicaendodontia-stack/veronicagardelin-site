#!/usr/bin/env python3
"""Gera o índice público a partir das entradas YAML aprovadas no Pages CMS.

Executar a partir da raiz do repositório: python3 scripts/gerar_indice_diario.py
Não acessa rascunhos privados nem publica alterações por conta própria.
"""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTRADAS = ROOT / "diario" / "publicacoes"
SAIDA = ROOT / "diario" / "publicacoes.json"
CATEGORIAS = {"casos", "bastidores", "reflexoes"}

def gerar():
    publicacoes = []
    if ENTRADAS.exists():
        for arquivo in sorted([*ENTRADAS.glob("*.yaml"), *ENTRADAS.glob("*.yml")]):
            dados = yaml.safe_load(arquivo.read_text(encoding="utf-8"))
            if not isinstance(dados, dict) or dados.get("publicado") is not True:
                continue
            categoria = dados.get("categoria")
            legenda = dados.get("legenda")
            if categoria not in CATEGORIAS or not isinstance(legenda, str) or not legenda.strip():
                raise ValueError(f"Entrada pública inválida: {arquivo.name}")
            foto = dados.get("fotografia") or ""
            if not isinstance(foto, str):
                raise ValueError(f"Fotografia inválida: {arquivo.name}")
            if foto and not foto.startswith("/diario/imagens/"):
                raise ValueError(f"Fotografia fora da pasta permitida: {arquivo.name}")
            publicacoes.append({
                "categoria": categoria,
                "fotografia": foto,
                "legenda": legenda.strip(),
                "publicado": True,
            })
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(publicacoes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Índice gerado com {len(publicacoes)} publicações aprovadas.")

if __name__ == "__main__":
    gerar()
