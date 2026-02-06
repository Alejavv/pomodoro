import csv
import os


class AdministradorArchivos:
    '''Inicializa un Administrador de Archivos con un doc_path'''
    def __init__(self, path):
        self.doc_path = path
    
    def leer(self):
        '''Devuelve una lista con diccionarios representando las lineas del archivo CSV'''
        with open(self.doc_path, 'r', encoding='utf-8') as doc:
            doc_lines = csv.DictReader(doc)
            return list(doc_lines)
        
    def escribir(self, registro):
        '''Agrega un registro al archivo CSV, evaluando su existencia:
        - Si existe: agrega el registro sin sobreescribir.
        - Si no existe: agarra las claves del registro pasado por parametro y lo usa para establecer el encabezado del CSV.'''
        
        archivo_existe = os.path.exists(self.doc_path)
        with open(self.doc_path, mode='a', newline='', encoding='utf-8') as doc:
            writer = csv.DictWriter(doc, fieldnames=registro.keys())
            if not archivo_existe:
                writer.writeheader()
            writer.writerow(registro)
    
    def sobreescribir(self, registros):
        '''Sobreescribe los registros de todo el archivo csv con el listado pasado por parametros.'''
        if not registros:
            with open(self.doc_path, 'w', newline='', encoding='utf-8') as doc:
                pass
            return
        with open(self.doc_path, 'w', newline='', encoding="utf-8") as doc:
            writer = csv.DictWriter(doc, fieldnames=registros[0].keys())
            writer.writeheader()
            writer.writerows(registros)
            
    def actualizar(self, id_registro, nuevo_registro):
        '''Actualiza un registro segun el id del registro a modificar.
        Guarda todos los registros y reemplaza la posicion del id por el nuevo registro.
        Si el nuevo registro esta vacio o es nulo, no ingresa reemplazo.'''
        registros = self.leer()
        registros_actualizados = []
        for registro in registros:
            if not registro['id'] == id_registro:
                registros_actualizados.append(registro)
            else:
                if nuevo_registro:
                    registros_actualizados.append(nuevo_registro)
        self.sobreescribir(registros_actualizados)
    
    def eliminar(self, id_registro):
        '''Elimina el registro correspondiente al id pasado por parametro aprovechando
        la propiedad del metodo Actualizar, el cual omite el nuevo registro si este
        esta vacio o es nulo.'''
        self.actualizar(id_registro, {})
        
    def leerSinProcesar(self):
        try:
            lineas_intactas = []
            with open(self.doc_path, mode='r', encoding='utf-8') as archivo:
                for linea in archivo:
                    lineas_intactas.append(linea)
            for i, linea in enumerate(lineas_intactas):
                print(f"{i+1}: {linea.strip()}")
                
        except FileNotFoundError:
            print(f"Error: El archivo no fue encontrado.")