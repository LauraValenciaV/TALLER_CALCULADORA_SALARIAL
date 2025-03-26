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

def ingresar_empleado():
    print(Fore.RED + "*** REGISTRO DE EMPLEADO ***" + Style.RESET_ALL)
    nombre_del_empleado = libreria.validador_nombre(input("Ingrese el nombre del empleado: "))
    cedula = libreria.validor_cedula(input("Ingrese el documento de identidad: "))
    fecha_nacimiento = libreria.validador_fecha_nacimiento(input("Ingrese la fecha de nacimiento (YYYY-MM-DD): "))
    telefono = libreria.validador_contacto_telefonico(input("Ingrese contacto telefónico: "))
    correo_electronico = 
    salario_basico_mensual = libreria.validador_salario(input("Ingrese el salario mensual: "))
