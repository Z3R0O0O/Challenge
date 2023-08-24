# pip install pyinotify

import os                                                                 # Interage com o sistema
import time                                                               # Funções com relação a tempo
import subprocess                                                         # Processos secundários externos ao python
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_MODIFY     # Biblioteca para o monitoramento do sistema

diretorio = '/home/cobaia'                              # Onde está monitorando
arquivo = '.bash_history'                               # O que está monitorando
caminho = os.path.join(diretorio, arquivo)

palavras = ['su', 'sudo']                               # Palavras a serem procuradas

# Classe para manipular eventos
class EventHandler(ProcessEvent):                       # Personalizada para lidar com eventos específicos.
    def process_IN_MODIFY(self, evento):                 # É chamada quando ocorrem modificações em arquivos no diretório monitorado.
        if evento.pathname == caminho:
            with open(caminho, 'r') as f:
                conteudo = f.read()
                for chaves in palavras:
                    if chaves in conteudo:
                        print(f"A palavra '{chaves}' foi encontrada em {arquivo}")
                        subprocess.run(['bash', '-i'])

# Configuração para o monitoramento
wm = WatchManager()                     # Gerencia as operações de monitoramento de sistema de arquivos        
mask = IN_MODIFY                        # Uma constante que especifica que estamos interessados em eventos de modificação de arquivos.
handler = EventHandler()                # Uma classe personalizada que herda de ProcessEvent e é usada para achar "sudo" e "su", no caso
notifier = Notifier(wm, handler)        # Manipulador de eventos, recebe e processa os eventos que ocorrem nos diretórios monitorados.

# Inicia do monitoramento
monitor = wm.add_watch(diretorio, mask, rec=True)      
print(f"Monitorando {diretorio}/{arquivo}")

if __name__ == "__main__":
    try:
        while True:
            try:
                notifier.process_events() # ProcessEnvent-Herda o a configuração do manipulador de eventos personalizado para os eventos do pyinotify.
                if notifier.check_events():
                    notifier.read_events()
            except KeyboardInterrupt:
                notifier.stop()
                break
    finally:
        print("Monitoramento encerrado.")
