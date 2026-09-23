import tkinter as tk

from interface import Aplicacao


def main():

    janela = tk.Tk()

    Aplicacao(janela)

    janela.mainloop()


if __name__ == "__main__":
    main()