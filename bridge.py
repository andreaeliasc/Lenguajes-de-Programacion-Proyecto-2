### Disenio de Lenguajes de Programacion
## Andrea Elias
## 17048

### Programa Bridge que contiene la siguiente funcion:
### - Automata: Generar un AFN Directo dada una expresion aumentada

### Se importan librerias para
### - Random: Generacion de documentos PDF con correlativos random para los diagramas
### - Copy: Copiar listas para no tener conflicto de apuntar a una misma direccion de memoria para referencia
### - Pickle: Serializar variables, en este caso el automata
import random
import copy
import pickle

### Se importan los distintos modulos creados para realizar las distintas tareas del proyecto
### - lectorExpresionesMejorado: Modulo Final Lector para traducir expresiones a una estructura de listas que se utilizará como arbol
### - traductorExpresion_a_AFD: Generacion de documentos PDF con correlativos random para los diagramas
### - simulaciones: Simulacion del AFD
import lectorExpresionesMejorado
import traductorExpresion_a_AFD
import simulaciones

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

### Funcion que nos va a permitir generar un automata AFD a partir de una expresion regular
def automata(tokensRegex, dictTokens, dictKeywords, whiteSpace):
    ### Iniciamos con las entradas de los tokens
    arbolExpresionRegularAFD, _, _ = lectorExpresionesMejorado.conversionExpresionRegular(tokensRegex)

    ###------------------------------------------AFD-DIRECTO----------------------------------------###
    ### Se hace una sustitucion previa para las expresiones 
    arbolNodosExpresionRegularSustituido = traductorExpresion_a_AFD.sustitucionPrevia(arbolExpresionRegularAFD)

    ### Se convierten los nodos que no son operandos en Nodos para almacenar
    ### Conjunto estados, transiciones, estado inicial, estado final
    ### Aqui el arbol ya esta en modo nodos para procesarse los nodos Complejos
    ### Las correspondencias las tendremos guardadas para referencias de la construccion de subconjuntos
    arbolNodosExpresionRegularAFD, _, correspondencias = traductorExpresion_a_AFD.traduccionBase(arbolNodosExpresionRegularSustituido, 1, [])

    ### Obtenemos los nodos hojas que ya poseen sus posiciones
    nodosHoja = traductorExpresion_a_AFD.devolverNodosHoja(arbolNodosExpresionRegularAFD, [])

    ### Se realiza la definicion de nodos que no son hojas con sus operaciones nullable, firstpos, lastpos
    nodoRoot, nodos = traductorExpresion_a_AFD.definirNodosAFD(arbolNodosExpresionRegularAFD, 0, [])

    ### Unimos los nodos en un solo arreglo
    nodosFinales = nodosHoja + nodos

    ### Se calcula la tabla de followpos con los nodosFinales resultantes
    tablaFollowpos = traductorExpresion_a_AFD.followpos(nodosFinales, correspondencias)

    ### Obtener el conjunto de simbolos
    simbolos = traductorExpresion_a_AFD.simbolosAFDDirecta(correspondencias)

    ### Obtener las transiciones y estados (el primer estado es el estado inicial)
    dStatesAFD, dTransAFD  = traductorExpresion_a_AFD.traduccionAFDDirecta(nodoRoot, simbolos, tablaFollowpos, correspondencias)

    posicionesFinales = []

    ### Posicion para determinar que estados son finales
    for correspondencia in correspondencias:
        if correspondencia[0] == '#':
            posicionesFinales.append(correspondencia[1])

    ### Creamos una estructura de Nodo para simular el AFD
    afdd = traductorExpresion_a_AFD.convertirAFDDirectaNodo(dStatesAFD, dTransAFD, simbolos, posicionesFinales)

    ### Serializar afdd con Pickle
    with open('automata.pickle', 'wb') as f:
        pickle.dump(afdd, f)

    ### Serializar diccionario de Tokens con Pickle
    with open('tokens.pickle', 'wb') as f:
        pickle.dump(dictTokens, f)

    ### Serializar diccionario de Keywords con Pickle
    with open('keywords.pickle', 'wb') as f:
        pickle.dump(dictKeywords, f)

    ### Serializar Set de Ignore con Pickle
    with open('ignore.pickle', 'wb') as f:
        pickle.dump(whiteSpace, f)

    ### Escribir el scanner
    linea = '''### Disenio de Lenguajes de Programacion
## Andrea Elias
## 17048

### Programa Scanner que ejecuta las siguientes tareas:
### - Leer un archivo con tokens que el automata a cargar podra reconocer

### Se importan librerias para
### - Random: Generacion de documentos PDF con correlativos random para los diagramas
### - Copy: Copiar listas para no tener conflicto de apuntar a una misma direccion de memoria para referencia
### - Pickle: Serializar variables, en este caso el automata
import random
import copy
import pickle

### Se importan los distintos modulos creados para realizar las distintas tareas del proyecto
### - lectorExpresionesMejorado: Modulo Final Lector para traducir expresiones a una estructura de listas que se utilizara como arbol
### - traductorExpresion_a_AFD: Generacion de documentos PDF con correlativos random para los diagramas
### - simulaciones: Simulacion del AFD
import lectorExpresionesMejorado
import traductorExpresion_a_AFD
import simulaciones

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

IGNORE = 'IGNORE'

### Lectura de pickle del Automata Serializado
with open('automata.pickle', 'rb') as f:
    afdd = pickle.load(f)

### Lectura de pickle de la definicion de TOKENS Serializado
with open('tokens.pickle', 'rb') as f:
    tokens = pickle.load(f)

### Lectura de pickle de la definicion de TOKENS Serializado
with open('keywords.pickle', 'rb') as f:
    keywords = pickle.load(f)

### Lectura de pickle de la definicion de IGNORE Serializado
with open('ignore.pickle', 'rb') as f:
    ignoreSet = pickle.load(f)

### De aqui en adelante vamos a hacer la codificacion del Scanner
### Para la lectura de los tokens

### Primero leemos el archivo a modo de obtener una sola linea
fileName = input("Ingrese el nombre de su archivo a validar: ")
fileTxt = open(fileName, 'r', encoding='utf-8')
stringValidar = ''.join(fileTxt.readlines())
stringValidarAscii = ''
#print(tokens)

### Ahora pasamos el string a la simulacion
posicion = 0
while posicion < len(stringValidar):
    token, posicion, cadenaRetornar = simulaciones.simulacionAFD2(afdd, stringValidar, posicion, tokens, ignoreSet)

    ### Se limpia la cadena a retornar de los ignores
    cadenaFinal = ''
    for caracter in cadenaRetornar:
        if ignoreSet:
            caracterAscii = ord(caracter)
            if caracterAscii in ignoreSet:
                continue
        cadenaFinal = cadenaFinal + caracter

    if token:
        ### Se obtiene el valor de la bandera del token
        valorToken = tokens[token]
        valorBandera = valorToken[1]

        ### Revisar el valor de la bandera
        if (valorBandera == 1) and (cadenaFinal in keywords.values()):
            ### Imprimir que el string si es un KEYWORD
            print('KEYWORD =>', cadenaFinal)
        else:
            print(token,'=>', cadenaFinal)
    else:
        print('Error Lexico =>', cadenaFinal)'''

    archivo = open("scanner.py", "w")
    archivo.write(linea)
    archivo.close()

    print("Scanner producido")
