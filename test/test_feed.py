"""Testes do Bolha do Feed;  —  rode com:  python3 -m unittest -v"""

import io
import unittest
from contextlib import redirect_stdout

from feed import BISCOITO, BOLACHA, Experimento, fatia, feed_de, main, rodar


class TestSimulacao(unittest.TestCase):
    def test_mesmo_universo_da_sempre_o_mesmo_feed(self):
        self.assertEqual(feed_de(7), feed_de(7))

    def test_feed_tem_o_tamanho_pedido(self):
        self.assertEqual(len(feed_de(1, Experimento(posts_por_dia=12))), 12)

    def test_os_dois_universos_do_video(self):
        self.assertEqual(fatia(feed_de(25)), 1.0)
        self.assertEqual(fatia(feed_de(2026)), 0.0)

    def test_os_numeros_do_video(self):
        r = rodar(1000)
        self.assertEqual((r.travou_no_biscoito, r.travou_na_bolacha), (661, 327))

    def test_sem_reforco_o_feed_fica_meio_a_meio(self):
        r = rodar(1000, Experimento(reforco=1.0))
        self.assertAlmostEqual(r.media_biscoito, 0.5, delta=0.02)
        self.assertEqual(r.travou_no_biscoito + r.travou_na_bolacha, 0)

    def test_quem_so_curte_um_assunto_trava_nele(self):
        exp = Experimento(gosto={BISCOITO: 1.0, BOLACHA: 0.0})
        self.assertEqual(rodar(50, exp).travou_no_biscoito, 50)


class TestFatia(unittest.TestCase):
    def test_conta_a_fracao_do_assunto(self):
        self.assertEqual(fatia([BISCOITO, BOLACHA, BISCOITO, BISCOITO]), 0.75)
        self.assertEqual(fatia([BISCOITO, BOLACHA], BOLACHA), 0.5)

    def test_feed_vazio(self):
        self.assertEqual(fatia([]), 0.0)


class TestParametrosInvalidos(unittest.TestCase):
    def test_recusa_parametros_sem_sentido(self):
        for kwargs in (
            {"dias": 0},
            {"posts_por_dia": 0},
            {"reforco": 0.9},
            {"gosto": {BISCOITO: 1.2, BOLACHA: 0.5}},
            {"gosto": {BISCOITO: 0.5}},
        ):
            with self.subTest(**{k: str(v) for k, v in kwargs.items()}), self.assertRaises(ValueError):
                Experimento(**kwargs)

    def test_recusa_zero_universos(self):
        with self.assertRaises(ValueError):
            rodar(0)


class TestLinhaDeComando(unittest.TestCase):
    def test_saida_igual_a_do_video(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            self.assertEqual(main([]), 0)
        self.assertEqual(
            saida.getvalue().splitlines(),
            [
                "universo 25:   feed 100% biscoito",
                "universo 2026: feed 0% biscoito",
                "travou no biscoito: 661 de 1000",
                "travou na bolacha:  327 de 1000",
                "sem algoritmo: feed 50% biscoito",
            ],
        )


if __name__ == "__main__":
    unittest.main()
