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

#MENU PARA ACTUALIZAR DATOS DEL EMPLEADO
def menu_actualizar(titulo):
    # Formatear el título como tabla con una sola fila
    titulo_tabla = [[Fore.YELLOW + titulo + Style.RESET_ALL]]
    print(tabulate(titulo_tabla, tablefmt="grid", colalign=["center"]))
    # Formatear las opciones del menú
    opciones_tabla = [
        [Back.YELLOW + "[1]" + Style.RESET_ALL, "Nombre del empleado"],
        [Back.YELLOW + "[2]" + Style.RESET_ALL, "Cédula"],
        [Back.YELLOW + "[3]" + Style.RESET_ALL, "Fecha de nacimiento"],
        [Back.YELLOW + "[4]" + Style.RESET_ALL, "Telefono"],
        [Back.YELLOW + "[5]" + Style.RESET_ALL, "Correo electronico"],
        [Back.YELLOW + "[6]" + Style.RESET_ALL, "Salario basico mensual"],
        [Back.YELLOW + "[7]" + Style.RESET_ALL, "Regresar al menú anterior"]
    ]
    # Imprimir la tabla de opciones
    print(tabulate(opciones_tabla, tablefmt="grid", colalign=["center", "left"]))

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
                
empleados = libreria.cargar(ARCHIVO_EMPLEADOS)


#INICIO DEL PROGRAMA   
while True:
    libreria.menu_crud("BASE DE DATOS DE EMPLEADOS")
    opcion = input("Ingrese la opción que desea: ")
    match opcion:
        case "1":
            ingresar_empleado()   
        case "2":
            if not empleados:
                print(Fore.YELLOW + "⚠ No hay empleados registrados." + Style.RESET_ALL) 
            else:
                print(Fore.RED + "*** LISTADO DE EMPLEADOS ***" + Style.RESET_ALL)
                print(tabulate(empleados, headers=["Código", "Nombre", "Cédula", "Fecha Nac.", "Teléfono", "Correo", "Salario"], tablefmt="grid")) 
        case "3":
            if not empleados:
                print(Fore.YELLOW + "⚠ No hay empleados registrados, no es posible consultar." + Style.RESET_ALL) 
            else:
                consultar_empleado = input("Ingrese la cédula del empleado a consultar: ")
                encontrado = False  # Variable para saber si encontramos el empleado
                for empleado in empleados:
                    if empleado[2] == consultar_empleado:
                        print(Fore.RED + "*** INFORMACIÓN DEL EMPLEADO ***" + Style.RESET_ALL)
                        print(tabulate([empleado], headers=["Código", "Nombre", "Cédula", "Fecha Nac.", "Teléfono", "Correo", "Salario"], tablefmt="grid"))
                        encontrado = True
                        break  # Detenemos la búsqueda porque ya lo encontramos
                if not encontrado:
                    print(Fore.YELLOW + "⚠ No se encontró un empleado con esa cédula." + Style.RESET_ALL)
        case "4":
            if not empleados:
                print(Fore.YELLOW + "⚠ No hay empleados registrados, no es posible actualizar." + Style.RESET_ALL)
            else:
                consultar_empleado = input("Ingrese la cédula del empleado a actualizar: ")
                encontrado = False
                for i, empleado in enumerate(empleados):
                    if empleado[2] == consultar_empleado:
                        encontrado = True
                        while True:
                            menu_actualizar("ACTUALIZAR INFORMACIÓN DE EMPLEADO")
                            opcion_actualizar = input("Seleccione el dato a modificar: ")
                            match opcion_actualizar:
                                case "1":
                                    empleados[i][1] = libreria.validador_nombre(input("Ingrese el nuevo nombre: "))
                                case "2":
                                    empleados[i][2] = libreria.validador_cedula(input("Ingrese la nueva cédula: "))
                                case "3":
                                    empleados[i][3] = libreria.validador_fecha_nacimiento(input("Ingrese la nueva fecha de nacimiento: "))
                                case "4":
                                    empleados[i][4] = libreria.validador_contacto_telefonico(input("Ingrese el nuevo teléfono: "))
                                case "5":
                                    empleados[i][5] = libreria.validador_email(input("Ingrese el nuevo correo electrónico: "))
                                case "6":
                                    empleados[i][6] = libreria.validador_salario(input("Ingrese el nuevo salario: "))
                                case "7":
                                    print(Fore.YELLOW + "🔙 Volviendo al menú principal..." + Style.RESET_ALL)
                                    break
                                case _:
                                    print(Fore.RED + "⚠ Opción no válida, intente nuevamente." + Style.RESET_ALL)
                        # Guardar cambios en el archivo
                        libreria.guardar(empleados, ARCHIVO_EMPLEADOS)
                        print(Fore.GREEN + "✅ Información actualizada correctamente." + Style.RESET_ALL)
                        break  # Salimos del `for` porque ya encontramos el empleado
                if not encontrado:
                    print(Fore.YELLOW + "⚠ No se encontró un empleado con esa cédula." + Style.RESET_ALL)
        #case "5":
        #case "6":
            
        


