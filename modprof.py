
class Professor:

    def __init__(self, codigo_prof, nome, cpf, especialidade):
        self._codigo_prof = codigo_prof
        self._nome = nome
        self._cpf = cpf
        self._especialidade = especialidade
        # 1. Guarde os quatro dados em atributos protegidos.
        # Dica: cada atributo deve começar com self._



    def __str__(self):

        return f'O novo professor é: {self._nome}, com código {self._codigo_prof} e cpf{self._cpf}'
        # Aqui você vai devolver um texto que represente
        # a disciplina, e não receber os dados novamente.
        