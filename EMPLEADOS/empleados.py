import pickle
import sys
import os
from tabulate import tabulate
from colorama import Fore, Style, Back, init
init()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from BIBLIOTECA import libreria

ARCHIVO_EMPLEADOS = "EMPLEADOS/empleados.dat"

libreria.cabecera("EMPLEADOS")

#ESTRUCTURA DE DATOS A UTILIZAR
empleados = []

def ingresar_empleado():
    while True:
        print(Fore.RED + "*** REGISTRO DE EMPLEADO ***" + Style.RESET_ALL)
        nombre_del_empleado = libreria.validador_nombre(input("Ingrese el nombre del empleado: "))
        cedula = libreria.validador_cedula(input("Ingrese el documento de identidad: "))
        fecha_nacimiento = libreria.validador_fecha_nacimiento(input("Ingrese la fecha de nacimiento (YYYY-MM-DD): "))
        telefono = libreria.validador_contacto_telefonico(input("Ingrese contacto telefónico: "))
        correo_electronico = libreria.validador_email(input("Ingrese el correo electronico: "))
        salario_basico_mensual = libreria.validador_salario(input("Ingrese el salario mensual: "))

        # Buscar si el empleado ya existe en la lista
        indice_empleado = libreria.buscar(empleados, cedula, indice=2)
   
        if indice_empleado == -1:  # Si no existe, se registra
            codigo_empleado = "EMP" + str(len(empleados) + 1).zfill(4)  # Genera códigos como EMP0001, EMP0002...
            empleado = [codigo_empleado, nombre_del_empleado, cedula, fecha_nacimiento, telefono, correo_electronico, salario_basico_mensual]
            empleados.append(empleado)  # Agregar el nuevo empleado a la lista
            libreria.guardar(empleados, ARCHIVO_EMPLEADOS)
            print(Fore.GREEN + "✅ Empleado registrado correctamente." + Style.RESET_ALL)
            return empleado
        else:
            print(Fore.RED + "❌ Error: El empleado con esta cédula ya está registrado." + Style.RESET_ALL)
                
listado_empleados = libreria.cargar(empleados, ARCHIVO_EMPLEADOS)


#INICIO DEL PROGRAMA   
while True:
    libreria.menu_crud("BASE DE DATOS DE EMPLEADOS")
    opcion = input("Ingrese la opción que desea: ")
    match opcion:
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
        case 6:
        


