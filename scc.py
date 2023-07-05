#CLASE DATOS DE CONECCION
#CLASE DATOS DE CONECCION
path = 'base/conection.txt'
dato = ''
URL = ''
bl = False
LBIO = []
lista = []
ip = ''
prt = 0
bol = False
lugar = ''


with open(path) as archivo:
    for linea in archivo:
        dato = linea.replace("\n", "")
        if(dato.__contains__('URL')):
            URL = dato.replace('URL', '')
        if(dato.__contains__('ip')):
            ip = dato.replace('ip', '')
            lista.append(ip)
        if (dato.__contains__('prt')):
            prt = int(dato.replace('prt', ''))
            lista.append(prt)
        if (dato.__contains__('bol')):
            bol = eval(dato.replace('bol', ''))
            lista.append(bol)
        if (dato.__contains__('Lugar')):
            lugar = dato.replace('Lugar', '')
            lista.append(lugar)
            bl = True
        if bl:
            LBIO.append(lista)
            bl = False
            lista = []