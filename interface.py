import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from PIL import ImageTk

from configuracoes import (
    LARGURA,
    ALTURA,
    COR_PREENCHIMENTO,
    COR_ARESTA,
    COR_PIVOT
)

from algoritmos import (
    criar_matriz,
    preencher_scanline,
    desenhar_quadrilatero,
    marcar_pivot,
    obter_pivot,
    aplicar_escala,
    aplicar_rotacao,
    aplicar_translacao,
    matriz_para_imagem
)


# ==============================
# INTERFACE
# ==============================

class Aplicacao:

    def __init__(self, janela):

        self.janela = janela

        self.janela.title(
            "Transformações 2D - Quadrilátero"
        )

        self.janela.resizable(
            True,
            True
        )

        # --------------------------------
        # Estado da aplicação
        # --------------------------------

        self.pontos_originais = []

        self.pontos_atuais = []

        self.pivot_opcao = 5

        self.matriz_atual = None

        self.imagem_tk = None

        # --------------------------------
        # Layout principal
        # --------------------------------

        frame_principal = ttk.Frame(
            janela,
            padding=10
        )

        frame_principal.pack(
            fill="both",
            expand=True
        )

        # --------------------------------
        # Canvas principal
        # --------------------------------

        self.canvas = tk.Canvas(
            frame_principal,
            width=LARGURA,
            height=ALTURA,
            bg="white",
            highlightthickness=1,
            highlightbackground="black"
        )

        self.canvas.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(0, 10),
            sticky="nw"
        )

        self.canvas.bind(
            "<Button-1>",
            self.clicar_canvas
        )

        # --------------------------------
        # Painel lateral com rolagem
        # --------------------------------

        container_painel = ttk.Frame(
            frame_principal
        )

        container_painel.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        canvas_painel = tk.Canvas(
            container_painel,
            width=250,
            height=580,
            highlightthickness=0
        )

        canvas_painel.pack(
            side="left",
            fill="y"
        )

        barra_rolagem = ttk.Scrollbar(
            container_painel,
            orient="vertical",
            command=canvas_painel.yview
        )

        barra_rolagem.pack(
            side="right",
            fill="y"
        )

        canvas_painel.configure(
            yscrollcommand=barra_rolagem.set
        )

        painel = ttk.Frame(
            canvas_painel
        )

        canvas_painel.create_window(
            (0, 0),
            window=painel,
            anchor="nw",
            width=250
        )

        # Atualiza a área disponível para rolagem
        def atualizar_area_rolagem(event=None):

            canvas_painel.configure(
                scrollregion=canvas_painel.bbox(
                    "all"
                )
            )

        painel.bind(
            "<Configure>",
            atualizar_area_rolagem
        )

        # --------------------------------
        # Rolagem com roda do mouse
        # --------------------------------

        def rolar_painel(event):

            canvas_painel.yview_scroll(
                int(
                    -1 * (event.delta / 120)
                ),
                "units"
            )

        canvas_painel.bind(
            "<MouseWheel>",
            rolar_painel
        )

        # Linux
        canvas_painel.bind(
            "<Button-4>",
            lambda event:
            canvas_painel.yview_scroll(
                -1,
                "units"
            )
        )

        canvas_painel.bind(
            "<Button-5>",
            lambda event:
            canvas_painel.yview_scroll(
                1,
                "units"
            )
        )

        # --------------------------------
        # Pontos
        # --------------------------------

        grupo_pontos = ttk.LabelFrame(
            painel,
            text="Pontos"
        )

        grupo_pontos.pack(
            fill="x",
            pady=(0, 10)
        )

        self.labels_pontos = []

        for i in range(4):

            label = ttk.Label(
                grupo_pontos,
                text=f"P{i + 1}: -"
            )

            label.pack(
                anchor="w",
                padx=10,
                pady=2
            )

            self.labels_pontos.append(
                label
            )

        ttk.Label(
            grupo_pontos,
            text="Clique 4 vezes na área\n"
                 "para criar o quadrilátero."
        ).pack(
            padx=10,
            pady=8
        )

        # --------------------------------
        # Novo quadrilátero
        # --------------------------------

        ttk.Button(
            grupo_pontos,
            text="Novo quadrilátero",
            command=self.limpar
        ).pack(
            fill="x",
            padx=10,
            pady=(0, 8)
        )

        # --------------------------------
        # Pivot
        # --------------------------------

        grupo_pivot = ttk.LabelFrame(
            painel,
            text="Pivot"
        )

        grupo_pivot.pack(
            fill="x",
            pady=(0, 10)
        )

        self.pivot_var = tk.IntVar(
            value=5
        )

        opcoes_pivot = [
            ("P1", 1),
            ("P2", 2),
            ("P3", 3),
            ("P4", 4),
            ("Centro", 5),
            ("Origem", 6)
        ]

        for texto, valor in opcoes_pivot:

            ttk.Radiobutton(
                grupo_pivot,
                text=texto,
                variable=self.pivot_var,
                value=valor,
                command=self.atualizar_desenho
            ).pack(
                anchor="w",
                padx=10,
                pady=2
            )

        # --------------------------------
        # Escala
        # --------------------------------

        grupo_escala = ttk.LabelFrame(
            painel,
            text="Escala"
        )

        grupo_escala.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            grupo_escala,
            text="Escala X:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.entrada_sx = ttk.Entry(
            grupo_escala,
            width=10
        )

        self.entrada_sx.insert(
            0,
            "1.0"
        )

        self.entrada_sx.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            grupo_escala,
            text="Escala Y:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.entrada_sy = ttk.Entry(
            grupo_escala,
            width=10
        )

        self.entrada_sy.insert(
            0,
            "1.0"
        )

        self.entrada_sy.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Button(
            grupo_escala,
            text="Aplicar escala",
            command=self.aplicar_escala_interface
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=5
        )

        # --------------------------------
        # Rotação
        # --------------------------------

        grupo_rotacao = ttk.LabelFrame(
            painel,
            text="Rotação"
        )

        grupo_rotacao.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            grupo_rotacao,
            text="Ângulo:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.entrada_angulo = ttk.Entry(
            grupo_rotacao,
            width=10
        )

        self.entrada_angulo.insert(
            0,
            "0"
        )

        self.entrada_angulo.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Button(
            grupo_rotacao,
            text="Aplicar rotação",
            command=self.aplicar_rotacao_interface
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            pady=5
        )

        # --------------------------------
        # Translação
        # --------------------------------

        grupo_translacao = ttk.LabelFrame(
            painel,
            text="Translação"
        )

        grupo_translacao.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            grupo_translacao,
            text="X:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.entrada_tx = ttk.Entry(
            grupo_translacao,
            width=10
        )

        self.entrada_tx.insert(
            0,
            "0"
        )

        self.entrada_tx.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            grupo_translacao,
            text="Y:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.entrada_ty = ttk.Entry(
            grupo_translacao,
            width=10
        )

        self.entrada_ty.insert(
            0,
            "0"
        )

        self.entrada_ty.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Button(
            grupo_translacao,
            text="Aplicar translação",
            command=self.aplicar_translacao_interface
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=5
        )

        # --------------------------------
        # Botões gerais
        # --------------------------------

        ttk.Button(
            painel,
            text="Restaurar original",
            command=self.restaurar_original
        ).pack(
            fill="x",
            pady=3
        )

        ttk.Button(
            painel,
            text="Salvar imagem atual",
            command=self.salvar_atual
        ).pack(
            fill="x",
            pady=3
        )

        ttk.Button(
            painel,
            text="Salvar antes e depois",
            command=self.salvar_antes_depois
        ).pack(
            fill="x",
            pady=3
        )

        # --------------------------------
        # Status
        # --------------------------------

        self.status = ttk.Label(
            frame_principal,
            text="Clique na tela para inserir P1."
        )

        self.status.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(10, 0)
        )

    # ==============================
    # CLIQUE NO CANVAS
    # ==============================

    def clicar_canvas(self, evento):

        if len(
            self.pontos_originais
        ) >= 4:

            return

        ponto = (
            evento.x,
            evento.y
        )

        self.pontos_originais.append(
            ponto
        )

        self.pontos_atuais = (
            self.pontos_originais.copy()
        )

        self.atualizar_labels()

        self.atualizar_desenho()

        quantidade = len(
            self.pontos_originais
        )

        if quantidade < 4:

            self.status.config(
                text=(
                    f"Clique para inserir "
                    f"P{quantidade + 1}."
                )
            )

        else:

            self.status.config(
                text=(
                    "Quadrilátero criado. "
                    "Escolha uma transformação."
                )
            )

    # ==============================
    # DESENHAR LABELS DOS PONTOS
    # ==============================

    def desenhar_labels_pontos(self):

        """
        Desenha os nomes P1, P2, P3 e P4 próximos
        aos respectivos pontos.

        Quando os pontos estão sobrepostos, os nomes
        são distribuídos ao redor do pixel para evitar
        que os textos fiquem uns sobre os outros.
        """

        deslocamentos = [
            (8, -8),     # P1 - superior direito
            (-8, -8),    # P2 - superior esquerdo
            (8, 8),      # P3 - inferior direito
            (-8, 8)      # P4 - inferior esquerdo
        ]

        anchors = [
            "sw",        # P1
            "se",        # P2
            "nw",        # P3
            "ne"         # P4
        ]

        for i, ponto in enumerate(self.pontos_atuais):

            x, y = ponto

            deslocamento_x, deslocamento_y = deslocamentos[i]

            self.canvas.create_text(
                x + deslocamento_x,
                y + deslocamento_y,
                text=f"P{i + 1}",
                fill="black",
                anchor=anchors[i]
            )

    # ==============================
    # ATUALIZAR LABELS
    # ==============================

    def atualizar_labels(self):

        for i in range(4):

            if i < len(
                self.pontos_atuais
            ):

                x, y = (
                    self.pontos_atuais[i]
                )

                self.labels_pontos[i].config(
                    text=(
                        f"P{i + 1}: "
                        f"({x:.1f}, {y:.1f})"
                    )
                )

            else:

                self.labels_pontos[i].config(
                    text=f"P{i + 1}: -"
                )

    # ==============================
    # DESENHO
    # ==============================

    def atualizar_desenho(self):

        self.canvas.delete(
            "all"
        )

        # --------------------------------
        # Ainda definindo os pontos
        # --------------------------------

        if len(
            self.pontos_atuais
        ) < 4:

            for ponto in self.pontos_originais:

                x, y = ponto

                raio = 4

                self.canvas.create_oval(
                    x - raio,
                    y - raio,
                    x + raio,
                    y + raio,
                    fill="black"
                )

            self.desenhar_labels_pontos()

            self.atualizar_labels()

            return

        # --------------------------------
        # Obtém pivot
        # --------------------------------

        pivot = obter_pivot(
            self.pontos_atuais,
            self.pivot_var.get()
        )

        # --------------------------------
        # Cria matriz
        # --------------------------------

        matriz = criar_matriz()

        # --------------------------------
        # Preenchimento
        # --------------------------------

        preencher_scanline(
            matriz,
            self.pontos_atuais,
            COR_PREENCHIMENTO
        )

        # --------------------------------
        # Arestas
        # --------------------------------

        desenhar_quadrilatero(
            matriz,
            self.pontos_atuais,
            COR_ARESTA
        )

        # --------------------------------
        # Pivot
        # --------------------------------

        marcar_pivot(
            matriz,
            pivot,
            COR_PIVOT
        )

        self.matriz_atual = matriz

        # --------------------------------
        # Matriz -> imagem
        # --------------------------------

        imagem = matriz_para_imagem(
            matriz
        )

        self.imagem_tk = ImageTk.PhotoImage(
            imagem
        )

        self.canvas.create_image(
            0,
            0,
            image=self.imagem_tk,
            anchor="nw"
        )

        # --------------------------------
        # Nomes dos pontos
        # --------------------------------

        self.desenhar_labels_pontos()

        self.atualizar_labels()

    # ==============================
    # VALIDAÇÃO
    # ==============================

    def verificar_quadrilatero(self):

        if len(
            self.pontos_atuais
        ) != 4:

            messagebox.showwarning(
                "Atenção",
                "Defina os quatro pontos primeiro."
            )

            return False

        return True

    # ==============================
    # ESCALA
    # ==============================

    def aplicar_escala_interface(self):

        if not self.verificar_quadrilatero():

            return

        try:

            sx = float(
                self.entrada_sx.get()
            )

            sy = float(
                self.entrada_sy.get()
            )

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Informe valores numéricos "
                "para a escala."
            )

            return

        pivot = obter_pivot(
            self.pontos_atuais,
            self.pivot_var.get()
        )

        self.pontos_atuais = aplicar_escala(
            self.pontos_atuais,
            sx,
            sy,
            pivot
        )

        self.atualizar_desenho()

        self.status.config(
            text=(
                f"Escala aplicada: "
                f"SX={sx}, SY={sy}"
            )
        )

    # ==============================
    # ROTAÇÃO
    # ==============================

    def aplicar_rotacao_interface(self):

        if not self.verificar_quadrilatero():

            return

        try:

            angulo = float(
                self.entrada_angulo.get()
            )

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Informe um ângulo válido."
            )

            return

        pivot = obter_pivot(
            self.pontos_atuais,
            self.pivot_var.get()
        )

        self.pontos_atuais = aplicar_rotacao(
            self.pontos_atuais,
            angulo,
            pivot
        )

        self.atualizar_desenho()

        self.status.config(
            text=(
                f"Rotação aplicada: "
                f"{angulo} graus"
            )
        )

    # ==============================
    # TRANSLAÇÃO
    # ==============================

    def aplicar_translacao_interface(self):

        if not self.verificar_quadrilatero():

            return

        try:

            tx = float(
                self.entrada_tx.get()
            )

            ty = float(
                self.entrada_ty.get()
            )

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Informe valores numéricos "
                "para a translação."
            )

            return

        self.pontos_atuais = aplicar_translacao(
            self.pontos_atuais,
            tx,
            ty
        )

        self.atualizar_desenho()

        self.status.config(
            text=(
                f"Translação aplicada: "
                f"X={tx}, Y={ty}"
            )
        )

    # ==============================
    # RESTAURAR ORIGINAL
    # ==============================

    def restaurar_original(self):

        if len(
            self.pontos_originais
        ) != 4:

            messagebox.showwarning(
                "Atenção",
                "Defina os quatro pontos primeiro."
            )

            return

        self.pontos_atuais = (
            self.pontos_originais.copy()
        )

        self.atualizar_desenho()

        self.status.config(
            text="Figura restaurada."
        )

    # ==============================
    # LIMPAR / NOVO QUADRILÁTERO
    # ==============================

    def limpar(self):

        self.pontos_originais = []

        self.pontos_atuais = []

        self.matriz_atual = None

        self.imagem_tk = None

        self.canvas.delete(
            "all"
        )

        # --------------------------------
        # Restaurar pivot
        # --------------------------------

        self.pivot_var.set(
            5
        )

        # --------------------------------
        # Restaurar escala
        # --------------------------------

        self.entrada_sx.delete(
            0,
            tk.END
        )

        self.entrada_sx.insert(
            0,
            "1.0"
        )

        self.entrada_sy.delete(
            0,
            tk.END
        )

        self.entrada_sy.insert(
            0,
            "1.0"
        )

        # --------------------------------
        # Restaurar rotação
        # --------------------------------

        self.entrada_angulo.delete(
            0,
            tk.END
        )

        self.entrada_angulo.insert(
            0,
            "0"
        )

        # --------------------------------
        # Restaurar translação
        # --------------------------------

        self.entrada_tx.delete(
            0,
            tk.END
        )

        self.entrada_tx.insert(
            0,
            "0"
        )

        self.entrada_ty.delete(
            0,
            tk.END
        )

        self.entrada_ty.insert(
            0,
            "0"
        )

        self.atualizar_labels()

        self.status.config(
            text=(
                "Tela limpa. "
                "Clique na tela para inserir P1."
            )
        )

    # ==============================
    # SALVAR IMAGEM ATUAL
    # ==============================

    def salvar_atual(self):

        if self.matriz_atual is None:

            messagebox.showwarning(
                "Atenção",
                "Não há imagem para salvar."
            )

            return

        caminho = filedialog.asksaveasfilename(
            title="Salvar imagem",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png")
            ]
        )

        if not caminho:

            return

        imagem = matriz_para_imagem(
            self.matriz_atual
        )

        imagem.save(
            caminho
        )

        messagebox.showinfo(
            "Sucesso",
            "Imagem salva com sucesso."
        )

    # ==============================
    # SALVAR ANTES E DEPOIS
    # ==============================

    def salvar_antes_depois(self):

        if len(
            self.pontos_originais
        ) != 4:

            messagebox.showwarning(
                "Atenção",
                "Defina os quatro pontos primeiro."
            )

            return

        # --------------------------------
        # Imagem original
        # --------------------------------

        pivot_original = obter_pivot(
            self.pontos_originais,
            self.pivot_var.get()
        )

        matriz_original = criar_matriz()

        preencher_scanline(
            matriz_original,
            self.pontos_originais,
            COR_PREENCHIMENTO
        )

        desenhar_quadrilatero(
            matriz_original,
            self.pontos_originais,
            COR_ARESTA
        )

        marcar_pivot(
            matriz_original,
            pivot_original,
            COR_PIVOT
        )

        imagem_original = matriz_para_imagem(
            matriz_original
        )

        imagem_original.save(
            "quadrado_antes.png"
        )

        # --------------------------------
        # Imagem atual
        # --------------------------------

        if self.matriz_atual is not None:

            imagem_atual = matriz_para_imagem(
                self.matriz_atual
            )

            imagem_atual.save(
                "quadrado_depois.png"
            )

        messagebox.showinfo(
            "Sucesso",
            "Foram salvas:\n\n"
            "quadrado_antes.png\n"
            "quadrado_depois.png"
        )
