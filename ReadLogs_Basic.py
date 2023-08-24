def read_log_file(log_file_path):
    try:
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                if "failed" in line.lower():# Verifica se a palavra "failed" está na linha (ignorando maiúsculas/minúsculas)
                    print(line.strip())	# Remove espaços em branco e imprime a linha
                elif "failure" in line.lower():# Verifica se a palavra "failure" está na linha (ignorando maiúsculas/minúsculas)
                    print(line.strip())	# Remove espaços em branco e imprime a linha
    except FileNotFoundError:
        print(f"O arquivo '{log_file_path}' não foi encontrado.")



if __name__ == "__main__":
    log_file_path = "/var/log/auth.log"# Substitua pelo caminho do seu arquivo de log
    read_log_file(log_file_path)
    

