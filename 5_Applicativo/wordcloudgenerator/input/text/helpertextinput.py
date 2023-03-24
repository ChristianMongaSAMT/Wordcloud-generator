
import os

from bs4 import BeautifulSoup
class helperTextInput():
    # Lista
    proxySetup = []
    isProxySetup = False
    def __init__(self):
        pass
    def setProxyIfExist(self):
        # Se non ci sono le variabili d'ambiente del proxy le aggiunge
        if(not(self.isProxySetup)):
            for name, value in os.environ.items():
                if(name.upper() == 'HTTP_PROXY' or name.upper() == 'HTTPS_PROXY'):
                    self.proxySetup.append(f"{name}: {value}")
            self.isProxySetup = True
            print(self.proxySetup)



    def removeTags(self, html):
        # Tramite BeautifulSoup vengono rimossi tutti i tag della pagina web e viene formattato il testo
        pageParsed = BeautifulSoup(html, 'html.parser')
        for data in pageParsed(['style', 'script']):
            data.decompose()
        return ' '.join(pageParsed.stripped_strings)


    