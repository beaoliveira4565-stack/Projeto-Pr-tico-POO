"""DESAFIO: interface gráfica (Tkinter). Iniciada pelo main.py (opção 7 ou --gui)."""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from integracao import Sistema


class CrudFrame(ttk.Frame):
    """Aba genérica de CRUD, montada a partir de CLASSE.CAMPOS do gerenciador."""

    def __init__(self, master, ger):
        super().__init__(master)
        self.ger = ger
        self.campos = ger.CLASSE.CAMPOS
        self.vars = {}

        form = ttk.Frame(self)
        form.pack(fill="x", padx=10, pady=10)
        for i, (attr, rotulo) in enumerate(self.campos):
            ttk.Label(form, text=rotulo).grid(row=i, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            self.vars[attr] = var
            opcoes = ger.CLASSE.OPCOES.get(attr)
            if opcoes:
                w = ttk.Combobox(form, textvariable=var, values=opcoes, state="readonly")
            else:
                w = ttk.Entry(form, textvariable=var, width=40)
            w.grid(row=i, column=1, sticky="we", padx=8)
        form.columnconfigure(1, weight=1)

        botoes = ttk.Frame(self)
        botoes.pack(fill="x", padx=10)
        for texto, cmd in [("Cadastrar", self.cadastrar), ("Alterar", self.alterar),
                           ("Excluir", self.excluir), ("Pesquisar", self.pesquisar),
                           ("Listar tudo", self.atualizar), ("Limpar", self.limpar)]:
            ttk.Button(botoes, text=texto, command=cmd).pack(side="left", padx=3)

        cols = [a for a, _ in self.campos]
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for a, r in self.campos:
            self.tree.heading(a, text=r)
            self.tree.column(a, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar)
        self.atualizar()

    def _tentar(self, funcao, msg_ok=None):
        try:
            funcao()
            if msg_ok:
                messagebox.showinfo("Sucesso", msg_ok)
            self.atualizar()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def _valores(self):
        return [self.vars[a].get() for a, _ in self.campos]

    def cadastrar(self):
        self._tentar(lambda: self.ger.cadastrar(self.ger.CLASSE(*self._valores())),
                     "Cadastrado com sucesso!")

    def alterar(self):
        cod = self.vars[self.campos[0][0]].get()
        novos = {a: self.vars[a].get() for a, _ in self.campos[1:]}
        self._tentar(lambda: self.ger.alterar(cod, **novos), "Alterado com sucesso!")

    def excluir(self):
        cod = self.vars[self.campos[0][0]].get()
        if cod and messagebox.askyesno("Confirmar", f"Excluir '{cod}'?"):
            self._tentar(lambda: self.ger.excluir(cod), "Excluído com sucesso!")

    def pesquisar(self):
        termo = simpledialog.askstring("Pesquisar", "Código ou nome:")
        if termo:
            self._preencher(self.ger.pesquisar(termo))

    def limpar(self):
        for v in self.vars.values():
            v.set("")

    def selecionar(self, _evento=None):
        sel = self.tree.selection()
        if sel:
            for (a, _), valor in zip(self.campos, self.tree.item(sel[0], "values")):
                self.vars[a].set(valor)

    def atualizar(self):
        self._preencher(self.ger.listar())

    def _preencher(self, itens):
        self.tree.delete(*self.tree.get_children())
        for it in itens:
            self.tree.insert("", "end", values=[getattr(it, a) for a, _ in self.campos])


class RelatorioFrame(ttk.Frame):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema
        ttk.Button(self, text="Atualizar relatório", command=self.atualizar).pack(pady=8)
        self.texto = tk.Text(self, wrap="word", state="disabled")
        self.texto.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.atualizar()

    def atualizar(self):
        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("end", "\n\n".join(self.sistema.relatorio()) or "Sem dados.")
        self.texto.config(state="disabled")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão Acadêmica")
        self.geometry("860x560")
        s = Sistema()
        self.abas = ttk.Notebook(self)
        self.abas.pack(fill="both", expand=True)
        for titulo, ger in [("Cursos", s.cursos), ("Professores", s.professores),
                            ("Disciplinas", s.disciplinas), ("Alunos", s.alunos)]:
            self.abas.add(CrudFrame(self.abas, ger), text=titulo)
        self.abas.add(RelatorioFrame(self.abas, s), text="Relatório")
        self.abas.bind("<<NotebookTabChanged>>", self._ao_trocar_aba)

    def _ao_trocar_aba(self, _e):
        aba = self.abas.nametowidget(self.abas.select())
        aba.atualizar()


def iniciar():
    """Abre a janela principal (chamada pelo main.py)."""
    App().mainloop()


if __name__ == "__main__":
    iniciar()
