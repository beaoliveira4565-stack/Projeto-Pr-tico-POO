
class Disciplina:

    def __init__(self, codigo_disciplina, nome, carga_horaria, codigo_professor, codigo_curso):
       self._codigo_disciplina = codigo_disciplina
       self._nome = nome
       self._carga_horaria = carga_horaria
       self._codigo_professor = codigo_professor
       self._codigo_curso = codigo_curso
        # 2. Faça o método devolver uma representação
        # legível do professor.
    
    def __str__(self):
    
        return f'A nova disciplina do nosso curso é: {self._nome}, o código de identificação da disciplina é: {self._codigo_disciplina}'
