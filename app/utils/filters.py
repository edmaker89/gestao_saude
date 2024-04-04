from flask import json
from markupsafe import Markup 
from datetime import datetime

def format_cpf(cpf):
    if len(cpf) == 11:
        cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return Markup(cpf_formatado)
    else:
        return cpf
    
def format_cns(cns):
    if len(cns) == 15:
        cns_formatado = f"{cns[:3]} {cns[3:7]} {cns[7:11]} {cns[11:]}"
        return Markup(cns_formatado)
    else:
        return cns
    
def format_data(data):
    try:
        if type(data) == str:
            data = datetime.strptime(data, "%Y-%m-%d")
        data_formatada = data.strftime("%d/%m/%Y")
        return Markup(data_formatada)
    except ValueError:
        return data

def format_datatime(data):
    try:
        data_formatada = data.strftime("%d/%m/%Y")
        return Markup(data_formatada)
    except ValueError:
        return data
    
def data_padrao(data):
    try:
        data_obj = datetime.strptime(data, "%d/%m/%Y")
        return data_obj
    except Exception as e:
        return data

# def tojson(obj):
#     try:
#         telefones = json.loads(obj)
#         return Markup(telefones)
#     except Exception as e:
#         print(e)
#         return obj