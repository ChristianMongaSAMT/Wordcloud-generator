
import logging
import logmanager

logmanager.get_configured_logger()

class Coso():

    b = None

    _c = None

    def __init__(self, params):
        self.a = params

    def get_a(self) -> str:
        return self.a

    def set_a(self, value):
        self.a = value


    def set_fkljdsjfkls(self, v1, v2='0000'):
        self.v1 = v1
        self.v2 = v2

def run():

    coso = Coso('mip parametro')

    coso.a = 'asfjka'

    a = 'ciao'
    logging.debug(f'stringa di log: {a} lunghezza: {len(a)}')

    a = ['ciao', 'bella', 'ciao', 81247981]
    logging.debug(f'list di log: {a} lunghezza: {len(a)}')

    a = {
        'chiave1':9324902, 
        'chiave2':'ciao',
        'chiave3':[1,'20',[3,6,4]]
     }
    a['chiave4']='bla'
    logging.debug(f'list di log: {a} lunghezza: {len(a)}')    

    logging.debug(f'valore: {a["chiave4"]}')


if __name__ == '__main__':
    run()