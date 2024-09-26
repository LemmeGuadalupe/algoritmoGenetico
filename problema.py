import random
from enum import IntEnum

DIAS_SEMANA = IntEnum("DIA_SEMANA", ["LUNES", "MARTES", "MIERCOLES", "JUEVES"])
FRUTAS = IntEnum("FRUTA", ["MANGO", "BANANA", "MANZANA", "PERA"])
VEGETALES = IntEnum("VEGETAL" ,["KALE", "ESPINACA", "COL_RIZADA", "LECHUGA"])
NUECES = IntEnum("NUEZ", ["PECAN", "ALMENDRAS", "MADACAMIA", "CAJU"])

POS_FRUTA = 0
POS_VEGETAL = 1
POS_NUEZ = 2

CANT_ATRIBUTOS = 3
CANT_DIAS = 4

def imprimir_ind(ind):
    for i in range(CANT_DIAS):
        print("Día de la semana:" + DIAS_SEMANA(i + 1).name)
        print("\tFruta: " + FRUTAS(ind[i * CANT_ATRIBUTOS + POS_FRUTA]).name)
        print("\tVegetal: " + VEGETALES(ind[i * CANT_ATRIBUTOS + POS_VEGETAL]).name)
        print("\tNuez: " + NUECES(ind[i * CANT_ATRIBUTOS + POS_NUEZ]).name)

def crear_ind(cls, str_cls):
    ind = cls()
    for i in range(CANT_DIAS * CANT_ATRIBUTOS):
        ind.append(random.randint(1, 4))
    
    ind.strategy = str_cls()
    return ind

def verificar_condicion(v, index_dia, pos_atr1, val1, pos_atr2, val2):
    pos_absoluta1 = (index_dia -1) * CANT_ATRIBUTOS + pos_atr1
    pos_absoluta2 = (index_dia -1) * CANT_ATRIBUTOS + pos_atr2
    return v[pos_absoluta1] == val1 and v[pos_absoluta2] == val2  

def verificar_existe(v, pos_atr1, val1, pos_atr2, val2):
    for i in range(4):
        if(verificar_condicion(v, i, pos_atr1, val1, pos_atr2, val2)):
            return True
    return False

def verificar_dia_condicion(v, index_dia, pos_atr, val):
    return v[(index_dia -1) * CANT_ATRIBUTOS + pos_atr] == val

def cuanto_se_repiten(v):
    puntaje = 0
    for i in range(0,CANT_ATRIBUTOS * CANT_DIAS):
        for j in range(i + CANT_ATRIBUTOS, CANT_DIAS * CANT_ATRIBUTOS, CANT_ATRIBUTOS):
            if v[i % (CANT_DIAS * CANT_ATRIBUTOS)] == v[j % (CANT_DIAS * CANT_ATRIBUTOS)]:
                puntaje += 1
            
    return puntaje

def verificar_condiciones_dias(ind):
    puntaje = 0

    # El licuado de banana fue un día después del licuado de nueces pecán.
    for i in range(CANT_DIAS - 1):  # Evitar desbordamiento
        if (ind[i * CANT_ATRIBUTOS + POS_NUEZ] == NUECES.PECAN and 
            ind[(i + 1) * CANT_ATRIBUTOS + POS_FRUTA] == FRUTAS.BANANA):
            puntaje += 3
            
    # El licuado de banana fue dos días después del licuado de manzana.
    for i in range(CANT_DIAS - 2):  # Evitar desbordamiento
        if (ind[i * CANT_ATRIBUTOS + POS_FRUTA] == FRUTAS.MANZANA and 
            ind[(i + 2) * CANT_ATRIBUTOS + POS_FRUTA] == FRUTAS.BANANA):
            puntaje += 3
    
    return puntaje

def calcular_condiciones_a_cumplir(ind):
    puntos = 0

    #Los licuados con espinaca y lechuga son del Lunes y Martes, aunque no necesariamente en ese orden.
    
    if verificar_dia_condicion(ind, DIAS_SEMANA.LUNES, POS_VEGETAL, VEGETALES.ESPINACA):
        puntos += 3
        
    if verificar_dia_condicion(ind, DIAS_SEMANA.LUNES, POS_VEGETAL, VEGETALES.LECHUGA):
        puntos += 3
        
    if verificar_dia_condicion(ind, DIAS_SEMANA.MARTES, POS_VEGETAL, VEGETALES.ESPINACA):
        puntos += 3
        
    if verificar_dia_condicion(ind, DIAS_SEMANA.MARTES, POS_VEGETAL, VEGETALES.LECHUGA):
        puntos += 3
    
    #El licuado del jueves es el de almendras.
        
    if verificar_dia_condicion(ind, DIAS_SEMANA.JUEVES, POS_NUEZ, NUECES.ALMENDRAS):
        puntos += 3
    
    #El licuado de pera tiene lechuga.

    if verificar_existe(ind, POS_FRUTA, FRUTAS.PERA, POS_VEGETAL, VEGETALES.LECHUGA):
        puntos += 3


    #El licuado de banana fue un día después del licuado de nueces pecán.
    #El licuado de banana fue dos días después del licuado de manzana.

    puntos += verificar_condiciones_dias(ind)

    return puntos

def calcular_restricciones(ind):
    puntos = 0

    puntos -= cuanto_se_repiten(ind) * 3

    #El licuado de nueces pecán contiene mango o banana.
    if verificar_existe(ind, POS_NUEZ, NUECES.PECAN, POS_FRUTA, FRUTAS.MANGO):
        puntos -= 3

    if verificar_existe(ind, POS_NUEZ, NUECES.PECAN, POS_FRUTA, FRUTAS.BANANA):
        puntos -= 3

    #El licuado de kale contiene macadamias.
    if verificar_existe(ind, POS_VEGETAL, VEGETALES.KALE, POS_NUEZ, NUECES.MADACAMIA):
        puntos -= 3
    
    #El licuado de espinaca contiene macadamias.
    if verificar_existe(ind, POS_VEGETAL, VEGETALES.ESPINACA, POS_NUEZ, NUECES.MADACAMIA):
        puntos -= 3

    #El licuado de banana tiene nueces pecán.
    if verificar_existe(ind, POS_FRUTA, FRUTAS.BANANA, POS_NUEZ, NUECES.PECAN):
        puntos -= 3
    
    #El licuado de manzana tiene nueces pecán.
    if verificar_existe(ind, POS_FRUTA, FRUTAS.MANZANA, POS_NUEZ, NUECES.PECAN):
        puntos -= 3

    #El licuado de col rizada tiene castañas de cajú.
    if verificar_existe(ind, POS_VEGETAL, VEGETALES.COL_RIZADA, POS_NUEZ, NUECES.CAJU):
        puntos -= 3

    return puntos

def funcion_puntaje(ind):
    puntos = 0
    puntos += calcular_condiciones_a_cumplir(ind)
    puntos += calcular_restricciones(ind)

    return [puntos]