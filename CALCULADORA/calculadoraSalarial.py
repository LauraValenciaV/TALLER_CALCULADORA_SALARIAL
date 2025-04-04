import sys
import os
from tabulate import tabulate
from datetime import datetime
import pickle
from colorama import Fore, Style, Back, init
init()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from BIBLIOTECA import libreria

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
    #Por temas de practicidad para probar una y otra vez elprograma voy a comentar esta validación para que se sobre escriba la informacion en el archivo de nomina y generarla cuantas veces necesite para revisar mi programa
    '''try: # Verificar si la nómina de ese mes ya existe
        with open(archivo_nomina, "rb") as file:
            print(Fore.YELLOW + f"⚠ La nómina del mes {mes_actual}-{año_actual} ya fue generada." + Style.RESET_ALL)
            return
    except FileNotFoundError:
        pass''' # Si el archivo no existe, se continúa normalmente
    # Generar la nómina para todos los empleados
    nomina = []
    for empleado in empleados:
        codigo, nombre, cedula, _, _, _, salario_basico_mensual = empleado  # Extrae los datos que necesito del empleado
        dias_laborados = 30  # Inicialmente, asumimos que trabajó todo el mes
        salario_diario = round(salario_basico_mensual / 30, 2)
        salario_devengado = round(salario_diario * dias_laborados, 2)
        auxilio_transporte = round(calcular_auxilio_transporte(salario_basico_mensual), 2)
        descuento_salud = round(calcular_descuento_salud(salario_devengado, DESCUENTO_SALUD), 2)
        descuento_pension = round(calcular_descuento_pension(salario_devengado, DESCUENTO_PENSION), 2)
        salario_neto = round(salario_devengado + auxilio_transporte - (descuento_salud + descuento_pension), 2)
        # Guardar los datos de nomina de cada empleado en la lista de listas
        nomina.append([codigo, nombre, cedula, salario_basico_mensual, dias_laborados, salario_devengado, auxilio_transporte, descuento_salud, descuento_pension, salario_neto])
        # Guardar la nómina en archivo binario
    libreria.guardar(nomina, archivo_nomina)
    print(Fore.GREEN + f"\n✔ Nómina generada y guardada en {archivo_nomina}." + Style.RESET_ALL)


# FUNCION PARA ACTUALIZAR LOS DIAS LABORADOS DE UN EMPLEADO EN CASO DE ALGUNA NOVEDAD (PARA QUE EL CALCULO DE SU NOMINA QUEDE CORRECTAMENTE, DADO QUE INICIALMENTE SE ASUME QUE LABORO LOS 30 DÍAS SIN FALTA)
def actualizar_dias_laborados():
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.strftime("%m")
    año_actual = fecha_actual.strftime("%Y")
    # Abro el archivo de nomina del mes y año actual (solo puedo corregir la nomina del mes actual)
    archivo_nomina = f"NOMINA/nomina_{año_actual}_{mes_actual}.dat"
    # Cargar la nómina existente
    nomina = libreria.cargar(archivo_nomina)
    # Si la nómina está vacía, significa que no existe un archivo con datos
    if not nomina:
        print(Fore.RED + "⚠ No existe una nómina generada para este mes." + Style.RESET_ALL)
        return
    # Solicitamos la cédula del empleado a quien le vamos a generar la novedad
    cedula_empleado = input("Ingrese la cédula del empleado para actualizar días laborados: ")
    # Creamos la variable de encontrado por si no hay un empleado con esa cédula podamos hacer la notificación
    encontrado = False
    for empleado in nomina:
        if empleado[2] == cedula_empleado:  # La cédula está en la posición 2
            encontrado = True
            nuevos_dias = libreria.validador_dias_laborados(input("Ingrese los nuevos días laborados: "))
            # Recalcular salario devengado con los nuevos días laborados
            salario_basico = empleado[3]  # Salario básico en la posición 3
            salario_diario = salario_basico / 30
            salario_devengado = salario_diario * nuevos_dias
            # Actualizar la nómina con los nuevos valores
            empleado[4] = nuevos_dias  # Posición 4: Días trabajados
            empleado[5] = salario_devengado  # Posición 5: Salario devengado
            print(Fore.GREEN + "✔ Días laborados actualizados correctamente." + Style.RESET_ALL)
            break
    if not encontrado:
        print(Fore.RED + "⚠ No se encontró un empleado con esa cédula." + Style.RESET_ALL)
        return
    # Guardar los cambios en el archivo binario usando la función de la librería
    libreria.guardar(nomina, archivo_nomina)
    print(Fore.GREEN + "✔ Nómina actualizada correctamente." + Style.RESET_ALL)


#FUNCION PARA CONSULTAR LA NOMINA DE UN EMPLEADO EN UNA FECHA ESPECIFICA
def consultar_nomina_por_empleado_y_por_fecha():
    # Pedir al usuario que ingrese la cédula del empleado que desea consultar
    cedula_buscar = input("Ingrese la cédula del empleado que desea consultar: ")
    # Pedir al usuario que ingrese la fecha deseada (en formato YYYY-MM-DD)
    fecha_buscar_input = input("Ingrese la fecha de la nomina que desea visualizar y use el formato YYYY-MM-DD (ejemplo: 2025-03-31): ")
    try:
        # Convertir la fecha ingresada a un objeto datetime
        fecha_buscar = datetime.strptime(fecha_buscar_input, "%Y-%m-%d")
    except ValueError:
        print(Fore.RED + "⚠ Formato de fecha incorrecto. Asegúrese de usar el formato YYYY-MM-DD." + Style.RESET_ALL)
        return
    # Obtener el nombre del archivo correspondiente a esa fecha
    archivo_nomina = f"NOMINA/nomina_{fecha_buscar.strftime('%Y_%m')}.dat"
    # Usar la función cargar para obtener los datos de la nómina desde el archivo
    nomina = libreria.cargar(archivo_nomina)
    # Si la nómina está vacía, no se pudo cargar el archivo correctamente
    if not nomina:
        print(Fore.RED + "⚠ No se pudieron cargar los datos de la nómina." + Style.RESET_ALL)
        return
    # Encabezados de la tabla
    headers = ["Código", "Nombre", "Cédula", "Salario Básico", "Días Laborados", "Salario Devengado", 
               "Auxilio Transporte", "Descuento Salud", "Descuento Pensión", "Salario Neto"]
    # Buscar al empleado en la nómina por cédula
    for empleado in nomina:
        if empleado[2] == cedula_buscar:  
            # Mostrar la tabla con la información del empleado encontrado
            data = [empleado]  
            print(tabulate(data, headers=headers, tablefmt="pretty"))
            break
    else:
        print(Fore.RED + "⚠ No se encontró un empleado con esa cédula en la nómina." + Style.RESET_ALL)


#FUNCION PARA LISTAR LA NOMINA DE TODOS LOS EMPLEADOS EN UNA FECHA ESPECIFICA
def consultar_nominas_por_fecha():
    # Pedir al usuario que ingrese fecha de la que quiere listar la nomina de todos los empleados
    fecha_buscar_input = input("Ingrese la fecha de la nomina que desea visualizar y use el formato YYYY-MM-DD (ejemplo: 2025-03-31): ")
    try:
        # Convertir la fecha ingresada a un objeto datetime
        fecha_buscar = datetime.strptime(fecha_buscar_input, "%Y-%m-%d")
    except ValueError:
        print(Fore.RED + "⚠ Formato de fecha incorrecto. Asegúrese de usar el formato YYYY-MM-DD." + Style.RESET_ALL)
        return
    # Obtener el nombre del archivo correspondiente a esa fecha
    archivo_nomina = f"NOMINA/nomina_{fecha_buscar.strftime('%Y_%m')}.dat"
    # Usar la función cargar para obtener los datos de la nómina desde el archivo
    nomina = libreria.cargar(archivo_nomina)
    # Si la nómina está vacía, no se pudo cargar el archivo correctamente
    if not nomina:
        print(Fore.RED + "⚠ No se pudieron cargar los datos de la nómina." + Style.RESET_ALL)
        return
    print(Fore.RED + "*** LISTADO DE NOMINA ***" + Style.RESET_ALL)
    print(tabulate(nomina, headers=["Código", "Nombre", "Cédula", "Salario Básico", "Días Laborados", "Salario Devengado", "Auxilio Transporte", "Descuento Salud", "Descuento Pensión", "Salario Neto"], tablefmt="grid"))
          

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
            generar_nomina_del_mes()
        case "2":
            actualizar_dias_laborados()
        case "3":
            consultar_nomina_por_empleado_y_por_fecha()
        case "4":
            consultar_nominas_por_fecha()
        #case "5":
        case "6":
            print(Fore.YELLOW + "*** SALE DEL PROGRAMA ***" + Style.RESET_ALL)
            break
        case _:
            print(Fore.RED + "⚠ Opción no valida." + Style.RESET_ALL)
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