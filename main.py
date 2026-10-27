"""Ponto de entrada único do sistema (RF16).

    python main.py          -> menu no console
    python main.py --gui    -> interface gráfica (Tkinter)
"""
import sys

from alfa.aluno import Aluno
from alfa.curso import Curso
from beta.professor import Professor
from beta.disciplina import Disciplina
from integracao import Sistema


def ler(rotulo, atual=None):
    """Lê um campo; Enter mantém o valor atual (útil em alterações)."""
    sufixo = f" [{atual}]" if atual is not None else ""
    v = input(f"{rotulo}{sufixo}: ").strip()
    return v if v else atual


def menu_crud(ger, titulo):
    campos = ger.CLASSE.CAMPOS
    while True:
        print(f"\n--- {titulo} ---")
        print("1) Cadastrar  2) Listar  3) Alterar  4) Excluir  5) Pesquisar  0) Voltar")
        op = input("Opção: ").strip()
        try:
            if op == "0":
                return
            elif op == "1":
                valores = [ler(r) or "" for _, r in campos]
                ger.cadastrar(ger.CLASSE(*valores))
                print("Cadastrado com sucesso!")
            elif op == "2":
                itens = ger.listar()
                print(*itens, sep="\n") if itens else print("Nenhum registro.")
            elif op == "3":
                cod = input("Código/Matrícula: ").strip()
                obj = ger.buscar_por_codigo(cod)
                if obj is None:
                    print("Não encontrado.")
                    continue
                novos = {a: ler(r, getattr(obj, a)) for a, r in campos[1:]}
                ger.alterar(cod, **novos)
                print("Alterado com sucesso!")
            elif op == "4":
                ger.excluir(input("Código/Matrícula: ").strip())
                print("Excluído com sucesso!")
            elif op == "5":
                achados = ger.pesquisar(input("Código ou nome: "))
                print(*achados, sep="\n") if achados else print("Nada encontrado.")
            else:
                print("Opção inválida.")
        except ValueError as e:
            print(f"Erro: {e}")


def fluxo_integracao(s):
    """Seção 5 do enunciado: Professor+Curso -> Disciplina -> Aluno -> Relatório."""
    try:
        print("\n== 1) Professor ==")
        s.professores.cadastrar(Professor(*[ler(r) or "" for _, r in Professor.CAMPOS]))
        print("== 1) Curso ==")
        s.cursos.cadastrar(Curso(*[ler(r) or "" for _, r in Curso.CAMPOS]))
        print("== 2) Disciplina (use os códigos acima) ==")
        s.disciplinas.cadastrar(Disciplina(*[ler(r) or "" for _, r in Disciplina.CAMPOS]))
        print("== 3) Aluno (use o código do curso) ==")
        s.alunos.cadastrar(Aluno(*[ler(r) or "" for _, r in Aluno.CAMPOS]))
        print("\n== 4) Relatório completo ==")
        print(*s.relatorio(), sep="\n")
    except ValueError as e:
        print(f"Erro: {e}")


def abrir_gui():
    """Abre a interface gráfica (import tardio: Tkinter só é exigido aqui)."""
    try:
        import interface_grafica
    except ImportError:
        print("Tkinter não está disponível neste Python.")
        return
    try:
        interface_grafica.iniciar()
    except Exception as erro:   # ex.: tkinter.TclError (sem ambiente gráfico)
        print(f"Não foi possível abrir a interface gráfica: {erro}")


def menu_principal(s):
    """Menu de navegação (RF17)."""
    while True:
        print("\n===== SISTEMA DE GESTÃO ACADÊMICA =====")
        print("1) Alunos  2) Cursos  3) Professores  4) Disciplinas")
        print("5) Fluxo de integração  6) Relatório completo")
        print("7) Interface gráfica  0) Sair")
        op = input("Opção: ").strip()
        if op == "1": menu_crud(s.alunos, "ALUNOS")
        elif op == "2": menu_crud(s.cursos, "CURSOS")
        elif op == "3": menu_crud(s.professores, "PROFESSORES")
        elif op == "4": menu_crud(s.disciplinas, "DISCIPLINAS")
        elif op == "5": fluxo_integracao(s)
        elif op == "6": print(*(s.relatorio() or ["Sem dados."]), sep="\n")
        elif op == "7": abrir_gui()
        elif op == "0": return
        else: print("Opção inválida.")


def main():
    if "--gui" in sys.argv:
        abrir_gui()
        return
    s = Sistema()   # RF11: carrega os .txt para a memória
    try:
        menu_principal(s)
    except (KeyboardInterrupt, EOFError):   # Ctrl+C / Ctrl+D / fim da entrada
        print()
    # RF12: cada operação já grava no arquivo; aqui só confirmamos o encerramento
    print("Dados salvos nos arquivos .txt. Encerrando o sistema...")


if __name__ == "__main__":
    main()
