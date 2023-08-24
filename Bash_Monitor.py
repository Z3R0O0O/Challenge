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
    def __init__(self):
        self.contando_sudo = 0
        self.contando_su = 0
    
    def process_IN_MODIFY(self, evento):                 # É chamada quando ocorrem modificações em arquivos no diretório monitorado.
        if evento.pathname == caminho:
            with open(caminho, 'r') as f:
                conteudo = f.read()
                for chaves in palavras:
                    if chaves in conteudo:
                        if chaves == 'sudo':
                            self.contando_sudo += 1
                        elif chaves == 'su':
                            self.contando_su += 1
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

while True: 
    try:
        while True:
            try:
                notifier.process_events()   # ProcessEnvent-Herda o a configuração do manipulador de eventos personalizado para os eventos do pyinotify.
                if notifier.check_events():
                    notifier.read_events()
                print(f"'sudo' foi encontrado {handler.contando_sudo} vezes.") # Exibir as contagens das palavras encontradas 
                print(f"'su' foi encontrado {handler.contando_su} vezes.")
            except KeyboardInterrupt:       # Caso encerre o código manualmente
                notifier.stop()
                break
    finally:
        print(f"Total de vezes que 'sudo' foi encontrado: {handler.contando_sudo}") # Mostra a contagem final
        print(f"Total de vezes que 'su' foi encontrado: {handler.contando_su}")
