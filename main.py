import pandas as pd

# Clase para representar un nodo en la pila durante el análisis LL(1)
class NodoPila:
    def __init__(self, simbolo, lexema=None):
        self.simbolo = simbolo
        self.lexema = lexema

# Clase para representar un nodo en el árbol sintáctico
class NodoArbol:
    def __init__(self, simbolo, lexema=None):
        self.simbolo = simbolo
        self.lexema = lexema
        self.hijos = []
        self.padre = None

    # Método para agregar un hijo
    def agregar_hijo(self, hijo):
        hijo.padre = self
        self.hijos.append(hijo)

    # Método para imprimir el árbol sintáctico
    def imprimir_arbol(self, nivel=0, prefijo=""):
        print(f"{'  ' * nivel}- {self.simbolo}")
        for hijo in self.hijos:
            hijo.imprimir_arbol(nivel + 1)

# Clase para el analizador LL(1)
class AnalizadorLL1:
    def __init__(self, tabla_csv, entrada):
        # Leer la tabla LL(1) desde un CSV
        self.tabla = pd.read_csv(tabla_csv, index_col=0)
        self.entrada = entrada
        self.pila = []
        self.simbolo_inicial = "E"
        self.raiz = NodoArbol(self.simbolo_inicial)

    # Inicializar la pila con el símbolo inicial y el símbolo de fin de entrada
    def inicializar_pila(self):
        self.pila.append(NodoPila('$'))  # Símbolo de fin de entrada
        self.pila.append(NodoPila(self.simbolo_inicial))  # Símbolo inicial

    # Realizar el análisis LL(1)
    def analizar(self):
        self.inicializar_pila()
        index_entrada = 0
        exito = True

        while len(self.pila) > 0 and index_entrada < len(self.entrada):
            simbolo_pila = self.pila[-1].simbolo
            simbolo_entrada = self.entrada[index_entrada]["simbolo"]

            if simbolo_pila == simbolo_entrada:
                # Coincidencia, avanzar en la entrada y eliminar de la pila
                self.pila.pop()
                index_entrada += 1
            else:
                try:
                    # Validar que la producción existe y no es NaN
                    produccion = self.tabla.loc[simbolo_pila, simbolo_entrada]
                    if pd.isna(produccion):
                        raise ValueError(
                            f"Error de sintaxis: no hay producción válida para '{simbolo_pila}' con símbolo de entrada '{simbolo_entrada}'.")

                    # Aplicar la producción
                    self.pila.pop()  # Quitar el símbolo superior
                    if produccion != "e":  # Si no es producción epsilon
                        for simbolo in reversed(str(produccion).split()):
                            nuevo_nodo_pila = NodoPila(simbolo)
                            self.pila.append(nuevo_nodo_pila)

                            # Crear nodo en el árbol sintáctico
                            nodo_padre = self.raiz  # En este ejemplo, se asume una estructura simple
                            nuevo_nodo_arbol = NodoArbol(simbolo)
                            nodo_padre.agregar_hijo(nuevo_nodo_arbol)
                    else:
                        print(f"Producción epsilon para '{simbolo_pila}'")

                except KeyError:
                    raise ValueError(
                        f"Error de sintaxis: el símbolo '{simbolo_pila}' no se encuentra en la tabla para el símbolo de entrada '{simbolo_entrada}'.")

        if exito and len(self.pila) == 0:
            print("Análisis exitoso. Estructura del árbol sintáctico:")
            self.raiz.imprimir_arbol()  # Imprimir el árbol sintáctico
        else:
            print("Análisis fallido. No se encontró una estructura válida.")

# Cargar la tabla de análisis LL(1) desde el CSV
tabla_csv = "simple_grammar.csv"
entrada = [
    #{"simbolo": "lpar", "lexema": "lpar", "nroline": 1, "col": 1},
    #{"simbolo": "int", "lexema": "int", "nroline": 1, "col": 6},
    #{"simbolo": "plus", "lexema": "plus", "nroline": 1, "col": 10},
    #{"simbolo": "int", "lexema": "int", "nroline": 1, "col": 15},
    #{"simbolo": "rpar", "lexema": "rpar", "nroline": 1, "col": 19},
    #{"simbolo": "$", "lexema": "$", "nroline": 0, "col": 0},
    {"simbolo": "lpar", "lexema": "lpar", "nroline": 1, "col": 1},
    {"simbolo": "int", "lexema": "int", "nroline": 1, "col": 6},
    {"simbolo": "times", "lexema": "times", "nroline": 1, "col": 11},
    {"simbolo": "int", "lexema": "int", "nroline": 1, "col": 17},
    {"simbolo": "rpar", "lexema": "rpar", "nroline": 1, "col": 22},
    {"simbolo": "plus", "lexema": "plus", "nroline": 1, "col": 28},
    {"simbolo": "int", "lexema": "int", "nroline": 1, "col": 33},
    {"simbolo": "$", "lexema": "$", "nroline": 0, "col": 0},
]

# Crear una instancia del analizador y realizar el análisis
analizador = AnalizadorLL1(tabla_csv, entrada)
analizador.analizar()  # Realizar el análisis LL(1) e imprimir el árbol sintáctico
