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

    def obtenerMatrizCostos(self, costo_normal=1, costo_veneno=3, costo_meta=1):
        costos = [[costo_normal for _ in range(self.columnas)] for _ in range(self.filas)]
        for i in range(self.filas):
            for j in range(self.columnas):
                val = self.matriz[i][j]
                if val == "V":
                    costos[i][j] = costo_veneno
                elif val == "M":
                    costos[i][j] = costo_meta
                elif val == "H":
                    # Dejar la hormiga como costo normal (su posición no impide el paso)
                    costos[i][j] = costo_normal
                else:
                    costos[i][j] = costo_normal
        return costos
