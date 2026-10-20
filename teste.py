from modprof import Professor

codigo_prof =  '001'
nome = 'Augusto Martins'
cpf = '00011122233'
especialidade = 'Banco de dados'

professor1 = Professor(codigo_prof, nome, cpf, especialidade) 


print(professor1)
print(professor1._cpf)