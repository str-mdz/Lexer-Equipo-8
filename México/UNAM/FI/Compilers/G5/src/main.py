import re

tokens = {
    # Palabras reservadas 
    'keyword': ['int', 'return', 'if', 'else', 'while', 'for', 'printf'],
    
    # Expresión regular para identificadores: letra o guion bajo, luego letras, números o guion bajo
    'identifier': r'[a-zA-Z_][a-zA-Z0-9_]*',
    
    # Signos de puntuacion
    'punctuation': ['(', ')', '{', '}', '[', ']', ',', ';', '.', '->'],
    
    # Operadores
    'operator': ['=', '+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', 
                 '&&', '||', '!', '&', '|', '^', '<<', '>>', '+=', '-=', '*=', '/=', '++', '--'],
    
    # Expresión regular para constantes 
    'constant': r'\b\d+(\.\d+)?\b',
    
    # Literales de cadena
    'literal_string': r'"[^"\\]*(\\.[^"\\]*)*"',
    
    # Literales de carácter
    'literal_char': r"'[^'\\]*(\\.[^'\\]*)*'",
    
    # Comentarios: // hasta el final de línea o /* */ en múltiples líneas
    'comment': r'//[^\n]*|/\*.*?\*/',
    
    # Espacios en blanco: espacios, tabulaciones, nuevas líneas
    'whitespace': r'\s+',
    
    # Tokens desconocidos: cualquier cosa que no coincida con los patrones anteriores
    'unknown': r'.'
}

def tokenizar(codigo):

    resultado = {
        'keyword': [],
        'identifier': [],
        'punctuation': [],
        'operator': [],
        'constant': [],
        'literal_string': [],
        'literal_char': [],
        'comment': [],
        'unknown': []
    }
    

    posicion = 0
    longitud = len(codigo)
    
    # Recorre todo el código carácter por carácter
    while posicion < longitud:

        # Bandera para saber si encontramos un token en esta posición
        encontrado = False
        
        # Comentarios de una línea (//)
        if codigo[posicion:posicion+2] == '//' or codigo[posicion:posicion+1] == '#':

            # Buscamos el salto de línea
            fin = codigo.find('\n', posicion)

            # Si no hay salto de línea, es hasta el final del código
            if fin == -1:        
                fin = longitud

            # Extraemos el comentario completo
            comentario = codigo[posicion:fin]
            resultado['comment'].append(comentario) 

            # Avanzamos la posición hasta el final del comentario
            posicion = fin
            encontrado = True
            continue 
        
        # Comentarios de varias líneas
        elif codigo[posicion:posicion+2] == '/*':
            # Buscamos el cierre del comentario */
            fin = codigo.find('*/', posicion + 2)

            # Si no hay cierre, es hasta el final
            if fin == -1:
                fin = longitud
            else:
                # Incluimos los caracteres */ en el comentario
                fin += 2
            comentario = codigo[posicion:fin]
            resultado['comment'].append(comentario)
            posicion = fin
            encontrado = True
            continue
        
        # Literales de cadena
        if codigo[posicion] == '"':
            fin = posicion + 1
            # Recorremos hasta encontrar la comilla de cierre
            while fin < longitud:
                # Verificamos que sea comilla de cierre y no tenga \"
                if codigo[fin] == '"' and codigo[fin-1] != '\\':
                    break
                fin += 1
            # Si encontramos el cierre dentro del código
            if fin < longitud:
                string_literal = codigo[posicion:fin+1] 
                resultado['literal_string'].append(string_literal)
                posicion = fin + 1
                encontrado = True
                continue
        
        # Literales char
        if codigo[posicion] == "'":
            fin = posicion + 1
            while fin < longitud:
                if codigo[fin] == "'" and codigo[fin-1] != '\\':
                    break
                fin += 1
            if fin < longitud:
                char_literal = codigo[posicion:fin+1]
                resultado['literal_char'].append(char_literal)
                posicion = fin + 1
                encontrado = True
                continue
        
        # Los espacios, tabs y saltos de línea los ignoramos completamente
        if codigo[posicion].isspace():
            posicion += 1
            encontrado = True
            continue
        
        # Detectar y ignorar caracteres de escape \n, \t
        if codigo[posicion] == '\\' and posicion + 1 < longitud:
            # Lista de caracteres de escape comunes
            escape_chars = ['n', 't', 'r', '\\']
            if codigo[posicion + 1] in escape_chars:
                posicion += 2
                encontrado = True
                continue

        # Operadores
        # Primero verificamos operadores de múltiples caracteres (==, !=, +=)
        # Ordenamos por longitud (mayor a menor) para que primero coincidan los largos
        for op in sorted(tokens['operator'], key=len, reverse=True):
            # Verificamos si desde la posición actual empieza este operador
            if codigo[posicion:posicion+len(op)] == op:
                resultado['operator'].append(op)
                posicion += len(op) 
                encontrado = True
                break
        if encontrado:
            continue

        # Constantes
        # Usamos expresión regular para encontrar números
        match = re.match(tokens['constant'], codigo[posicion:])
        if match:
            resultado['constant'].append(match.group())
            posicion += len(match.group())
            continue
        
    
        # Si empieza con letra o guion bajo, es un identificador o keyword
        if codigo[posicion].isalpha() or codigo[posicion] == '_':
            # Encontramos el identificador completo
            fin = posicion
            
            # isalnum devuelve true si todos los caracteres son alfanuméricos
            while fin < longitud and (codigo[fin].isalnum() or codigo[fin] == '_'):
                fin += 1
            palabra = codigo[posicion:fin]
        
            # Verificamos si es una palabra keyword
            if palabra in tokens['keyword']:
                resultado['keyword'].append(palabra)
            else:
                resultado['identifier'].append(palabra)
            
            posicion = fin 
            continue
        

        # Verificamos si el carácter actual es un signo de puntuación
        if codigo[posicion] in tokens['punctuation']:
            resultado['punctuation'].append(codigo[posicion])
            posicion += 1
            continue
        
        # Si llegamos aquí, el carácter no coincide con ningún patrón y es un lexical error
        resultado['unknown'].append(codigo[posicion])
        posicion += 1
    
    resultadoTotal = {}
    for tipo in resultado:
        resultadoTotal[tipo] = resultado[tipo].copy()
    
    # Eliminamos duplicados
    for tipo in resultado:

        resultado[tipo] = list(set(tuple(resultado[tipo])))
    
    return resultado, resultadoTotal

def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def imprimir(diccionario, tiene_errores):

    print("\n" + "="*50)
    if tiene_errores:
        print("Error léxico")
    else:
        print("Tokens:")
    print("="*50)
    
    for tipo, valores in diccionario.items():
        if valores: 
            print(f"\n{tipo.upper()}: ", end="")
            
            for i, valor in enumerate(valores):
                if i == len(valores) - 1:
                    print(f"{valor}", end="") 
                else:
                    print(f"{valor}, ", end="")
            print()

def main():

    print("=== L E X E R ===")
    print("Opciones:")
    print("1. Ingresar código manualmente")
    print("2. Leer desde archivo")
    
    opcion = input("Selecciona una opción (1/2): ").strip()
    
    codigo = ""
    
    if opcion == "1":
        print("Ingresa tu código (presiona enter dos veces para terminar):")
        lineas = []
        while True:
            linea = input()
            # Si la línea está vacía y la línea anterior también estaba vacía terminamos
            if linea == "" and len(lineas) > 0 and lineas[-1] == "":
                break
            lineas.append(linea)
        # Une con salto de línea
        codigo = "\n".join(lineas)
    
    elif opcion == "2":
        print("Sugerencia: code1.txt, code2.txt, code3.txt")
        nombre_archivo = input("Nombre del archivo a leer: ").strip()
        codigo = leer_archivo(nombre_archivo)
        if codigo is None:
            return
    
    else:
        print("Opción no válida")
        return
    
    if codigo:
        print("\n" + "="*50)
        print("Código")
        print(codigo)

        print("\n" + "="*50)
        resultado, resultadoTotal = tokenizar(codigo)

        tiene_errores = len(resultadoTotal['unknown']) > 0

        imprimir(resultado, tiene_errores)
        
        print("\n" + "="*50)
        print("COUNT:")
        
        # Contamos los tokens 
        total_tokens_original = sum(len(v) for v in resultadoTotal.values())
        print(f"Total de tokens encontrados: {total_tokens_original}")
        
        coms = len(resultado['comment'])
        print(f"Comentarios: {coms}")

        if tiene_errores:
            print("Errores léxicos")
            for error in resultadoTotal['unknown']:
                print(error)

if __name__ == "__main__":
    main()