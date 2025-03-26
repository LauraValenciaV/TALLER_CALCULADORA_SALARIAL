import sys
import os
from tabulate import tabulate
from colorama import Fore, Style, Back, init
init()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from BIBLIOTECA import libreria


libreria.cabecera("CALCULADORA SALARIAL")

SALARIO_MINIMO = 1423500  
DESCUENTO_SALUD = 0.04
DESCUENTO_PENSION = 0.04
AUXILIO_DE_TRANSPORTE = 200000

#PROCESOS
def calcular_salario_diario(salario_basico_mensual):
    return salario_basico_mensual / 30

def calcular_salario_devengado(salario_diario, dias_trabajados_en_el_mes):
    return salario_diario * dias_trabajados_en_el_mes

def calcular_auxilio_transporte(salario_basico_mensual):
    if salario_basico_mensual <= (SALARIO_MINIMO * 2):
        return AUXILIO_DE_TRANSPORTE
    else:
        return 0
    
def calcular_descuento_salud(salario_devengado, DESCUENTO_SALUD):
    return salario_devengado * DESCUENTO_SALUD

def calcular_descuento_pension(salario_devengado, DESCUENTO_PENSION):
    return salario_devengado * DESCUENTO_PENSION

def calcular_salario_neto(salario_devengado, auxilio_de_transporte, descuento_salud, descuento_pension):
    return salario_devengado + auxilio_de_transporte - ((descuento_salud) + (descuento_pension))

while (True):
    #ENTRADAS
    nombre_del_empleado = libreria.validador_nombre(input("Ingrese el nombre del empleado: "))
    salario_basico_mensual = libreria.validador_salario(input("Ingrese el salario mensual: "))
    dias_trabajados_en_el_mes = libreria.validador_dias_laborados(input("Ingrese los días laborados en el mes: "))

    salario_diario = calcular_salario_diario(salario_basico_mensual)
    salario_devengado = calcular_salario_devengado(salario_diario, dias_trabajados_en_el_mes)
    auxilio_de_transporte = calcular_auxilio_transporte(salario_basico_mensual)
    descuento_salud = calcular_descuento_salud(salario_devengado, DESCUENTO_SALUD)
    descuento_pension = calcular_descuento_pension(salario_devengado, DESCUENTO_PENSION)
    salario_neto = calcular_salario_neto(salario_devengado, auxilio_de_transporte, descuento_salud, descuento_pension)

    #SALIDAS
    nomina = [
    [Fore.GREEN + "Nombre del Empleado" + Style.RESET_ALL, nombre_del_empleado],
    [Fore.GREEN + "Salario Devengado" + Style.RESET_ALL, f"${int(salario_devengado):,}".replace(",", ".")],
    [Fore.GREEN + "Auxilio de Transporte" + Style.RESET_ALL, f"${int(auxilio_de_transporte):,}".replace(",", ".")],
    [Fore.GREEN + "Descuento Salud" + Style.RESET_ALL, f"${int(round(descuento_salud)):,}".replace(",", ".")],
    [Fore.GREEN + "Descuento Pensión" + Style.RESET_ALL, f"${int(round(descuento_pension)):,}".replace(",", ".")],
    [Fore.LIGHTGREEN_EX + "Salario Neto a Pagar" + Style.RESET_ALL, f"${int(round(salario_neto)):,}".replace(",", ".")]
    ]
    
    print(tabulate(nomina, tablefmt="grid"))

    respuesta = libreria.validador_respuesta(input("Desea ingresar más empleados (Si ó No): "))
    if (respuesta != "Si"):
        print("GRACIAS POR USAR NUESTRO SISTEMA")
        break
    continue 
