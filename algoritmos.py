import math
from PIL import Image

from configuracoes import (
    LARGURA,
    ALTURA,
    FUNDO
)


# ==============================
# MATRIZ
# ==============================

def criar_matriz(largura=LARGURA, altura=ALTURA, fundo=FUNDO):
    return [
        [fundo for _ in range(altura)]
        for _ in range(largura)
    ]


def ponto_valido(x, y, largura=LARGURA, altura=ALTURA):
    return 0 <= x < largura and 0 <= y < altura


def marcar_pixel(matriz, x, y, simbolo):
    largura = len(matriz)
    altura = len(matriz[0]) if largura > 0 else 0

    if ponto_valido(x, y, largura, altura):
        matriz[x][y] = simbolo


def marcar_pivot(matriz, pivot, simbolo):
    px = round(pivot[0])
    py = round(pivot[1])

    for deslocamento in range(-2, 3):
        marcar_pixel(matriz, px + deslocamento, py, simbolo)
        marcar_pixel(matriz, px, py + deslocamento, simbolo)


# ==============================
# RASTERIZAÇÃO
# ==============================

def inc_linha(x1, y1, x2, y2, matriz, simbolo):
    """
    Rasteriza uma reta usando o algoritmo do ponto médio
    / Bresenham.
    """

    if x1 > x2 or (x1 == x2 and y1 > y2):
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    distancia_y = y2 - y1
    distancia_x = x2 - x1

    if distancia_x == 0 and distancia_y == 0:
        marcar_pixel(matriz, x1, y1, simbolo)

    elif distancia_y == 0:
        for x in range(x1, x2 + 1):
            marcar_pixel(matriz, x, y1, simbolo)

    elif distancia_x == 0:
        for y in range(y1, y2 + 1):
            marcar_pixel(matriz, x1, y, simbolo)

    else:
        x = x1
        y = y1

        marcar_pixel(matriz, x, y, simbolo)

        passo_y = 1 if y1 < y2 else -1

        if abs(distancia_y) > abs(distancia_x):
            decisao = 2 * abs(distancia_x) - abs(distancia_y)
            incremento_e = 2 * abs(distancia_x)
            incremento_ne = 2 * (abs(distancia_x) - abs(distancia_y))

            contador = 0

            while contador < abs(distancia_y):
                if decisao <= 0:
                    decisao += incremento_e
                    y += passo_y
                else:
                    decisao += incremento_ne
                    x += 1
                    y += passo_y

                marcar_pixel(matriz, x, y, simbolo)
                contador += 1

        else:
            decisao = 2 * abs(distancia_y) - abs(distancia_x)
            incremento_e = 2 * abs(distancia_y)
            incremento_ne = 2 * (abs(distancia_y) - abs(distancia_x))

            contador = 0

            while contador < abs(distancia_x):
                if decisao <= 0:
                    decisao += incremento_e
                    x += 1
                else:
                    decisao += incremento_ne
                    x += 1
                    y += passo_y

                marcar_pixel(matriz, x, y, simbolo)
                contador += 1


def pontos_para_pixels(pontos):
    return [
        (round(x), round(y))
        for x, y in pontos
    ]


def desenhar_quadrilatero(matriz, pontos, simbolo):
    pontos_em_pixels = pontos_para_pixels(pontos)

    for indice in range(4):
        x1, y1 = pontos_em_pixels[indice]
        x2, y2 = pontos_em_pixels[(indice + 1) % 4]

        inc_linha(
            x1,
            y1,
            x2,
            y2,
            matriz,
            simbolo
        )


# ==============================
# PREENCHIMENTO
# ==============================

def preencher_scanline(matriz, pontos, simbolo):
    largura = len(matriz)
    altura = len(matriz[0]) if largura > 0 else 0

    if largura == 0 or altura == 0:
        return

    menor_y = min(y for _, y in pontos)
    maior_y = max(y for _, y in pontos)

    inicio_y = max(0, math.ceil(menor_y))
    fim_y = min(altura, math.ceil(maior_y))

    for y in range(inicio_y, fim_y):
        intersecoes = []

        for indice in range(4):
            x1, y1 = pontos[indice]
            x2, y2 = pontos[(indice + 1) % 4]

            if y1 == y2:
                continue

            y_min = min(y1, y2)
            y_max = max(y1, y2)

            if y_min <= y < y_max:
                x = (
                    x1
                    + (y - y1)
                    * (x2 - x1)
                    / (y2 - y1)
                )

                intersecoes.append(x)

        intersecoes.sort()

        inicio_x = None

        for indice in range(len(intersecoes)):
            if indice % 2 == 0:
                inicio_x = max(
                    0,
                    math.ceil(intersecoes[indice])
                )
            else:
                fim_x = min(
                    largura - 1,
                    math.floor(intersecoes[indice])
                )

                for x in range(inicio_x, fim_x + 1):
                    matriz[x][y] = simbolo


# ==============================
# PIVOT
# ==============================

def calcular_centro(pontos):
    centro_x = sum(x for x, _ in pontos) / 4
    centro_y = sum(y for _, y in pontos) / 4

    return centro_x, centro_y


def obter_pivot(pontos, opcao):
    if 1 <= opcao <= 4:
        return pontos[opcao - 1]

    if opcao == 5:
        return calcular_centro(pontos)

    if opcao == 6:
        return 0,0

    raise ValueError("Pivot inválido.")


# ==============================
# TRANSFORMAÇÕES
# ==============================

def aplicar_escala(pontos, sx, sy, pivot):
    px, py = pivot

    pontos_escalados = []

    for x, y in pontos:
        novo_x = px + (x - px) * sx
        novo_y = py + (y - py) * sy

        pontos_escalados.append(
            (novo_x, novo_y)
        )

    return pontos_escalados


def aplicar_rotacao(pontos, angulo_graus, pivot):
    px, py = pivot

    angulo = math.radians(angulo_graus)

    cosseno = math.cos(angulo)
    seno = math.sin(angulo)

    pontos_rotacionados = []

    for x, y in pontos:
        x_transladado = x - px
        y_transladado = y - py

        novo_x = (
            x_transladado * cosseno
            - y_transladado * seno
            + px
        )

        novo_y = (
            x_transladado * seno
            + y_transladado * cosseno
            + py
        )

        pontos_rotacionados.append(
            (novo_x, novo_y)
        )

    return pontos_rotacionados


def aplicar_translacao(pontos, deslocamento_x, deslocamento_y):
    pontos_transladados = []

    for x, y in pontos:
        novo_x = x + deslocamento_x
        novo_y = y + deslocamento_y

        pontos_transladados.append(
            (novo_x, novo_y)
        )

    return pontos_transladados


# ==============================
# MATRIZ -> IMAGEM
# ==============================

def matriz_para_imagem(matriz):
    largura = len(matriz)

    altura = (
        len(matriz[0])
        if largura > 0
        else 0
    )

    imagem = Image.new(
        "RGB",
        (largura, altura),
        FUNDO
    )

    for x in range(largura):
        for y in range(altura):
            imagem.putpixel(
                (x, y),
                matriz[x][y]
            )

    return imagem
