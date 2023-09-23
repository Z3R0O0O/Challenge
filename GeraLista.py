# Deve ser rodado antes do matador de processos!
# OBS: TODOS os processos que devem permanecer funcionando devem esta rodando no momento da execução!

import os

# Obtém a lista de PIDs em execução no sistema
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

# Cria um arquivo de texto para armazenar os PIDs
with open('pids.txt', 'w') as file:
    for pid in pids:
        file.write(f'{pid}\n')

print('PIDs foram salvos em pids.txt')
