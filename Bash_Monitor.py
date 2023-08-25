# pip install pyinotify

import os
import subprocess
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_MODIFY 

# Diretórios que serão monitorados
diretorios_assistidos = ['/home/cobaia', '/home', '/home/cobaia/Downloads', '/home/cobaia/Desktop'] 

# Classe para manipular eventos
class EventHandler(ProcessEvent):    
    def process_IN_MODIFY(self, evento):         # É chamada quando ocorrem modificações no diretório monitorado.        
        for dir_path in diretorios_assistidos:            
            if evento.pathname.startswith(dir_path):                
                print(f"Arquivo modificado: {evento.pathname}")                
                subprocess.run(['bash', '-i']) 

# Configuração do monitoramento
wm = WatchManager()                     # Gerencia as operações de monitoramento de sistema de arquivos        
mask = IN_MODIFY                        # Uma constante que especifica que estamos interessados em eventos de modificação de arquivos.
handler = EventHandler()                # Uma classe personalizada que herda de ProcessEvent 
notifier = Notifier(wm, handler)        # Manipulador de eventos, recebe e processa os eventos que ocorrem nos diretórios monitorados. 

# Inicia o monitoramento para cada diretório
watch_descriptors = []
for dir_path in diretorios_assistidos:    
    wdd = wm.add_watch(dir_path, mask, rec=True)    
    watch_descriptors.append(wdd) 
    
print("Monitorando os diretórios") 

try:    
    while True:         # ProcessEnvent-Herda o a configuração do manipulador de eventos personalizado para os eventos do pyinotify.        
        try:            
            notifier.process_events()              
            if notifier.check_events():                
                notifier.read_events()        
        except KeyboardInterrupt:            
            notifier.stop()            
            break
finally:    
    print("Achamos algo.")
