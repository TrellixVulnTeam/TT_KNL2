import numpy as np
import pandas as pd
from collections import Counter

def generar_vectores_filtrado(dictamenes, materias_obligatorias, materia_dictamen):
    vector, vectores = [],[]
    periodos_permitidos = ['10/1','10/2', '11/1', '11/2', '12/1', '12/2', '13/1',
                       '13/2', '14/1', '14/2', '15/1', '15/2', '16/1', '16/2', 
                       '17/1', '17/2', '18/1', '18/2', '19/1', '19/2','20/1','20/2']
    for d in dictamenes:
        if d['materia'] == materia_dictamen:
            materia = materias_obligatorias.index(d['materia']) if d['materia'] in materias_obligatorias else 50
            vector.append(materia)
            vector.append(periodos_permitidos.index(d['inicio']) - periodos_permitidos.index(d['periodo_de_ingreso']))
            vector.append(d['materias_cursadas'])
            vectores.append(vector.copy())
            vector.clear()
    dictamenes.rewind()
    return np.array(vectores)
    
def obtener_rose_distribution(vectores,predicciones):
    p = []
    for v in vectores:
        p.append(v[1])
    periodos = sorted(list(set(p)))
    distribucion = {str(pe):0 for pe in periodos}
    for i,v in enumerate(vectores):
        if predicciones[i] == 1:
            distribucion[str(v[1])] += 1
    d = [{"value" : v, "name" : k} for k,v in distribucion.items()]
    return d

def generar_vectores(dictamenes, materias_obligatorias):
    vector, vectores = [],[]
    periodos_permitidos = ['10/1','10/2', '11/1', '11/2', '12/1', '12/2', '13/1',
                       '13/2', '14/1', '14/2', '15/1', '15/2', '16/1', '16/2', 
                       '17/1', '17/2', '18/1', '18/2', '19/1', '19/2','20/1','20/2']
    for d in dictamenes:
        materia = materias_obligatorias.index(d['materia']) if d['materia'] in materias_obligatorias else 50
        vector.append(materia)
        vector.append(periodos_permitidos.index(d['inicio']) - periodos_permitidos.index(d['periodo_de_ingreso']))
        vector.append(d['materias_cursadas'])
        vectores.append(vector.copy())
        vector.clear()
    if not isinstance(dictamenes, list):
        dictamenes.rewind()
    return np.array(vectores)

def get_materias(dictamenes):
    materias_dictamenes = set()
    for d in dictamenes:
        materias_dictamenes.add(d['materia'])
    dictamenes.rewind()
    materias_dictamenes = sorted(list(materias_dictamenes))
    materias_dictamenes.insert(0,'Total')
    return materias_dictamenes

def generar_distribucion(predicciones):
    distribucion = []
    c = dict(Counter(predicciones))
    print(c)
    try:
        for value,count in c.items():
            if value == 0:
                distribucion.append({'value' : count, 'name' : 'No cumple'})
            else:
                distribucion.append({'value' : count, 'name' : 'Cumple'})
    except:
        pass
    if 0 in c.keys():
        indice = 1 - (c[0] / sum(c.values()))
    else:
        indice = 1
    return distribucion, indice