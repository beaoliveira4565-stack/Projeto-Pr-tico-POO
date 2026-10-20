import os

class Curso:
    def __init__(self, codigo: str, nome: str, modalidade: str):
        self._codigo = codigo
        self._nome = nome
        self._modalidade = modalidade

    @property
    def codigo(self):
        return self._codigo

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def modalidade(self):
        return self._modalidade

    @modalidade.setter
    def modalidade(self, valor):
        self._modalidade = valor

    def __str__(self):
        return f"{self._codigo};{self._nome};{self._modalidade}"


class GerenciadorCursos:
    def __init__(self, arquivo="cursos.txt"):
        self.arquivo = arquivo
        self.cursos = []
        self.carregar_dados()

    def carregar_dados(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                self.cursos = [Curso(*linha.strip().split(";")) for linha in f if linha.strip() and len(linha.strip().split(";")) == 3]

    def salvar_dados(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            f.writelines(f"{curso}\n" for curso in self.cursos)

    def cadastrar(self, codigo, nome, modalidade):
        if self.pesquisar_por_codigo(codigo):
            return False, "Erro: Já existe um curso com este código."
        self.cursos.append(Curso(codigo, nome, modalidade))
        self.salvar_dados()
        return True, "Curso cadastrado com sucesso!"

    def listar(self):
        return self.cursos

    def pesquisar_por_codigo(self, codigo):
        return next((c for c in self.cursos if c.codigo == codigo), None)

    def alterar(self, codigo, novo_nome=None, nova_modalidade=None):
        curso = self.pesquisar_por_codigo(codigo)
        if not curso:
            return False, "Curso não encontrado."
        if novo_nome:
            curso.nome = novo_nome
        if nova_modalidade:
            curso.modalidade = nova_modalidade
        self.salvar_dados()
        return True, "Curso alterado com sucesso!"

    def excluir(self, codigo):
        curso = self.pesquisar_por_codigo(codigo)
        if not curso:
            return False, "Curso não encontrado."
        self.cursos.remove(curso)
        self.salvar_dados()
        return True, "Curso excluído com sucesso!"