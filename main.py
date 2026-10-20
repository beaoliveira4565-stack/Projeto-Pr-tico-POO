from alfa import GerenciadorCursos

def exibir_menu():
    print("\n==========================================")
    print("   Sistema de Gestão - Módulo de Curso")
    print("==========================================")
    print("1. Cadastrar curso")
    print("2. Listar cursos")
    print("3. Pesquisar curso por código")
    print("4. Alterar curso")
    print("5. Excluir curso")
    print("6. Sair")

def main():
    # Inicializa o gerenciador (carrega os dados do arquivo cursos.txt automaticamente)
    gerenciador = GerenciadorCursos()

    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- CADASTRAR CURSO ---")
            cod = input("Código do Curso: ").strip()
            nome = input("Nome do Curso: ").strip()
            mod = input("Modalidade (Presencial/EAD): ").strip()
            sucesso, msg = gerenciador.cadastrar(cod, nome, mod)
            print(msg)

        elif opcao == "2":
            print("\n--- LISTAR CURSOS ---")
            cursos = gerenciador.listar()
            if not cursos:
                print("Nenhum curso cadastrado.")
            else:
                for c in cursos:
                    print(f"Código: {c.codigo} | Nome: {c.nome} | Modalidade: {c.modalidade}")

        elif opcao == "3":
            print("\n--- PESQUISAR CURSO ---")
            cod = input("Digite o código do curso: ").strip()
            c = gerenciador.pesquisar_por_codigo(cod)
            if c:
                print(f"Encontrado -> Código: {c.codigo} | Nome: {c.nome} | Modalidade: {c.modalidade}")
            else:
                print("Curso não encontrado.")

        elif opcao == "4":
            print("\n--- ALTERAR CURSO ---")
            cod = input("Código do curso a alterar: ").strip()
            novo_nome = input("Novo nome (pressione Enter para manter): ").strip()
            nova_mod = input("Nova modalidade (pressione Enter para manter): ").strip()
            _, msg = gerenciador.alterar(cod, novo_nome or None, nova_mod or None)
            print(msg)

        elif opcao == "5":
            print("\n--- EXCLUIR CURSO ---")
            cod = input("Código do curso a excluir: ").strip()
            _, msg = gerenciador.excluir(cod)
            print(msg)

        elif opcao == "6":
            print("\nEncerrando o sistema. Até logo!")
            break

        else:
            print("\nOpção inválida! Escolha um número entre 1 e 6.")

if __name__ == "__main__":
    main()