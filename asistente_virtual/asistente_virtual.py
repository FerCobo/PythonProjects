import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import os

# Opciones de voz/idioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

# escuchar nuestro micrófono y devolver el audio como texto
def transformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el micrófono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzó la grabación
        print("ya puedes hablar")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google lo que se escuche
            escuchado = r.recognize_google(audio, language="es-es")

            # prueba de que pudo ingresar
            print("Dijiste: " + escuchado)

            # devolver pedido
            return escuchado
        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendió el audio
            print("Ups, no entedí el audio")

            # devolver error
            return "sigo esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendió el audio
            print("Ups, no hay servicio")

            # devolver error
            return "sigo esperando"

        # error inesperado
        except:

            # prueba de que no comprendió el audio
            print("Ups, algo ha salido mal")

            # devolver error
            return "sigo esperando"

# función para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # pronunciar el mensaje
    engine.say(mensaje)
    engine.runAndWait()

# informar el día de la semana
def pedir_dia():

    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear una variable para el día de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombres de días
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # decir el día de la semana
    hablar(f'Hoy es {calendario[dia_semana]}. Espero que lo disfrutes')

# informar qué hora es:
def pedir_hora():

    # crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas y {hora.minute} minutos'
    print(hora)

    # decir la hora
    hablar(hora)

# función saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'

    # decir el saludo
    hablar(f"{momento}, soy Elena, tu asistente personal. Por favor, dime en qué te puedo ayudar")

# función central del asistente
def pedir_cosas():

    # activar el saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Perfecto, abrimos YouTube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro cariño, ahora mismo te abro el navegador, tu no te hernies')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando la consulta en wikipedia')
            pedido = pedido.replace('Busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1) #en sentences le indicamos el número de párrafos que queremos que lea
            hablar('Wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en ello')
            pedido = pedido.replace('Busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Estupendo, ahora reproduzco el contenido')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdón, pero no la he encontrado')
                continue

        elif 'abre la consola' in pedido:
            direccion = '"C:/Archivos de programa/Git/git-bash.exe"'
            hablar("Ahora mismo ejecuto el programa")
            os.system(direccion)
            continue

        elif 'adiós' in pedido:
            hablar("Vale, pues me voy ya, que me tienes hasta el coño")
            break

pedir_cosas()