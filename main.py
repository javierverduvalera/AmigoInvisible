import random

import Correo as c
import PySimpleGUI as sg
if __name__ == '__main__':



    diccionario = {}
    lista = []
    cont = 0
    cont2 = 1
    repetir = True  # variable de control de los bucles
    repertir2 = True
    CorreosEnviados = []

    layoutNumeroParticipantes = [
        [sg.Text('¿Cuantas personas van a participar?'), sg.InputText(key='parcitipantes')],
        [sg.Button('Aceptar')], [sg.Button('Salir')],
    ]

    layoutERRORNumeroParticipantes = [[sg.Text('Valor no valido para el numero de participantes')]]

    layoutIntroduceCorreo = [
        [sg.Text('Introduce tu correo'), sg.InputText(key='correo')],
        [sg.Button('Aceptar')]
    ]

    layoutExito = [
        [sg.Text('Todo ha salido bien, id a revisad vuestro correo')],
        [sg.Button('Salir')],
    ]

    ventana1 = sg.Window('Introduce el Numero de participantes', layoutNumeroParticipantes, margins=(10, 10))
    while repetir:
        event, values = ventana1.read()
        if event == 'Aceptar' and len(values['parcitipantes']) >= 1:
            participantes = values['parcitipantes']
            repetir = False
        if event == 'Salir' or event == sg.WIN_CLOSED:
            exit(1)
    ventana1.close()
    repetir = True

    try:
        assert int(participantes) > 1
        for i in range(int(participantes)):
            layoutInsertarParticipantes = [
                [sg.Text('Nombre'), sg.InputText(key="nombre")],
                [sg.Button('Aceptar')],
            ]

            layoutOperacionCancelada = [[sg.Text("Operacion cancelada"), sg.Button('OK')]]
            ventana2 = sg.Window("Introduce el participante nº" + str(i + 1), layoutInsertarParticipantes,
                                 margins=(15, 10))

            while repetir:
                event, values = ventana2.read()
                if event == 'Aceptar' and len(values['nombre']) >= 1:
                    if values['nombre'] in diccionario.keys():
                        layoutNombreRepetido = [[sg.Text('Este participante ya ha sido introducido antes')]]
                        ventanaERROR = sg.Window('Participante repetido', layoutNombreRepetido, margins=(100, 30))
                        ventanaERROR.read()
                        ventanaERROR.close()
                    else:
                        diccionario[values['nombre']] = {}
                        lista.append(values['nombre'])
                        repetir = False
                if event == sg.WIN_CLOSED:
                    ventana2.close()
                    ventanaERROR = sg.Window('Operacion cancelada', layoutOperacionCancelada, margins=(100, 30))
                    event, values = ventanaERROR.read()

                    exit(3)

            ventana2.close()
            repetir = True

    except Exception as e:
        print(e)
        ventanaERROR = sg.Window('Error al introducir el numero de particiantes', layoutERRORNumeroParticipantes,
                                 margins=(100, 10))
        event, values = ventanaERROR.read()
        exit(2)

    '''
    Asignacion de regalos
    '''
    for i in diccionario.keys():

        regalado = random.randint(0, len(lista) - 1)

        while i == lista[regalado] and cont < 30:
            cont = cont + 1
            # print('hemos cambiado ' + str(cont) + ' veces')
            regalado = random.randint(0, len(lista) - 1)

        diccionario[i] = lista[regalado]
        lista.pop(regalado)

        if cont == 30:
            # print('cambiamos a quien le regalan el primero y el ultimo')
            contenidocambio = diccionario[i]
            diccionario[i] = diccionario[cambio]
            diccionario[cambio] = contenidocambio

        cambio = i
        cont = 0

    '''
    Correos
    '''
    for i in diccionario.keys():
        repetir = True
        texto = '¡Enhorabuena! ' + i + ' te ha tocado regalarle a ' + diccionario[i]
        while (repetir):

            layoutIntroduceCorreo = [
                [sg.Text('Introduce tu correo'), sg.InputText(key='correo')],
                [sg.Button('Aceptar')]
            ]
            layoutConfirmacionCancelar = [
                [sg.Text('¿Estas seguro de que quieres cancelar?')],
                [sg.Button('Si')], [sg.Button('NO')],
            ]

            ventana3 = sg.Window(i + ' Introduce tu correo', layoutIntroduceCorreo, margins=(100, 10))

            event, values = ventana3.read()

            if event == 'Aceptar':
                destinatario = values['correo']
                destinatario = destinatario.strip()
                ventana3.close()
                try:
                    c.mandar_correo(texto, "4mig0invisible.bot@gmail.com", "nmlximwqjxwoiwkx", destinatario,
                                    "amigo invisible")
                    CorreosEnviados.append(destinatario)
                    repetir = False

                except Exception as e:
                    print(e)
                    layoutERRORCorreo = [[sg.Text('No se ha podido enviar el correo a esa direccion, vuelve a probar')],
                                         [sg.Button('OK')]]
                    ventanaERROR = sg.Window('No se pudo enviar el correo a ' + i, layoutERRORCorreo, margins=(100, 10))
                    event, values = ventanaERROR.read()
                    ventanaERROR.close()

            if event == sg.WIN_CLOSED:
                ventana3.close()
                ventanaConfirmacion = sg.Window('¿Quieres cancelar la operacion?', layoutConfirmacionCancelar,
                                                margins=(100, 30))
                event, values = ventanaConfirmacion.read()

                if event == "Si":
                    ventanaConfirmacion.close()
                    repetir = False
                    ventanaERROR = sg.Window('Operacion cancelada', layoutOperacionCancelada, margins=(100, 30))
                    event, values = ventanaERROR.read()
                    ventanaERROR.close()

                    for direcciones in CorreosEnviados:
                        c.mandar_correo("Lo siento, el amigo invisible ha sido cancelado ;("
                                        , "4mig0invisible.bot@gmail.com", "nmlximwqjxwoiwkx", direcciones,
                                        "amigo invisible")
                    exit(4)

                ventanaConfirmacion.close()

            # print("correo de " + i + " enviado")
            # print("Error al mandar el correo")

    """
    codigos de error:

    1: Ventana nº participantes cerrada
    2: Numero de participantes no validos
    3: Operacion cancelada en la etapa de introduccion de los participantes
    4: Operacion cancelada en la etapa de obtener los correos

    """
    ventanaEXITO = sg.Window('Todo ha salido correctamente', layoutExito, margins=(10, 10))
    event, values = ventanaEXITO.read()



