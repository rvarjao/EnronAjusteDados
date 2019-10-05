import os
import re
import json
import cProfile

def procurar_destinatarios(campo, txt):
    """
    :param campo: "to:", "cc:" ou "cco:"
    :param txt: Texto do arquivo atual
    :return: array com os destinatarios
    """
    compile = re.compile(r'{}\w*:\w*(.*)'.format(campo))
    compile_email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    reg = compile.search(txt)  # Run a regex search anywhere inside a string
    if reg:  # If there is a match
        string = reg.group(1)
        fields = string.split(",")
        array = []
        for to in fields:
            t = to.strip()
            if compile_email.search(t):
                if t not in emails:
                    emails[t] = {}
                if t != "":
                    array.append(t)
        return array
    else: return []


# diretorio principal dos arquivos
# nao esta junto do projeto principal
# esta em uma pasta anterior
path = '../maildir'

# Dicionario de retorno dos dados
# tera o formato: {"emailFrom1" : {"email_to_1" : 1, "email_to_2" : 2}}
# cada chave sera o email do remetente principal
# cada valor sera um segundo dicionario
# em que as chaves serao os seus destinatarios
# com a quantidade de emails enviados
#
# ex:
# {"rvarjao@gmail.com" :
#      {"joao@gmail.com" : 2, "jose@gmail.com" : 3}
# }

emails = dict()

i = 0
cProfile.run('re.compile("foo|bar")')

# pega o caminho de todos os arquivos
# r=root, d=directories, f = files
for root, dirs, files in os.walk(path):
    for file in files:
        i += 1
        if i % 1000 == 0: print(i)

        with open(os.path.join(root, file), "r", encoding="ISO-8859-1") as auto:
            txt = auto.read()
            if txt.__len__() > 5: #alguns arquivos estao vazios
                txt = txt.lower() #lowercase para nao dar conflito
                # print(txt)
                #procura pelo remetente
                compileFrom = re.compile(r'from\s*:\s*(.*)')
                regFrom = compileFrom.search(txt)  # Run a regex search anywhere inside a string
                if regFrom:  # If there is a match
                    emailFrom = regFrom.group(1)
                    emailFrom = emailFrom.strip()
                    # se nao existir esse email from, adiciona no dicionario
                    if emailFrom not in emails:
                        emails[emailFrom] = {}

                    # array com os destinatarios

                    array_dest = procurar_destinatarios("to", txt) +\
                                 procurar_destinatarios("cc", txt) +\
                                 procurar_destinatarios("cco", txt)

                    # remover duplicatas
                    array_dest = list(dict.fromkeys(array_dest))
                    # print(array_dest)
                    for dest in array_dest:
                        if dest in emails[emailFrom]:
                            emails[emailFrom][dest] += 1
                        else:
                            emails[emailFrom][dest] = 1


    # if i > 100: break #fazendo alguns para teste


with open('emails.txt', 'w') as file:
    file.write(json.dumps(emails))  # use `json.loads` to do the reverse

