import os
import time
from tabulate import tabulate
from datetime import datetime
from colorama import Fore, Style, Back, init
init()

#FUNCION PARA AGREGAR TITULO AL PROGRAMA
def cabecera(titulo): 
     print(Fore.YELLOW + f"{titulo}" + Style.RESET_ALL)

#FUNCION PARA ASEGURAR QUE INGRESE CORRECTAMENTE EL NOMBRE
def validador_nombre(nombre_del_empleado):
    nombre_valido = nombre_del_empleado.strip()
    while nombre_valido.replace(" ", "").isalpha() == False:
        print(Fore.RED + "❌Error: Ingrese un nombre válido (solo letras)." + Style.RESET_ALL, end="", flush=True)
        time.sleep(3)
        print("\r\033[K", end="")  # Borra el mensaje de error
        print("\033[F\033[K", end="")  # Borra la línea anterior también
        nombre_valido = input("Ingrese nuevamente el nombre del empleado: ").strip()
    return nombre_valido.title()

#FUNCION PARA ASEGURAR QUE SE INGRESE CORRECTAMENTE EL SALARIO
def validador_salario(salario_basico_mensual):
    salario_valido = salario_basico_mensual.strip()
    while not salario_valido.isdigit() or int(salario_valido) < 0 or int(salario_valido) >= 8000000:
        print(Fore.RED + f"❌Error: Ingrese un salario válido: " + Style.RESET_ALL, end="", flush=True)
        time.sleep(3)
        print("\r\033[K", end="")  # Borra el mensaje de error
        print("\033[F\033[K", end="")  # Borra la línea anterior también
        salario_valido = input("Ingrese nuevamente el salario: ").strip()
    return int(salario_valido)

#FUNCION PARA ASEGURAR QUE SE INGRESE CORRECTAMENTE LOS DIAS LABORADOS
def validador_dias_laborados(dias_trabajados_en_el_mes):
    dias_validos = dias_trabajados_en_el_mes.strip()
    while not dias_validos.isdigit() or int(dias_validos) > 30 or int(dias_validos) < 1:
        print(Fore.RED + "❌Error: Ingrese un número entre 1 y 30." + Style.RESET_ALL, end="", flush=True)
        time.sleep(3)
        print("\r\033[K", end="")  # Borra el mensaje de error
        print("\033[F\033[K", end="")  # Borra la línea anterior también
        dias_validos = input("Ingrese nuevamente los días laborados: ").strip()
    return int(dias_validos)

#FUNCION PARA VALIDAR SI EL USUARIO DESEA CONTINUAR USANDO EL SISTEMA O NO
def validador_respuesta(respuesta):
    respuesta_valida = respuesta.strip().capitalize()
    while not respuesta_valida in ("Si", "No"):
        print(Fore.RED + "❌Error: Ingrese solo (Si o No)" + Style.RESET_ALL, end="", flush=True)
        time.sleep(3)
        print("\r\033[K", end="")  # Borra el mensaje de error
        print("\033[F\033[K", end="")  # Borra la línea anterior también
        respuesta_valida = input("Desea continuar en el programa? ").strip().capitalize()
    return(respuesta_valida)

#FUNCION PARA VALIDAR SI EL USUARIO INGRESA LA CEDULA CORRECTAMENTE
def validador_cedula(cedula):  
    cedula_valida = cedula.strip()
    while not (cedula_valida.isdigit() and 6 <= len(cedula_valida) <= 10):
        print(Fore.RED + "❌ Error: Ingrese solo números (6-10 dígitos)." + Style.RESET_ALL, end="", flush=True)
        time.sleep(3)
        print("\r\033[K", end="")  
        print("\033[F\033[K", end="")  
        cedula_valida = input("Ingrese nuevamente el documento de identidad: ").strip()
    return cedula_valida

#FUNCION PARA VALIDAR 