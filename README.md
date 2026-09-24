# Transformações 2D — Quadrilátero

Aplicação gráfica desenvolvida em Python para demonstrar **rasterização e transformações geométricas 2D** aplicadas a um quadrilátero.

O projeto permite criar uma figura diretamente em uma interface gráfica, visualizar seu preenchimento e suas arestas e aplicar transformações de **escala, rotação e translação**, utilizando diferentes pontos de referência (pivôs).

## Funcionalidades

* Criação de um quadrilátero através de quatro cliques no canvas.
* Visualização dos pontos `P1`, `P2`, `P3` e `P4`.
* Preenchimento do quadrilátero utilizando o algoritmo **Scanline**.
* Rasterização das arestas utilizando uma implementação baseada no **algoritmo de Bresenham**.
* Visualização do ponto de pivot utilizado nas transformações.
* Aplicação de:

  * **Escala**
  * **Rotação**
  * **Translação**
* Escolha do pivot entre:

  * P1
  * P2
  * P3
  * P4
  * Centro do quadrilátero
  * Origem `(0, 0)`
* Restauração da figura original.
* Criação de um novo quadrilátero.
* Salvamento da imagem atual em PNG.
* Salvamento das imagens antes e depois das transformações.

## Tecnologias utilizadas

* **Python 3**
* **Tkinter** — criação da interface gráfica.
* **Pillow (PIL)** — criação e manipulação das imagens.
* **Math** — cálculos matemáticos utilizados nas transformações e rasterização.

## Estrutura do projeto

```text
.
├── main.py
├── configuracoes.py
├── algoritmos.py
├── interface.py
└── README.md
```

### `main.py`

É o ponto de entrada da aplicação.

Responsável por:

1. Criar a janela principal do Tkinter.
2. Instanciar a classe `Aplicacao`.
3. Iniciar o loop de eventos da interface.

```python
def main():
    janela = tk.Tk()

    Aplicacao(janela)

    janela.mainloop()
```

### `configuracoes.py`

Centraliza as principais configurações visuais e dimensionais da aplicação.

```python
LARGURA = 600
ALTURA = 600

FUNDO = (255, 255, 255)
COR_PREENCHIMENTO = (120, 190, 255)
COR_ARESTA = (0, 0, 0)
COR_PIVOT = (255, 0, 0)
```

As configurações incluem:

| Configuração        | Descrição                              |
| ------------------- | -------------------------------------- |
| `LARGURA`           | Largura do canvas                      |
| `ALTURA`            | Altura do canvas                       |
| `FUNDO`             | Cor de fundo                           |
| `COR_PREENCHIMENTO` | Cor utilizada no preenchimento         |
| `COR_ARESTA`        | Cor das arestas                        |
| `COR_PIVOT`         | Cor utilizada para representar o pivot |

### `algoritmos.py`

Contém a parte matemática e computacional do projeto.

Entre as principais funções estão:

#### Manipulação da matriz

* `criar_matriz()`
* `ponto_valido()`
* `marcar_pixel()`
* `marcar_pivot()`

A figura é inicialmente representada por uma matriz de pixels.

#### Rasterização

* `inc_linha()`
* `pontos_para_pixels()`
* `desenhar_quadrilatero()`

A função `inc_linha()` implementa a rasterização das linhas utilizando uma abordagem baseada no algoritmo de **Bresenham**.

#### Preenchimento

* `preencher_scanline()`

Utiliza o algoritmo **Scanline** para determinar quais pixels devem ser preenchidos no interior do quadrilátero.

#### Pivot

* `calcular_centro()`
* `obter_pivot()`

Permitem determinar o ponto utilizado como referência para escala e rotação.

#### Transformações geométricas

* `aplicar_escala()`
* `aplicar_rotacao()`
* `aplicar_translacao()`

Essas funções recebem os pontos atuais do quadrilátero e retornam suas novas posições após a transformação.

#### Conversão para imagem

* `matriz_para_imagem()`

Converte a matriz de pixels para uma imagem RGB utilizando o Pillow.

### `interface.py`

Implementa toda a interface gráfica e integra os algoritmos com o usuário.

A classe principal é:

```python
class Aplicacao:
```

Ela é responsável por:

* Criar o canvas;
* Criar o painel de controles;
* Receber os cliques do usuário;
* Exibir os pontos;
* Aplicar as transformações;
* Atualizar a representação gráfica;
* Validar entradas;
* Restaurar a figura;
* Salvar imagens.

## Como executar

### 1. Pré-requisitos

É necessário ter o **Python 3** instalado.

Também é necessário instalar a biblioteca Pillow:

```bash
pip install Pillow
```

> O Tkinter normalmente já acompanha instalações padrão do Python. Em algumas distribuições Linux, pode ser necessário instalar o pacote `python3-tk` separadamente.

### 2. Clonar ou baixar o projeto

Após obter os arquivos do projeto, entre no diretório:

```bash
cd nome-do-projeto
```

### 3. Executar

Execute:

```bash
python main.py
```

Em alguns sistemas, pode ser necessário utilizar:

```bash
python3 main.py
```

## Como utilizar

### 1. Criar um quadrilátero

Ao iniciar o programa, clique **quatro vezes no canvas**.

Cada clique representa um ponto:

```text
P1 → primeiro clique
P2 → segundo clique
P3 → terceiro clique
P4 → quarto clique
```

Após o quarto clique, o quadrilátero será preenchido e suas arestas serão desenhadas.

### 2. Escolher o pivot

No painel **Pivot**, selecione o ponto que será utilizado como referência.

As opções disponíveis são:

* `P1`
* `P2`
* `P3`
* `P4`
* `Centro`
* `Origem`

O pivot é representado visualmente por uma marcação vermelha.

### 3. Aplicar escala

Informe os fatores de escala nos campos:

```text
Escala X
Escala Y
```

Por exemplo:

```text
SX = 2
SY = 2
```

duplica as dimensões da figura em relação ao pivot selecionado.

Valores menores que `1` reduzem a figura.

### 4. Aplicar rotação

Informe o ângulo em graus.

Por exemplo:

```text
90
```

aplica uma rotação de 90 graus em relação ao pivot selecionado.

Ângulos positivos seguem a convenção utilizada pela transformação matemática implementada no projeto.

### 5. Aplicar translação

Informe os deslocamentos:

```text
X
Y
```

Por exemplo:

```text
X = 50
Y = 30
```

desloca todos os pontos do quadrilátero em `(50, 30)`.

A translação não depende do pivot selecionado.

### 6. Restaurar a figura

O botão **Restaurar original** retorna o quadrilátero para as posições definidas inicialmente, descartando as transformações aplicadas desde sua criação.

### 7. Criar um novo quadrilátero

O botão **Novo quadrilátero** limpa o canvas e restaura os valores padrão dos controles.

Depois disso, é possível inserir quatro novos pontos.

## Sistema de coordenadas

A aplicação utiliza o sistema de coordenadas do canvas do Tkinter:

```text
(0,0) ───────────────→ X
  |
  |
  |
  ↓
  Y
```

Assim:

* `X` aumenta para a direita;
* `Y` aumenta para baixo;
* A origem está localizada no canto superior esquerdo do canvas.

A origem `(0, 0)` também pode ser selecionada como pivot.

## Transformações matemáticas

### Escala

Para um ponto `(x, y)` em relação ao pivot `(px, py)`:

```text
x' = px + (x - px) × sx
y' = py + (y - py) × sy
```

### Rotação

Para um ângulo `θ`:

```text
x' = (x - px) × cos(θ) - (y - py) × sin(θ) + px

y' = (x - px) × sin(θ) + (y - py) × cos(θ) + py
```

O ângulo informado em graus é convertido para radianos antes dos cálculos.

### Translação

Para os deslocamentos `tx` e `ty`:

```text
x' = x + tx
y' = y + ty
```

## Rasterização

O projeto trabalha diretamente com uma **matriz de pixels**, em vez de depender exclusivamente dos recursos de desenho geométrico do Tkinter.

### Arestas

As arestas são convertidas em pixels pela função `inc_linha()`, utilizando uma implementação baseada no algoritmo de Bresenham.

Isso permite determinar quais pixels devem ser marcados para representar uma linha entre dois pontos.

### Preenchimento Scanline

O preenchimento utiliza a técnica Scanline:

1. Percorre as linhas horizontais que atravessam o quadrilátero.
2. Calcula as interseções da linha atual com as arestas.
3. Ordena as interseções.
4. Preenche os pixels existentes entre os pares de interseções.

Esse processo é repetido para as linhas que atravessam a área da figura.

## Salvamento de imagens

A aplicação possui duas opções de salvamento.

### Salvar imagem atual

O botão **Salvar imagem atual** permite escolher o local e o nome do arquivo PNG.

### Salvar antes e depois

O botão **Salvar antes e depois** gera automaticamente:

```text
quadrado_antes.png
quadrado_depois.png
```

A primeira imagem representa o quadrilátero original e a segunda representa seu estado atual.

## Organização da arquitetura

O projeto possui uma separação simples entre interface, configurações e lógica:

```text
                 ┌──────────────┐
                 │   main.py    │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ interface.py │
                 └──────┬───────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
      ┌───────────────┐   ┌────────────────┐
      │ configuracoes │   │  algoritmos.py │
      │     .py       │   │                │
      └───────────────┘   └───────┬────────┘
                                  │
                                  ▼
                           ┌─────────────┐
                           │ Pillow (PIL)│
                           └─────────────┘
```

Essa organização permite manter:

* **Inicialização** em `main.py`;
* **Configurações** em `configuracoes.py`;
* **Algoritmos matemáticos e gráficos** em `algoritmos.py`;
* **Interface e interação com o usuário** em `interface.py`.

## Dependências

O projeto possui uma dependência externa principal:

```text
Pillow
```

A biblioteca `tkinter` é utilizada para a interface gráfica e faz parte da distribuição padrão do Python em muitas instalações.


## Integrantes

- [Caio Felix](https://github.com/Caio-Felix1)
- [Vinicius Santos](https://github.com/vynnyss)
- [Gabriel Vicente](https://github.com/Gabriel-Aiala)
- [Diego Fonseca](https://github.com/Diegopkg100)
