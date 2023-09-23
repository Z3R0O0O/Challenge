import psutil
import time
import os
import signal

# Limite de uso da CPU (em porcentagem)
limite_cpu = 23.0

# PID do processo Python atual
pid_python = os.getpid()

# Obtém a lista de PIDs em execução no sistema
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

# Cria um arquivo de texto para armazenar os PIDs
with open('pids.txt', 'w') as file:
    for pid in pids:
        file.write(f'{pid}\n')

print('Processos atuais registrados') 

# Nome do arquivo de texto que contém os PIDs a serem excluídos
arquivo_pids_excecoes = "pids.txt"

# Função para ler os PIDs do arquivo de texto
def ler_pids_excecoes(arquivo):
    try:
        with open(arquivo, "r") as file:
            pids_excecoes = [int(line.strip()) for line in file.readlines()]
        return pids_excecoes
    except FileNotFoundError:
        return []

# Adicione o PID do processo Python atual à lista de exceções
processos_excepcionais = [pid_python]

while True:
    try:
        # Carregue a lista de PIDs a partir do arquivo de exceções
        pids_excecoes = ler_pids_excecoes(arquivo_pids_excecoes)

        for processo in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
            try:
                process_info = processo.info
                pid = process_info['pid']
                nome_processo = process_info['name']
                uso_cpu = process_info['cpu_percent']

                # Verifique se o processo não está na lista de exceções
                if (
                    pid not in processos_excepcionais
                    and uso_cpu > limite_cpu
                    and pid not in pids_excecoes
                ):
                    print(f"Processo {nome_processo} é suspeito. Encerrando com SIGTERM.\nPara abrir novos processos encerre e rode o código novamente!")
                    os.kill(pid, signal.SIGTERM)
                    
                    # Aguarde um curto período antes de verificar o próximo processo
                    time.sleep(0.1)
                    
                    # Se o processo ainda estiver ativo após o SIGTERM, encerre-o com SIGKILL
                    processo = psutil.Process(pid)
                    if processo.is_running():
                        print(f"Processo não respondeu ao SIGTERM. Encerrando com SIGKILL.")
                        os.kill(pid, signal.SIGKILL)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Aguarde um tempo antes de verificar novamente
        time.sleep(0.01)  # Verifique a cada segundo (ajuste conforme necessário)
    except KeyboardInterrupt:
        break
