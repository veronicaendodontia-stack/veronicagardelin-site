import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import gerar_indice_diario as modulo


class DiarioIndiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.entradas = self.raiz / "diario" / "publicacoes"
        self.entradas.mkdir(parents=True)
        self.saida = self.raiz / "diario" / "publicacoes.json"

    def escrever(self, nome, conteudo):
        (self.entradas / nome).write_text(conteudo, encoding="utf-8")

    def gerar(self):
        with patch.object(modulo, "ENTRADAS", self.entradas), patch.object(modulo, "SAIDA", self.saida):
            modulo.gerar()
        return json.loads(self.saida.read_text(encoding="utf-8"))

    def test_somente_aprovados(self):
        self.escrever("aprovado.yaml", "categoria: reflexoes\\nlegenda: Texto público\\npublicado: true\\n".replace("\\n", "\n"))
        self.escrever("rascunho.yaml", "categoria: bastidores\\nlegenda: Texto privado\\npublicado: false\\n".replace("\\n", "\n"))
        resultado = self.gerar()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["legenda"], "Texto público")

    def test_sem_publicacoes(self):
        self.assertEqual(self.gerar(), [])

    def test_categoria_invalida_interrompe(self):
        self.escrever("erro.yaml", "categoria: outra\\nlegenda: Texto\\npublicado: true\\n".replace("\\n", "\n"))
        with self.assertRaises(ValueError):
            self.gerar()


if __name__ == "__main__":
    unittest.main()
