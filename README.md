# Sistema de Gestão Acadêmica Integrado (Python + TXT)

## Integrantes
**EQUIPE ALFA** (Alunos e Cursos)
- Beatriz Feitosa – Curso ADS
- Jéssica Boa Morte – Curso ADS
- Caroline Dias – Curso ADS
- Sandro Jesus – Curso ADS

**EQUIPE BETA** (Professores e Disciplinas)
- José Augusto – Disciplina Banco de Dados
- Fernando Araujo – Disciplina Python
- Andreia Lima – Disciplina Engenharia de Software
- Pedro Oliveira – Disciplina Desenvolvimento de Algoritmo

## Como executar (ponto de entrada único: `main.py`)
```
python main.py          # menu no console (opção 7 abre a interface gráfica)
python main.py --gui    # abre direto a interface gráfica (Tkinter)
```

## Estrutura e responsabilidades
```
base.py               Entidade (modelo de dados) e GerenciadorBase (RF: CRUD + .txt)
alfa/                 Aluno, Curso (modelos) + GerenciadorAlunos, GerenciadorCursos
beta/                 Professor, Disciplina (modelos) + GerenciadorProfessores, GerenciadorDisciplinas
integracao.py         Sistema: liga os gerenciadores e gera o relatório (RF13-RF15)
main.py               Ponto de entrada, menu e encerramento (RF16-RF18)
interface_grafica.py  Interface gráfica (desafio)
dados/                alunos.txt, cursos.txt, professores.txt, disciplinas.txt
```
**Regra de projeto:** as classes de entidade são apenas modelos de dados
(`__init__`, `@property` com validação e `__str__`). Toda a lógica funcional
(CRUD, conversão objeto <-> linha, leitura e gravação de arquivo, integridade
entre módulos) fica nas classes Gerenciadoras.

## Formato dos arquivos .txt
Uma linha por registro, campos separados por `;`, na ordem dos atributos:
```
alunos.txt       matricula;nome;cpf;email;codigo_curso
cursos.txt       codigo_curso;nome;modalidade
professores.txt  codigo_professor;nome;cpf;especialidade
disciplinas.txt  codigo_disciplina;nome;carga_horaria;codigo_professor;codigo_curso
```
Exemplo: `202301;João Silva;123.456.789-00;joao@email.com;10`

- O caractere `;` é proibido dentro dos campos (validado nos setters).
- Os IDs são tratados como texto.

## Rastreabilidade dos requisitos
| RF | Descrição resumida | Onde está implementado |
|----|--------------------|------------------------|
| RF01 | Cadastrar | `GerenciadorBase.cadastrar` (+ `validar` nos gerenciadores) |
| RF02 | Listar | `GerenciadorBase.listar` / `carregar`; exibição em `main.menu_crud` e na GUI |
| RF03 | Pesquisar por código ou nome | `GerenciadorBase.buscar_por_codigo` e `pesquisar` |
| RF04 | Alterar | `GerenciadorBase.alterar` (altera uma cópia, valida e só então grava) |
| RF05 | Excluir | `GerenciadorBase.excluir` (bloqueia se houver vínculos) |
| RF06 | Atributos de Aluno | `alfa/aluno.py` – `Aluno` |
| RF07 | Atributos de Curso | `alfa/curso.py` – `Curso` |
| RF08 | Atributos de Professor | `beta/professor.py` – `Professor` |
| RF09 | Atributos de Disciplina | `beta/disciplina.py` – `Disciplina` |
| RF10 | Arquivos .txt com `;` | `GerenciadorBase.ARQUIVO`, `_para_linha`, `salvar` |
| RF11 | Carregamento inicial | `GerenciadorBase.__init__` -> `carregar` (via `Sistema()`) |
| RF12 | Sincronização de escrita | `salvar()` chamado em cadastrar, alterar e excluir |
| RF13 | Aluno -> Curso | `GerenciadorAlunos.validar` (`codigo_curso`) |
| RF14 | Disciplina -> Professor e Curso | `GerenciadorDisciplinas.validar` |
| RF15 | Relatório integrado | `Sistema.relatorio` em `integracao.py` |
| RF16 | `main.py` único | `main.py` (console e `--gui`) |
| RF17 | Menu de navegação | `main.menu_principal` e abas da GUI |
| RF18 | Encerramento controlado | opção 0, Ctrl+C e fim de entrada tratados em `main.main` |

## Decisões de projeto
- **Código/matrícula não é alterável (RF04).** Alterar o código de um curso ou
  professor deixaria alunos e disciplinas apontando para um código inexistente.
  Todos os demais atributos podem ser alterados.
- **Integridade referencial.** Não é possível cadastrar aluno ou disciplina com
  curso/professor inexistente, nem excluir curso/professor que ainda tenha vínculos.
- **Alteração segura.** O gerenciador altera uma cópia do objeto e só substitui
  o original se a validação passar; um erro nunca deixa o arquivo inconsistente.

## Dificuldades encontradas na integração
- Definir antes os nomes dos identificadores (`codigo_curso`, `codigo_professor`).
- Garantir a consistência entre arquivos de equipes diferentes (validação cruzada).
- Evitar código repetido: criou-se `GerenciadorBase`, reutilizado pelas duas equipes.
- Separar o que é modelo (entidades) do que é regra funcional (gerenciadores).
