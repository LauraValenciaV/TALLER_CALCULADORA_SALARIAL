import os
import time
import pickle
import re
from tabulate import tabulate
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
        time.sleep(2)
        print("\r\033[K", end="")  # Borra el mensaje de error
        print("\033[F\033[K", end="")  # Borra la línea anterior también
        nombre_valido = input("Ingrese nuevamente el nombre del empleado: ").strip()
    return nombre_valido.title()

#FUNCION PARA ASEGURAR QUE SE INGRESE CORRECTAMENTE EL SALARIO
def validador_salario(salario_basico_mensual):
    salario_valido = salario_basico_mensual.strip()
    while not salario_valido.isdigit() or int(salario_valido) < 0 or int(salario_valido) >= 8000000:
        print(Fore.RED + f"❌Error: Ingrese un salario válido: " + Style.RESET_ALL, end="", flush=True)
        time.sleep(2)
        print("\r\033[K", end="")  # Borra el mensaje de error
        print("\033[F\033[K", end="")  # Borra la línea anterior también
        salario_valido = input("Ingrese nuevamente el salario: ").strip()
    return int(salario_valido)

#FUNCION PARA ASEGURAR QUE SE INGRESE CORRECTAMENTE LOS DIAS LABORADOS
def validador_dias_laborados(dias_trabajados_en_el_mes):
    dias_validos = dias_trabajados_en_el_mes.strip()
    while not dias_validos.isdigit() or int(dias_validos) > 30 or int(dias_validos) < 1:
        print(Fore.RED + "❌Error: Ingrese un número entre 1 y 30." + Style.RESET_ALL, end="", flush=True)
        time.sleep(2)
        print("\r\033[K", end="")  # Borra el mensaje de error
        print("\033[F\033[K", end="")  # Borra la línea anterior también
        dias_validos = input("Ingrese nuevamente los días laborados: ").strip()
    return int(dias_validos)

#FUNCION PARA VALIDAR SI EL USUARIO DESEA CONTINUAR USANDO EL SISTEMA O NO
def validador_respuesta(respuesta):
    respuesta_valida = respuesta.strip().capitalize()
    while not respuesta_valida in ("Si", "No"):
        print(Fore.RED + "❌Error: Ingrese solo (Si o No)" + Style.RESET_ALL, end="", flush=True)
        time.sleep(2)
        print("\r\033[K", end="")  # Borra el mensaje de error
        print("\033[F\033[K", end="")  # Borra la línea anterior también
        respuesta_valida = input("Desea continuar en el programa? ").strip().capitalize()
    return(respuesta_valida)

#FUNCION PARA VALIDAR SI EL USUARIO INGRESA LA CEDULA CORRECTAMENTE
def validador_cedula(cedula):  
    cedula_valida = cedula.strip()
    while not (cedula_valida.isdigit() and 6 <= len(cedula_valida) <= 10):
        print(Fore.RED + "❌ Error: Ingrese solo números (6-10 dígitos)." + Style.RESET_ALL, end="", flush=True)
        time.sleep(2)
        print("\r\033[K", end="")  
        print("\033[F\033[K", end="")  
        cedula_valida = input("Ingrese nuevamente el documento de identidad: ").strip()
    return cedula_valida

#FUNCION PARA VALIDAR FECHA DE NACIMIENTO ASEGURANDO QUE NO SE INGRESEN FECHAS FUTURAS O QUE SEA MENOR DE EDAD
def validador_fecha_nacimiento(fecha_nacimiento):
    fecha_nacimiento_valida = fecha_nacimiento.strip()
    while True:
        try:
            fecha = datetime.strptime(fecha_nacimiento_valida, "%Y-%m-%d")
            fecha_actual = datetime.today()
            if fecha > fecha_actual:  # 🚨 Evita fechas futuras
                print(Fore.RED + "❌ Error: No debe ingresar una fecha en el futuro." + Style.RESET_ALL)
            elif relativedelta(fecha_actual, fecha).years < 18:  # 🚨 Evita menores de edad
                print(Fore.RED + "❌ Error: No debe ser menor de edad." + Style.RESET_ALL)
            else:
                return fecha  # ✅ Fecha válida
        except ValueError:
            print(Fore.RED + "❌ Error: Formato incorrecto. Use YYYY-MM-DD." + Style.RESET_ALL)
        # Pedir la fecha nuevamente si hubo error
        fecha_nacimiento_valida = input("Ingrese nuevamente la fecha de nacimiento: ").strip()

#FUNCION PARA VALIDAR QUE UN TELEFONO O CELULAR SE INGRESEN CORRECTAMENTE
def validador_contacto_telefonico(telefono):
    telefono_valido = telefono.strip()
    while True:
        # 🔹 Permitir solo números y opcionalmente un '+' al inicio
        if re.fullmatch(r"\+?\d{7,15}", telefono_valido):
            return telefono_valido  # ✅ Número válido
        # 🚨 Mensaje de error más claro
        print(Fore.RED + "❌ Error: El teléfono debe tener entre 7 y 15 dígitos y no contener letras." + Style.RESET_ALL)
        telefono_valido = input("Ingrese nuevamente el teléfono: ").strip()

#FUNCION PARA VALIDAR QUE UN CORREO ELECTRONICO ESTE BIEN ESCRITO
def validador_email(correo_electronico):
    email_valido = correo_electronico.strip()
    patron_correo = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)+$'
    while True:
        if re.match(patron_correo, email_valido):
            return email_valido
        else:
            print(Fore.RED + "❌ Error: El correo ingresado es invalido." + Style.RESET_ALL)
            email_valido = input("Ingrese nuevamente el correo electronico: ").strip()

#FUNCION PARA BUSCAR DENTRO DE UNA LISTA Y EVIDENCIAR SI EFECTIVAMENTE SE ENCUENTRA O NO (SE DEBE CONOCER EL INDICE DEL DATO A BUSCAR)
def buscar(lista, dato_a_buscar, indice=0):
    for i, registro in enumerate(lista):
        if str(registro[indice].upper()) == str(dato_a_buscar.upper()):
            return 1
    return -1

#FUNCION PARA CARGAR INFORMACION EN ARCHIVOS, MODO R DE SOLO LECTURA
def cargar(filename):
    try:
        with open(filename, 'rb') as archivo:
            lista = pickle.load(archivo)
            print(Fore.RED + f"\n>>> Cargando Información: {filename}" + Style.RESET_ALL)
            time.sleep(2)
            return lista
    except FileNotFoundError:
        print(Fore.YELLOW + f"\n>>> No se encontró el archivo {filename}, se creará uno nuevo." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n>>> Error al cargar el archivo {filename}: {e}" + Style.RESET_ALL)
    
    return []  # Devuelve una lista vacía si hay error

#FUNCION PARA GUARDAR INFORMACION DE UN EMPLEADO EN EL ARCHIVO
def guardar(lista, filename):
    with open(filename, 'wb') as archivo:  # Usa `with open` para manejar archivos de forma segura
        pickle.dump(lista, archivo)
    print(Fore.LIGHTYELLOW_EX + "\n\n>>> Guardando Información en los archivos correspondientes <<< " + Style.RESET_ALL)
    time.sleep(2)

#MENU CRUD
def menu_crud(titulo):
    # Formatear el título como tabla con una sola fila
    titulo_tabla = [[Fore.YELLOW + titulo + Style.RESET_ALL]]
    print(tabulate(titulo_tabla, tablefmt="grid", colalign=["center"]))
    # Formatear las opciones del menú
    opciones_tabla = [
        [Back.YELLOW + "[1]" + Style.RESET_ALL, "Insertar"],
        [Back.YELLOW + "[2]" + Style.RESET_ALL, "Listar"],
        [Back.YELLOW + "[3]" + Style.RESET_ALL, "Consultar"],
        [Back.YELLOW + "[4]" + Style.RESET_ALL, "Actualizar"],
        [Back.YELLOW + "[5]" + Style.RESET_ALL, "Eliminar"],
        [Back.YELLOW + "[6]" + Style.RESET_ALL, "Salir"]
    ]
    # Imprimir la tabla de opciones
    print(tabulate(opciones_tabla, tablefmt="grid", colalign=["center", "left"]))
   
