class Entorno:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[" " for _ in range(columnas)] for _ in range(filas)]
        self.pos_hormiga = None
        self.pos_meta = None
        self.venenos = set()

    def colocar_hormiga(self, pos):
        self.limpiar_celda(self.pos_hormiga)
        self.pos_hormiga = pos
        self.matriz[pos[0]][pos[1]] = "H"

    def colocar_meta(self, pos):
        self.limpiar_celda(self.pos_meta)
        self.pos_meta = pos
        self.matriz[pos[0]][pos[1]] = "M"

    def colocar_veneno(self, pos):
        if pos != self.pos_hormiga and pos != self.pos_meta:
            self.matriz[pos[0]][pos[1]] = "V"
            self.venenos.add(pos)

    def borrar_elemento(self, pos):
        self.limpiar_celda(pos)

    def limpiar_celda(self, pos):
        if pos and 0 <= pos[0] < self.filas and 0 <= pos[1] < self.columnas:
            self.matriz[pos[0]][pos[1]] = " "
            if pos in self.venenos:
                self.venenos.remove(pos)
