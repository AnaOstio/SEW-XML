import xml.etree.ElementTree as ET



def XML2SVG(f_svg, f_out):
    cont = 0;
    lista = []

    try:
        arbol = ET.parse(f_svg)
    except ET.ParseError:
        print("Se ha producido un error procesando el archivo xml")
        exit()

    svg = '''<?xml version="1.0" encoding="utf-8"?>
    <svg width="3770" height="18470" style="overflow:visible " 
    version="1.1" xmlns="http://www.w3.org/2000/svg">'''

    raiz = arbol.getroot()
    svg += getInfo(raiz, 0, 0)

    for amigo in raiz.findall(".//"):
        if(amigo.tag == 'persona'):
            lista.append(amigo.attrib.get("nombre"))
            svg += getInfo(amigo, 1200, 300 * cont )
            cont = cont +1;
    
    conta = 0; 
    var = 0 
    for p in lista:
        if(conta == 0 or conta == 4 or conta == 8):
            var = var + 1
            if(var == 1):
                svg += printLineasHijos(2120, 100, 2325, 100)
            if (var >= 2):
               svg += printLineasHijos(2120, 1250*(var-1), 2325, 1250*(var-1)) 
        conta = conta +1;

    # Pinto las lineas de raiz        
    svg += printLineas()

    svg += '</svg>'
    with open(f_out, 'w', encoding = 'utf-8') as f:
        f.write(svg)
    exit()


def printLineasHijos(dx1, dy1, dx2, dy2):
    cad = ""
    cad += "<line x1 = '{}' y1 = '{}' x2 = '{}' y2 = '{}' stroke-width = '3' stroke = 'black'/>".format(dx1,dy1,dx2,dy2)
    cad += "<line x1 = '{}' y1 = '{}' x2 = '{}' y2 = '{}' stroke-width = '3' stroke = 'black'/>".format(dx2,dy1,dx2,dy2+900)
    cad += "<line x1 = '{}' y1 = '{}' x2 = '{}' y2 = '{}' stroke-width = '3' stroke = 'black'/>".format(dx1,dy1+300,dx2,dy2+300)
    cad += "<line x1 = '{}' y1 = '{}' x2 = '{}' y2 = '{}' stroke-width = '3' stroke = 'black'/>".format(dx1,dy1+600,dx2,dy2+600)
    cad += "<line x1 = '{}' y1 = '{}' x2 = '{}' y2 = '{}' stroke-width = '3' stroke = 'black'/>".format(dx1,dy1+900,dx2,dy2+900)
    return cad

def printLineas():
    cad = ""
    cad += "<line x1 = '915' y1 = '100' x2 = '1215' y2 = '100' stroke-width = '3' stroke = 'black'/>"
    cad += "<line x1 = '400' y1 = '125' x2 = '400' y2 = '2500' stroke-width = '3' stroke = 'black'/>"
    cad += "<line x1 = '400' y1 = '2500' x2 = '1215' y2 = '2500' stroke-width = '3' stroke = 'black'/>"
    cad += "<line x1 = '400' y1 = '1250' x2 = '1215' y2 = '1250' stroke-width = '3' stroke = 'black'/>"
    return cad

def getInfo(persona, x, y):
    dx = 15 + x
    dy = 25 + y
    tx = 350 + x
    ty = 60 + y
    cad = ''

    cad += "<rect x='{}' y='{}' width='900' stroke = 'blue' stroke-width = '7' height = '100' fill='yellow' />".format(dx, dy)
    cad += '<text x= "{}" y = "{}" text-anchor="middle" font-size="16" style="fill:black">'.format(tx, ty)
    cad += persona.attrib.get("nombre") + " " + persona.attrib.get("apellidos") + ". Nacido el "  + persona.find('datos/nacimiento/fecha').text + " en " + persona.find('datos/nacimiento/lugar').text
    cad += "</text>\n"

    return cad

def checkXML(xml, svg):
    try:
        with open(xml, 'r') as f:
            XML2SVG(xml, svg);
            return True
    except FileNotFoundError:
        print('No se ha encontrado el archivo, vuelva a intentarlo')
        main();

def main():
    """Metodo que pide por consola el fichero e intenta ejecutar el codigo"""
    f_xml = input("Nombre del fichero XML: ")
    f_svg = input('Nombre del fichero SVG donde se quiere guardar la informacion: ')
    checkXML(f_xml, f_svg)

if __name__ == '__main__':
    main()