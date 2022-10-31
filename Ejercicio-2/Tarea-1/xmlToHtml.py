import xml.etree.ElementTree as ET

def xml2html(xml, file_o):
    text = '''
        <!DOCTYPE HTML>

    <html lang="es">
    <head>
        <!-- Datos que describen el documento -->
        <meta charset="UTF-8" />

        <!--Metadatos de los documentos HTML5-->
        <meta name ="author" content = 'Ana Fernandez Ostio, UO275780' />
        <meta name ="description" content = 'Red Social de Ana Fernandez' />
        <meta name ="keywords" content ='red social, xml, ana fernandez' />

        <!--Definición de la ventana gráfica-->
        <meta name ="viewport" content ="width=device-width, initial-scale=1.0" />

        <title>RED SOCIAL</title>

        <!-- añadir el elemento link de enlace a la hoja de estilo dentro del <head> del documento html -->
        <link rel="stylesheet" type="text/css" href="estilo.css" />
    </head>

    
    <body>
        <header>
            <h1>RED SOCIAL</h1>
        </header>
    '''
    

    try:
        arbol = ET.parse(xml)
    except ET.ParseError:
        print("Se ha producido un error procesando el archivo xml")
        exit()

    raiz = arbol.getroot()

    text += getInformacion(raiz)

    for amigo in raiz.findall(".//"):
        if(amigo.tag == 'persona'):
            text += getInformacion(amigo)

    text += "\t</body>\n</html>" 
    
    with open(file_o, 'w', encoding = 'utf-8') as f:
        f.write(text )
    print('Cambio realizado')
    exit()


def getInformacion(persona):
    nombreP = persona.attrib.get("nombre")
    texto = "\t\t<section>\n" 
    texto += "\t\t\t\t<h2>" + persona.attrib.get("nombre") + " " + persona.attrib.get("apellidos")  + "</h2> \n"
    texto += "\t\t\t\t<p>A continuación se muestra informacion de la persona: </p>\n"
    texto += "\t\t\t<ul>\n"
    for i in persona.findall('datos'):
        texto += getNacimiento(i)
        texto += getResidencia(i)
        texto += "\t\t\t\t<li>Comentario: " + i.find('comentario').text + "</li>\n"
        texto += "\t\t\t</ul>\n"        
        texto += "\t\t\t\t<p>Imagenes de la persona</p>\n"
        texto += getFotos(i, nombreP)
        texto += "\t\t\t\t<p>Videos de la persona</p>\n"
        texto += getVideos(i)
        

    texto += "\t\t</section>\n"
    return texto


def getVideos(datosP):
    texto = ""
    for f in datosP.findall('video'):
        texto += "\t\t\t\t<video src = '" + f.text  + "' controls></video>\n" 
    return texto

def getFotos(datosP, nombreP):
    texto = ""
    for f in datosP.findall('foto'):
        texto += "\t\t\t\t<img src = '" + f.text  + "' alt= 'Imagen de " + nombreP +  "'/>\n"
    return texto

def getResidencia(datoP):
    texto = ""
    for h in datoP.findall('residencia'):
        texto += "\t\t\t\t<li>Reside en: " + h.find('lugar').text
        texto += " en coordenadas, " + getCoords(h) + "</li>\n"
    
    return texto

def getNacimiento(datoP):
    texto = ""
    for h in datoP.findall('nacimiento'):
        texto += "\t\t\t\t<li>Nacido en: " + h.find('lugar').text
        texto += " en coordenadas, " + getCoords(h)
        texto += "el " + h.find('fecha').text + "</li>\n"
    
    return texto

def getCoords(tipo):
    cad = "("
    for t in tipo.findall('coord'): 
       cad += t.find('longitud').text + ", " + t.find('latitud').text + ", " +  t.find('altitud').text + ") "
    return cad

def checkExist(xml, f_out):
    # MEtodo que comprueuba si existe el archivo
    try:
        with open(xml, 'r') as f:
            xml2html(xml, f_out);
            return True
    except FileNotFoundError:
        print('No se ha encontrado el archivo, vuelva a intentarlo')
        main();

def main():
    """Metodo que pide por consola el fichero e intenta ejecutar el codigo"""
    f_xml = input("Nombre del fichero XML: ")
    f_html = input('Nombre del fichero HTML donde se quiere guardar la informacion: ')

    # Comprobamos que existe el fichero, si no existe se vuelve a pedir
    checkExist(f_xml, f_html)

if __name__ == '__main__':
    main()