"""Integração: junta os módulos de ALFA e BETA e gera o relatório completo."""
from alfa.aluno import GerenciadorAlunos
from alfa.curso import GerenciadorCursos
from beta.professor import GerenciadorProfessores
from beta.disciplina import GerenciadorDisciplinas


class Sistema:
    def __init__(self, pasta="dados"):
        self.cursos = GerenciadorCursos(pasta)
        self.professores = GerenciadorProfessores(pasta)
        self.alunos = GerenciadorAlunos(pasta, self.cursos)
        self.disciplinas = GerenciadorDisciplinas(pasta, self.cursos, self.professores)
        # Integridade referencial na exclusão
        self.cursos.dependentes = [(self.alunos, "codigo_curso", "aluno(s)"),
                                   (self.disciplinas, "codigo_curso", "disciplina(s)")]
        self.professores.dependentes = [(self.disciplinas, "codigo_professor", "disciplina(s)")]

    def relatorio(self):
        """Retorna as linhas: 'O Aluno X está matriculado no curso Y, ...'."""
        linhas = []
        for aluno in self.alunos.listar():
            curso = self.cursos.buscar_por_codigo(aluno.codigo_curso)
            nome_curso = curso.nome if curso else "(curso não encontrado)"
            discs = [d for d in self.disciplinas.listar()
                     if d.codigo_curso == aluno.codigo_curso]
            if not discs:
                linhas.append(f"O Aluno {aluno.nome} está matriculado no curso "
                              f"{nome_curso}, que ainda não possui disciplinas.")
            for d in discs:
                prof = self.professores.buscar_por_codigo(d.codigo_professor)
                nome_prof = prof.nome if prof else "(professor não encontrado)"
                linhas.append(f"O Aluno {aluno.nome} está matriculado no curso "
                              f"{nome_curso}, assistindo a disciplina {d.nome} "
                              f"com o professor {nome_prof}.")
        return linhas
