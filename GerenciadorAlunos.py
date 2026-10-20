
from Aluno import Aluno
import os


class GerenciadorAlunos:

    def __init__(self):
        self.alunos = []
        self.arquivo = "alunos.txt"
        self.carregar()

    # CARREGAR ALUNOS DO ARQUIVO TXT
    def carregar(self):
        self.alunos.clear()

        if not os.path.exists(self.arquivo):
            open(self.arquivo, "a", encoding="utf-8").close()
            return

        with open(self.arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")

                if len(dados) == 5:
                    aluno = Aluno(
                        dados[0],
                        dados[1],
                        dados[2],
                        dados[3],
                        dados[4]
                    )

                    self.alunos.append(aluno)

    # SALVAR ALUNOS NO ARQUIVO TXT
    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            for aluno in self.alunos:
                arquivo.write(aluno.para_txt() + "\n")

    # CADASTRAR ALUNO
    def cadastrar(self, aluno):
        if self.pesquisar(aluno.Matricula):
            print("Matrícula já cadastrada!")
            return False

        self.alunos.append(aluno)
        self.salvar()

        print("Aluno cadastrado com sucesso!")
        return True

    # LISTAR TODOS OS ALUNOS
    def listar(self):
        if not self.alunos:
            print("Nenhum aluno cadastrado!")
            return

        for aluno in self.alunos:
            print(aluno)

    # PESQUISAR ALUNO PELA MATRÍCULA
    def pesquisar(self, matricula):
        for aluno in self.alunos:
            if aluno.Matricula == matricula:
                return aluno

        return None

    # PESQUISAR ALUNO PELO NOME
    def pesquisar_nome(self, nome):
        encontrados = []

        for aluno in self.alunos:
            if nome.lower() in aluno.Nome.lower():
                encontrados.append(aluno)

        return encontrados

    # ALTERAR DADOS DO ALUNO
    def alterar(self, matricula, novo_nome,
                novo_cpf, novo_email, novo_codigo_curso):

        aluno = self.pesquisar(matricula)

        if aluno is None:
            print("Aluno não encontrado!")
            return False

        aluno.Nome = novo_nome
        aluno.CPF = novo_cpf
        aluno.Email = novo_email
        aluno.Codigo_curso = novo_codigo_curso

        self.salvar()

        print("Aluno atualizado com sucesso!")
        return True

    # EXCLUIR ALUNO
    def excluir(self, matricula):
        aluno = self.pesquisar(matricula)

        if aluno is None:
            print("Aluno não encontrado!")
            return False

        self.alunos.remove(aluno)
        self.salvar()

        print("Aluno excluído com sucesso!")
        return True

