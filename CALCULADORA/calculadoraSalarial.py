import sys
import os
from tabulate import tabulate
from datetime import datetime
from colorama import Fore, Style, Back, init
init()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from BIBLIOTECA import libreria


libreria.cabecera("CALCULADORA SALARIAL")

#CONSTANTES
SALARIO_MINIMO = 1423500  
DESCUENTO_SALUD = 0.04
DESCUENTO_PENSION = 0.04
AUXILIO_DE_TRANSPORTE = 200000

#FUNCIONES DE CÁLCULO
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

#FUNCIÓN PARA GENERAR LA NÓMINA DEL MES DE TODOS LOS EMPLEADOS
def generar_nomina_del_mes():
    empleados = libreria.cargar("EMPLEADOS/empleados.dat")
    if not empleados:
        print(Fore.RED + "No hay empleados registrados. Registre empleados primero." + Style.RESET_ALL)
        return
     # Obtener fecha actual para identificar el mes y el año
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.strftime("%m")
    año_actual = fecha_actual.strftime("%Y")
    # Definir el archivo donde se guardará la nómina del mes
    archivo_nomina = f"NOMINA/nomina_{año_actual}_{mes_actual}.dat"
    try: # Verificar si la nómina de ese mes ya existe
        with open(archivo_nomina, "rb") as file:
            print(Fore.YELLOW + f"⚠ La nómina del mes {mes_actual}-{año_actual} ya fue generada." + Style.RESET_ALL)
            return
    except FileNotFoundError:
        pass # Si el archivo no existe, se continúa normalmente
    # Generar la nómina para todos los empleados
    nomina = []
    for empleado in empleados:
        codigo, nombre, cedula, _, _, _, salario_basico_mensual = empleado  # Extrae los datos que necesito del empleado
        dias_laborados = 30  # Inicialmente, asumimos que trabajó todo el mes
        salario_diario = salario_basico_mensual / 30
        salario_devengado = salario_diario * dias_laborados
        auxilio_transporte = calcular_auxilio_transporte(salario_basico_mensual)
        descuento_salud = calcular_descuento_salud(salario_devengado, DESCUENTO_SALUD)
        descuento_pension = calcular_descuento_pension(salario_devengado, DESCUENTO_PENSION)
        salario_neto = salario_devengado + auxilio_transporte - (descuento_salud + descuento_pension)
        # Guardar los datos de nomina de cada empleado en la lista de listas
        nomina.append([codigo, nombre, cedula, salario_basico_mensual, dias_laborados, salario_devengado, auxilio_transporte, descuento_salud, descuento_pension, salario_neto])
        # Guardar la nómina en archivo binario
        libreria.guardar(nomina, archivo_nomina)
        print(Fore.GREEN + f"\n✔ Nómina generada y guardada en {archivo_nomina}." + Style.RESET_ALL)

# FUNCION PARA ACTUALIZAR LOS DIAS LABORADOS DE UN EMPLEADO EN CASO DE ALGUNA NOVEDAD (PARA QUE EL CALCULO DE SU NOMINA QUEDE CORRECTAMENTE, DADO QUE INICIALMENTE SE ASUME QUE LABORO LOS 30 DÍAS SIN FALTA)



def menu_calculadora_salarial():
    # Formatear el título como tabla con una sola fila
    titulo_tabla = [[Fore.YELLOW + "CALCULADORA SALARIAL" + Style.RESET_ALL]]
    print(tabulate(titulo_tabla, tablefmt="grid", colalign=["center"]))
    # Formatear las opciones del menú
    opciones_tabla = [
        [Back.YELLOW + "[1]" + Style.RESET_ALL, "Generar nómina del mes"],
        [Back.YELLOW + "[2]" + Style.RESET_ALL, "Actualizar los días laborados de un empleado"],
        [Back.YELLOW + "[3]" + Style.RESET_ALL, "Consultar nómina de un empleado en una fecha especifica"],
        [Back.YELLOW + "[4]" + Style.RESET_ALL, "Consultar nómina de todos los empleados en una fecha especifica"],
        [Back.YELLOW + "[5]" + Style.RESET_ALL, "Generar reportes"],
        [Back.YELLOW + "[6]" + Style.RESET_ALL, "Regresar al menú anterior"]
    ]
    # Imprimir la tabla de opciones
    print(tabulate(opciones_tabla, tablefmt="grid", colalign=["center", "left"]))


# INICIO DEL PROGRAMA
while True:
    menu_calculadora_salarial()
    opcion = input("Ingrese la opción que desea: ")
    match opcion:
        case "1":
        case "2":
        case "3":
        case "4":
        case "5":
        case "6":
            print(Fore.RED + "*** SALE DEL PROGRAMA ***" + Style.RESET_ALL)
            break
        case _:
            print(Fore.YELLOW + "⚠ Opción no valida." + Style.RESET_ALL)
            continue



#ASI HABIA COMENZADO EL PROGRAMA ANTERIORMENTE
'''
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
'''