#!/usr/bin/env python3
"""
Bolha do Feed;  —  um algoritmo de recomendação de brinquedo pra ver uma bolha nascer.
por Garoto do Programa;  (github.com/garotodoprograma404/bolha-do-feed)

A pessoa gosta quase igual de dois assuntos (biscoito 52%, bolacha 48%).
O algoritmo começa neutro e só tem uma regra: curtiu? mostra mais daquilo.
Depois de 30 dias, como fica o feed? E se a gente repetir isso em 1.000 universos?

Uso:
  python3 feed.py                       # o experimento do vídeo (1.000 universos)
  python3 feed.py --reforco 1.10        # algoritmo mais "agressivo"
  python3 feed.py --universos 10000     # mais universos
  python3 -m unittest -v                # roda os testes

Precisa só de Python 3.10+. Nenhuma biblioteca pra instalar.
É uma simulação didática: o algoritmo de verdade das redes usa milhares de sinais,
mas a regra central (o que prende mais aparece mais) é a mesma.
"""

from __future__ import annotations

import argparse
import random
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field

BISCOITO, BOLACHA = "biscoito", "bolacha"
TRAVOU = 0.9  # feed com 90% ou mais de um assunto = travou nele


def gosto_padrao() -> dict[str, float]:
    """Chance de a pessoa curtir cada assunto: quase empate."""
    return {BISCOITO: 0.52, BOLACHA: 0.48}


@dataclass(frozen=True)
class Experimento:
    """Os parâmetros de uma simulação (os padrões são os do vídeo)."""

    dias: int = 30
    posts_por_dia: int = 20
    reforco: float = 1.05  # quanto o peso de um assunto cresce a cada curtida
    gosto: dict[str, float] = field(default_factory=gosto_padrao)

    def __post_init__(self) -> None:
        if self.dias < 1 or self.posts_por_dia < 1:
            raise ValueError("dias e posts_por_dia precisam ser pelo menos 1")
        if self.reforco < 1:
            raise ValueError("reforco < 1 seria um algoritmo que esconde o que você curte")
        if len(self.gosto) < 2 or not all(0 <= p <= 1 for p in self.gosto.values()):
            raise ValueError("gosto precisa de 2+ assuntos, cada um com chance entre 0 e 1")


def curtiu(chance: float, rng: random.Random) -> bool:
    """Sorteia se a pessoa curtiu um post, dada a chance de curtir aquele assunto."""
    return rng.random() < chance


def feed_de(universo: int, exp: Experimento | None = None) -> list[str]:
    """Simula um universo e devolve o feed do último dia.

    O número do universo é a semente: o mesmo universo dá sempre o mesmo resultado.
    """
    exp = exp or Experimento()
    rng = random.Random(universo)
    peso = {assunto: 1.0 for assunto in exp.gosto}  # o algoritmo começa neutro
    feed: list[str] = []
    for _dia in range(exp.dias):
        feed = rng.choices(list(peso), weights=list(peso.values()), k=exp.posts_por_dia)
        for post in feed:
            if curtiu(exp.gosto[post], rng):
                peso[post] *= exp.reforco  # curtiu? mostra mais disso
    return feed


def fatia(feed: Sequence[str], assunto: str = BISCOITO) -> float:
    """Fração do feed ocupada por um assunto (0.0 a 1.0)."""
    return feed.count(assunto) / len(feed) if feed else 0.0


@dataclass(frozen=True)
class Resumo:
    universos: int
    travou_no_biscoito: int
    travou_na_bolacha: int
    media_biscoito: float


def rodar(universos: int, exp: Experimento | None = None) -> Resumo:
    """Roda os universos 0, 1, 2… e conta em quantos o feed travou em cada assunto."""
    if universos < 1:
        raise ValueError("universos precisa ser pelo menos 1")
    exp = exp or Experimento()
    feeds = [feed_de(u, exp) for u in range(universos)]
    return Resumo(
        universos=universos,
        # cada assunto é medido pela própria fatia: "1 - 0.9" daria 0.0999… e erraria a borda
        travou_no_biscoito=sum(fatia(f, BISCOITO) >= TRAVOU for f in feeds),
        travou_na_bolacha=sum(fatia(f, BOLACHA) >= TRAVOU for f in feeds),
        media_biscoito=sum(fatia(f, BISCOITO) for f in feeds) / universos,
    )


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Bolha do Feed: veja uma bolha nascer de uma regra só.")
    ap.add_argument("--universos", type=int, default=1000, help="quantos universos simular (padrão: 1000)")
    ap.add_argument("--dias", type=int, default=30, help="dias por universo (padrão: 30)")
    ap.add_argument("--posts", type=int, default=20, help="posts por dia no feed (padrão: 20)")
    ap.add_argument("--reforco", type=float, default=1.05, help="quanto cada curtida aumenta o peso (padrão: 1.05)")
    args = ap.parse_args(argv)

    try:
        exp = Experimento(dias=args.dias, posts_por_dia=args.posts, reforco=args.reforco)
        com = rodar(args.universos, exp)
        sem = rodar(args.universos, Experimento(dias=args.dias, posts_por_dia=args.posts, reforco=1.0))
    except ValueError as erro:
        ap.error(str(erro))

    print(f"universo 25:   feed {fatia(feed_de(25, exp)):.0%} biscoito")
    print(f"universo 2026: feed {fatia(feed_de(2026, exp)):.0%} biscoito")
    print(f"travou no biscoito: {com.travou_no_biscoito} de {com.universos}")
    print(f"travou na bolacha:  {com.travou_na_bolacha} de {com.universos}")
    print(f"sem algoritmo: feed {sem.media_biscoito:.0%} biscoito")
    return 0


if __name__ == "__main__":
    sys.exit(main())
