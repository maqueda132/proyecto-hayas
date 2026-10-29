"""
En esta practica se llevara 
a cabo un repaso de fundamentos de python
"""

# Practica de tipos de datos

TIEMPO_DE_ESPERA = 5
SEPARADOR = "-" * 54

print(SEPARADOR)

def demo_datos():
    print("Vamos a imprimir los tipos de datos")
    print(SEPARADOR)

    puerto= 443  # valor entero
    latencia= 67.8 # valor flotante
    hostname="hola+adios" #cadena de texto

    for valor in (puerto, latencia, hostname):
        print(f"{str(valor):<12} -> {type(valor)}")

if __name__ == "__main__":
    demo_datos()


#asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdas



# Práctica 1 - Programación de Redes
nombre = "Tu Nombre Completo"
print(f"Hola desde {maqueda} - Inicio del Proyecto")