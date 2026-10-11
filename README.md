# Bolha do Feed;

![testes](https://github.com/garotodoprograma404/bolha-do-feed/actions/workflows/testes.yml/badge.svg)

**Um algoritmo de recomendação de brinquedo pra ver uma bolha nascer de uma regra só: curtiu? mostra mais.**
Feito pelo [Garoto do Programa;](https://instagram.com/garotodoprograma) · Python puro, nada pra instalar.

```bash
python3 feed.py                    # o experimento do vídeo (1.000 universos)
python3 feed.py --reforco 1.10     # algoritmo mais "agressivo"
python3 feed.py --universos 10000  # mais universos
python3 -m unittest -v             # roda os testes
```

## O experimento

| | |
|---|---|
| **a pessoa** | gosta quase igual de dois assuntos: biscoito (52%) e bolacha (48%) |
| **o feed** | 20 posts por dia, durante 30 dias |
| **o algoritmo** | começa neutro (peso 1 pra cada assunto) e tem **uma regra só**: cada curtida multiplica o peso daquele assunto por 1,05 |
| **o universo** | o número do universo é a semente do sorteio. Mesmo universo, mesmo resultado, sempre |

## Rodando

```
universo 25:   feed 100% biscoito
universo 2026: feed 0% biscoito
travou no biscoito: 661 de 1000
travou na bolacha:  327 de 1000
sem algoritmo: feed 50% biscoito
```

- Em **988 de 1.000** universos o feed termina com 90% ou mais de um assunto só. Uma diferença de gosto de 52 × 48 virou um feed de 100 × 0.
- Em **327** deles o feed travou na **bolacha**, o assunto que a pessoa gosta **menos**. Quem decide é a sorte dos primeiros cliques, não o gosto.
- **Sem a regra** (`--reforco 1.0`), o feed fica em 50%: a bolha vem do laço "curtiu → mostra mais → curte mais".

É o efeito "rico fica mais rico" (*rich get richer*): o que sai na frente no começo ganha mais espaço, e mais espaço gera mais curtida.

## O que isto é (e o que não é)

- É uma **simulação didática** de pouco mais de 100 linhas, com comentários. O algoritmo de verdade das redes usa milhares de sinais e não é público.
- A regra central é a que as próprias plataformas descrevem: o chefe do Instagram, Adam Mosseri, disse em jan/2025 que os sinais que mais pesam são **tempo assistido**, **curtidas** e **envios** ([Social Media Today](https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/)).
- **Bolha no feed não é o mesmo que mudar a opinião.** Num estudo publicado na *Science* em 2023, milhares de pessoas usaram o feed cronológico no lugar do algoritmo durante 3 meses da eleição dos EUA: mudou o que elas viram, mas a polarização e as atitudes políticas quase não mudaram ([Guess et al., 2023](https://doi.org/10.1126/science.abp9364)). O algoritmo escolhe o que você vê… e aí parece que todo mundo pensa igual a você.

## Como o código está organizado

| peça | o que faz |
|---|---|
| `Experimento` | os parâmetros (dias, posts, reforço, gosto), validados na criação |
| `feed_de(universo)` | simula um universo e devolve o feed do último dia |
| `rodar(universos)` | roda vários universos e conta em quantos o feed travou |
| `test_feed.py` | 11 testes, incluindo os números exatos do vídeo |

Cada universo usa o próprio gerador de números aleatórios (`random.Random(universo)`), então o resultado não depende da ordem em que as coisas rodam.

No vídeo aparece uma versão mais curta do mesmo código (mesma lógica, mesmos números), pra caber na tela.

## Licença

MIT. Pode usar, copiar e mudar à vontade. Se fizer um experimento diferente, me marca que eu quero ver;)

---
// feito pelo Garoto do Programa; · código aberto, humor duvidoso;)
