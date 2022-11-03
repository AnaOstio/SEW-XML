import xml.etree.ElementTree as ET


def XML2KML(f_xml, f_out):
    kml = '''<?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2">
        <Document>
        <Style id="residencia">
            <IconStyle>
                <color>ff0000ff</color>
            </IconStyle>
        </Style>
        <name> Red Social (Nacimiento y residencia) </name>\n'''


    try:
        arbol = ET.parse(f_xml)
    except ET.ParseError:
        print("Se ha producido un error procesando el archivo xml")
        exit()

    raiz = arbol.getroot()

    kml += getInformacion(raiz)

    for amigo in raiz.findall(".//"):
        if(amigo.tag == 'persona'):
            kml += getInformacion(amigo)

    kml += "</Document>\n</kml>"

    with open(f_out, 'w', encoding = 'utf-8') as f:
        f.write(kml)

    exit()

def getInformacion(persona):
    texto = "<Placemark>\n"
    texto += "\t<name> NACIMIENTO DE: " +  persona.attrib.get("nombre") + " " + persona.attrib.get("apellidos") + "</name>\n"
    texto += "\t<description>Nacío en :" +  persona.find('datos/nacimiento/lugar').text + "</description>\n"
    texto += "\t<Point>\n"
    texto += "\t\t<coordinates>" + persona.find('datos/nacimiento/coord/longitud').text + "," + persona.find('datos/nacimiento/coord/latitud').text + "," + persona.find('datos/nacimiento/coord/altitud').text + "</coordinates>\n"
    texto += "\t</Point>\n"
    texto += "\t</Placemark>\n"

    texto += "<Placemark>\n"
    texto += "\t<name> RESIDENCIA DE: " +  persona.attrib.get("nombre") + " " + persona.attrib.get("apellidos") + "</name>\n"
    texto += "\t<styleUrl>#residencia</styleUrl>\n"
    texto += "\t<Point>\n"
    texto += "\t\t<coordinates>" + persona.find('datos/residencia/coord/longitud').text + "," + persona.find('datos/residencia/coord/latitud').text + "," + persona.find('datos/residencia/coord/altitud').text + "</coordinates>\n"
    texto += "\t</Point>\n"
    texto += "\t</Placemark>\n"
    return texto


def checkXML(xml, kml):
    try:
        with open(xml, 'r') as f:
            XML2KML(xml, kml);
            return True
    except FileNotFoundError:
        print('No se ha encontrado el archivo, vuelva a intentarlo')
        main();


def main():
    """Metodo que pide por consola el fichero e intenta ejecutar el codigo"""
    f_xml = input("Nombre del fichero XML: ")
    f_kml = input('Nombre del fichero KML donde se quiere guardar la informacion: ')
    checkXML(f_xml, f_kml)

if __name__ == '__main__':
    main()