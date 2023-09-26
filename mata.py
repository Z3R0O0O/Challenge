import psutil
import time
import os
import signal

# Limite de uso da CPU (em porcentagem)
limite_cpu = 23.0

# Nome do processo Python atual
nome_python = os.path.basename(__file__)

# Nome do arquivo de texto que contém os nomes dos processos a serem excluídos
arquivo_nomes_excecoes = "nomes_excecoes.txt"

# Função para ler os nomes dos processos do arquivo de texto
def ler_nomes_excecoes(arquivo):
    try:
        with open(arquivo, "r") as file:
            nomes_excecoes = [line.strip() for line in file.readlines()]
        return nomes_excecoes
    except FileNotFoundError:
        return []

# Adicione o nome do processo Python atual à lista de exceções
nomes_excepcionais = [nome_python]

while True:
    try:
        # Carregue a lista de nomes dos processos a partir do arquivo de exceções
        nomes_excecoes = ler_nomes_excecoes(arquivo_nomes_excecoes)

        for processo in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']):
            try:
                process_info = processo.info
                nome_processo = process_info['name']
                uso_cpu = process_info['cpu_percent']
                
                if nome_processo.startswith('kworker/'):
                    # Não faça nada, permita que esses processos continuem
                    continue

                # Verifique se o nome do processo não está na lista de exceções
                if (
                    nome_processo not in nomes_excepcionais
                    and uso_cpu > limite_cpu
                    and nome_processo not in nomes_excecoes
                ):
                    print(f"Processo {nome_processo} é desconhecido. Encerrando com SIGTERM.")
                    
                    # Obtenha o PID do processo
                    pid = process_info['pid']
                    
                    os.kill(pid, signal.SIGTERM)
                    
                    # Aguarde um curto período antes de verificar o próximo processo
                    time.sleep(0.1)
                    
                    # Se o processo ainda estiver ativo após o SIGTERM, encerre-o com SIGKILL
                    processo = psutil.Process(pid)
                    if processo.is_running():
                        print(f"Processo {nome_processo} não respondeu ao SIGTERM. Encerrando com SIGKILL.")
                        os.kill(pid, signal.SIGKILL)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            except PermissionError:
            	print(f"Não foi possível encerrar o processo {nome_processo} devido a permissões insuficientes.")

        # Aguarde um tempo antes de verificar novamente
        time.sleep(0.01)  # Verifique a cada segundo (ajuste conforme necessário)
    except KeyboardInterrupt:
        break
