import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsEllipseItem, QPushButton, QCheckBox, QLineEdit, QShortcut, QRadioButton, QSizePolicy, QTextEdit, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor, QKeyEvent, QTextCursor, QKeySequence, QTransform, QTextCharFormat
from PyQt5.QtCore import QPointF, Qt, QTimer
import dialogos, calculosYformatos
import json
"""
    Muchas cosas estan momentaneamete desabilitadas para la proccima version.
*falta:
    -la vista del eje Z
    -La simulacion desde la linea 0 a la... y el zoom
    -El zoom en el eje XY para que siempre lo haga en la exquina superior izquerda
    -
"""


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


class DrawingAreaZ(QGraphicsView):
    def __init__(self, scene, parent=None):
        print("draw area z")
        super(DrawingAreaZ, self).__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setSceneRect(0, -100, 320, 220)   ###125,125,200,300
        self.puntos = []

    def dibujoRojo(self, x, y):
        print("dibujo Rojo")
        #print("dibujoAzul")
        try:
            x = float(x)
            y = float(y)
        
            #print(x1, x2, y1, y2)

            penRojo = QPen(Qt.red)
            
            # Si hay al menos dos puntos en la lista, dibujar líneas entre los puntos
            if len(self.puntos) >= 2:
                #print(f"largo de puntos:{len(self.puntos)}")
                for i in range(1, len(self.puntos)):
                    p1 = self.puntos[i-1]
                    p2 = self.puntos[i]
                    line_item = QGraphicsLineItem(p1.x(), p1.y(), (p2.x() + p1.x()), (p2.y() + p1.y()))
                    line_item.setPen(penRojo)
                    self.scene().addItem(line_item)

                    

            ##############################################mas o menos esta...agrandar el area y la cuadricula y que arranque bien haciendo la linea
            # Agregar el nuevo punto a la lista
            self.puntos.append(QPointF(x, y))
        except ValueError:
            print("Por favor, ingresa números válidos para las coordenadas.")
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################






class DrawingArea(QGraphicsView):
    def __init__(self, scene, main_window, parent=None):
        #print("draw area")
        super(DrawingArea, self).__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setSceneRect(-50, -50, 620, 620)   ###125,125,200,300
        
        self.puntos = []
        self.MyMainWindow = main_window
        
        
        
    def dibujoAzul(self, x, y):
        #print("dibujoAzul")
        #self.timer.start(500)
        try:
            x = float(x)
            y = float(y)
        
            #print("x1, x2", x, y)

            penAzul = QPen(Qt.blue)
            if self.puntos == []:  # si no hay puntos
                self.puntos.append(QPointF(x, y))
                # como no hay puntos escribo que:
                tex = f"X {x}  Y{y}  ;Inicio"
            else: # si hay puntos
                uPunto = self.puntos[-1] #uPunto = ultimo punto
                nPunto = QPointF(uPunto.x() + x, uPunto.y() + y) # nPunto = nuevo punto
                self.puntos.append(nPunto)
                lineaIt = QGraphicsLineItem(uPunto.x(), uPunto.y(), nPunto.x(), nPunto.y())
                
                lineaIt.setPen(penAzul)
                self.scene().addItem(lineaIt)
                #y porque hay mas de 2 puntos...
                tex = None
                    
            # Agregar el nuevo punto a la lista
            self.MyMainWindow.anotarGcode(tex, self.puntos)     
            
        except ValueError:
            print("Por favor, ingresa números válidos para las coordenadas.")

    def rescatarAzul(self, x=0.0, y=0.0, i=0.0, j=0.0, color=None):
        #print("rescata Az x, y, color=None, i=None, j=None)", x, y, i, j, color)
        penAzul = QPen(Qt.blue)
        if color == "yellow":
            penAzul = QPen(Qt.yellow)
        if self.puntos == []:  
            self.puntos.append(QPointF(x, y))        
        if x != None and y != None and i == None and j == None:   ## si no hay valor de i, j, es una linea o trayecto
            uPunto = self.puntos[-1] 
            QApplication.processEvents()
            lineaIt = QGraphicsLineItem(uPunto.x(), uPunto.y(), x, y) #nPunto.x(), nPunto.y()) # nPunto.x(), nPunto.y())
            lineaIt.setPen(penAzul)
            self.scene().addItem(lineaIt)
            self.puntos.append(QPointF(x, y)) 
        elif x != None and y != None and i != None and j != None:   ## si hay valor de i, j, es un circulo
            radio = j
            centroX = self.puntos[-1].x()
            centroY = self.puntos[-1].x() 
            circulo = QGraphicsEllipseItem(centroX - radio , centroY - radio , radio * 2, radio * 2)
            # Agregar el círculo a la escena
            self.scene().addItem(circulo)
            self.puntos.append(QPointF(centroX, centroY))    



class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        
        self.zoomXY = 1.4
        self.zoomZ  = 1.0
        
        # Crear la interfaz principal
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        QApplication.processEvents()
        
        
        # Crear las áreas de dibujo
        grillaRoja = QPen(Qt.red)
        grillaRoja.setWidth(0)
        grillaNegra = QPen(Qt.black)
        grillaNegra.setWidth(0)
        lineaAzul = QPen(Qt.blue)
        lineaVerde = QPen(Qt.green)
        #ellipse_pen_black = QPen(Qt.black)
        #ellipse_pen_black.setWidth(2)
        
        scene1 = QGraphicsScene()
        #sceneA = QGraphicsScene()
        
        self.scene2 = QGraphicsScene()
        
        # Cuadricula roja y fondo verde para la primera área
        for i in range(-25, 401, 20):
            scene1.addLine(i, -45, i, 400, grillaRoja)
            scene1.addLine(-45, i, 400, i, grillaRoja)
       
        #grillaRoja = QPen(Qt.green)
        #scene1.addLine(-10, 0, 200, 0, grillaRoja)
        #scene1.addLine(0, -10, 0, 300, grillaRoja)
            
        # Cuadricula negra y fondo blanco para la segunda área
        for i in range(-100, 251, 15):
            self.scene2.addLine(i, -100, i, 250, grillaNegra)
            self.scene2.addLine(-100, i, 250, i, grillaNegra)

        ##############################################################################
        # Crear elementos para dibujar líneas y círculos
        #line = scene1.addLine(0, 0, 50, 50, lineaAzul)
        guiaX = scene1.addLine(-10, 0, 200, 0, lineaVerde)
        guiaY = scene1.addLine(0, -10, 0, 300, lineaVerde)
        #lineaXP = self.scene1.addLine(0, 0, 50, 0, lineaAzul)
        
        
        line = self.scene2.addLine(0, 0, 50, 50, lineaAzul)
        guiaX = self.scene2.addLine(-50, 0, 300, 0, lineaVerde)
        guiaY = self.scene2.addLine(0, -50, 0, 100, lineaVerde)
        #self.enchula() #scene1, scene2)

        layoutP = QHBoxLayout(central_widget)
        #layout = QVBoxLayout(central_widget)
        layout = QHBoxLayout()
        
        # Áreas de dibujo en la parte superior
        #global area1
        self.area1 = DrawingArea(scene1, self)
        
        area2 = DrawingAreaZ(self.scene2)

        layout.addWidget(self.area1)

        # Crear widgets para el área izquierda
        self.textoCodigo = QTextEdit(self)
        self.textoCodigo.setStyleSheet("background-color: white;")  # Solo para visualización
        self.textoCodigo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.textoCodigo.setToolTip("Texto para gcode")
        self.textoCodigo.append(" ")
        self.cursor = self.textoCodigo.textCursor()

        self.lCoordX = QLineEdit(self)
        self.lCoordX.setStyleSheet("background-color: white;")  # Solo para visualización
        self.lCoordX.setPlaceholderText("Coordenada X (mm)")
        self.lCoordX.setToolTip("Ingrese 0 para añadir un punto desde 0 una medida relativa al eje 'X'\n dejar en 0 para desplazar paralelo al eje 'Y'")

        self.lCoordY = QLineEdit(self)
        self.lCoordY.setStyleSheet("background-color: white;")  # Solo para visualización
        self.lCoordY.setPlaceholderText("Coordenada Y (mm)")
        self.lCoordY.setToolTip("Ingrese 0 para añadir un punto desde 0 una medida relativa al eje 'Y'\n dejar en 0 para desplazar paralelo al eje 'X'")
        
        self.anotar_button = QPushButton("Anotar", self)
        self.anotar_button.clicked.connect(self.anotar) #area1.draw_blue_line(0,0,50,50)) #self.anotarYdibujar)
        self.anotar_button.setToolTip("Pasar a codigo G las coordenadas")
        
        """habilitar si hace falta"""
        #self.borraLineaButton = QPushButton("Deshacer", self)
        self.borraLineaButton = QPushButton("------", self)
        #self.borraLineaButton.clicked.connect(self.borraLinea)

        self.rescatarButton = QPushButton("Dibujar desde Texto", self)
        self.rescatarButton.clicked.connect(self.rescatarCodigo)
        self.rescatarButton.setToolTip("Dibujar desde el codigo creado")

        self.botonreinicio = QPushButton("Reiniciar", self)
        self.botonreinicio.clicked.connect(self.reinicio)
        self.botonPerfilado = QPushButton("Agregar Perfilado", self)
        self.botonPerfilado.clicked.connect(self.abrirDialogoPerf)
        self.botonPerfilado.setToolTip("Trabajos pre determinados")
        self.botonAyuda = QPushButton("Ayuda", self)
        self.botonAyuda.clicked.connect(self.abrirDialogoAyuda)
        self.botonMasZoom = QPushButton("Zoom +XY", self)
        self.botonMasZoom.clicked.connect(lambda: self.haceZoom("+", "XY"))
        self.botonMenosZoom = QPushButton("Zoom -XY", self)
        self.botonMenosZoom.clicked.connect(lambda: self.haceZoom("-", "XY"))
        self.botonMasZoomZ = QPushButton("Zoom +Z", self)
        self.botonMasZoomZ.clicked.connect(lambda: self.haceZoom("+", "Z"))
        self.botonMenosZoomZ = QPushButton("Zoom -Z", self)
        self.botonMenosZoomZ.clicked.connect(lambda: self.haceZoom("-", "Z"))
        # wid para simulacion:
        self.labDesde = QLabel("Simulacion:\n\n\nDesde 0 a:")
        self.labDesde.setMaximumSize(80, 100)
        self.lineHasta = QLineEdit()
        self.lineHasta.setMaximumSize(60, 30)
        self.lineHasta.setToolTip("***DENTRO DE POCO***")
        self.botSig = QPushButton("Siguiente")
        self.botSig.clicked.connect(lambda: self.simular("mas"))
        self.botSig.setMaximumSize(65, 33)
        self.botAtr = QPushButton("Anterior") 
        self.botAtr.clicked.connect(lambda: self.simular("menos"))
        self.botAtr.setMaximumSize(65, 33)
        # su layout
        layoutSimul = QVBoxLayout(self)
        layoutSimul.addWidget(self.labDesde)
        layoutSimul.addWidget(self.lineHasta)
        layoutSimul.addWidget(self.botSig)
        layoutSimul.addWidget(self.botAtr)
        #layoutSimul.SetMaximumSize(300, 200)
        
        self.labInfoZoom = QLabel(f"Zoom: V1: {self.zoomXY} / V2: {self.zoomZ}") 

        layoutVarios = QVBoxLayout()
        layoutVarios.addWidget(area2)
        
        layoutVariosH = QHBoxLayout()
        layoutVariosH.addWidget(self.textoCodigo)
        
        layoutZoom = QVBoxLayout()
        layoutZoom.addWidget(self.botonMasZoom)
        layoutZoom.addWidget(self.botonMenosZoom)
        layoutZoom.addWidget(self.labInfoZoom)
        layoutZoom.addWidget(self.botonMasZoomZ)
        layoutZoom.addWidget(self.botonMenosZoomZ)
        
        layoutVarios.addLayout(layoutVariosH)
        layoutVariosH.addLayout(layoutSimul)
        layoutVariosH.addLayout(layoutZoom)
        
        layoutVarios.addWidget(self.lCoordX)
        layoutVarios.addWidget(self.lCoordY)
        layoutVarios.addWidget(self.anotar_button)
        layoutVarios.addWidget(self.borraLineaButton)
        layoutVarios.addWidget(self.rescatarButton)
        layoutVarios.addWidget(self.botonreinicio)
        layoutVarios.addWidget(self.botonPerfilado)
        layoutVarios.addWidget(self.botonAyuda)

        layoutP.addLayout(layout)
        layoutP.addLayout(layoutVarios)
        
        
        
        shortcut = QShortcut(QKeySequence(Qt.AltModifier + Qt.Key_Q), self)
        shortcut.activated.connect(self.cerrarVentana)
        self.rescatarButton.installEventFilter(self) # asocio
        
        
        self.itemsInicio = self.area1.scene().items()
        
        self.showMaximized()
        
        self.botonPerfilado.setFocus(True)
        self.haceZoom("+", "XY")
        
        
        
    def actualizarSelec(self, nLin):
        if nLin > 0:
            cursor = self.textoCodigo.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.movePosition(cursor.NextBlock, cursor.KeepAnchor, nLin)
            seleccion = self.textoCodigo.setTextCursor(cursor)
            seleccion = seleccion.split("/n")
            return True
            
            
    def simular(self, accion):
        #print("para dibujar las lineas que se eligen del codigo", accion) #, event)
        #print("es un mal metodo, no sirve para simular")
        
        #self.cursor = self.textoCodigo.textCursor()            
        # CAMBIO EL FORMATO: Obtener el formato actual del cursor
        formato_actual = self.textoCodigo.textCursor().charFormat()
        # Crear un nuevo formato con fondo rojo
        formato_nuevo = QTextCharFormat()
        formato_nuevo.setBackground(QColor("red"))
        # Combinar el nuevo formato con el formato actual
        formato_nuevo.merge(formato_actual)
        # Aplicar el nuevo formato al texto seleccionado
        self.textoCodigo.setCurrentCharFormat(formato_nuevo)
        
        if accion == "mas":
            self.cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor)
            seleccion = self.textoCodigo.setTextCursor(self.cursor)
            texto = self.cursor.selectedText()
            texto = texto.split("\n")
            for linea in texto:
                if 'X' in linea and 'Y' in  linea:
                    # Dividir la línea en partes 
                    partes = linea.split()
                    # Inicializar variables para almacenar los valores de X e Y
                    valorX = None
                    valorY = None
                    # buscar los valores de X e Y
                    for i in range(len(partes) - 1):
                        if partes[i] == 'X':
                            valorX = float(partes[i + 1])
                        elif partes[i] == 'Y':
                            valorY = float(partes[i + 1])
                        valorI = None
                        valorJ = None
                # con I y J
                if 'I' in linea and 'J' in  linea:
                    # Dividir la línea en partes 
                    partes = linea.split()
                    
                    # Inicializar variables para almacenar los valores de X e Y
                    valorI = None
                    valorJ = None
                    # buscar los valores de X e Y
                    for i in range(len(partes) - 1):
                        if partes[i] == 'I':
                            valorI = float(partes[i + 1])
                        elif partes[i] == 'J':
                            valorJ = float(partes[i + 1])
                try:
                    self.area1.rescatarAzul(float(valorX), float(valorY), valorI, valorJ, None) #, "yellow")
                except:
                    pass
                    
        elif accion == "menos":
            self.cursor.movePosition(QTextCursor.Up, QTextCursor.KeepAnchor)
            seleccion = self.textoCodigo.setTextCursor(self.cursor)
            texto = self.cursor.selectedText()
            texto = texto.split("\n")
            if len(self.area1.puntos) > 1:
                self.area1.puntos.pop()
                self.area1.scene().removeItem(self.area1.scene().items()[0])
        
    def haceZoom(self, tipo, eje):
        #print("zoom")  
        # para hacer zoom
        if tipo == "+" and eje == "XY":
            self.zoomXY += 0.2
        elif tipo == "-" and eje == "XY":
            self.zoomXY -= 0.2
            if self.zoomXY <= 0.2:
                self.zoomXY = 0.2
        self.zoomXY = round(self.zoomXY, 1)
        vistaXY = QTransform() # Modifica el tamaño
        vistaXY.scale(self.zoomXY, self.zoomXY)
        #self.mapToScene(cursor_position) invertigar
        self.area1.setTransform(vistaXY) # habilitar para zoom
        ######la otra va a ser vistaZ y self.zoomZ
        
        self.labInfoZoom.setText(f"Zoom: V1 en: {self.zoomXY} / V2 en: {self.zoomZ}")
        
    def anotar(self):
        #print("anotar")
        #coordenadas de los campos
        x = self.lCoordX.text()
        y = self.lCoordY.text()
        self.area1.dibujoAzul(x, y)
        
        
            
    def anotarGcode(self, tex=None, puntos=None):
        #print("anotarGcode")
        try:
            dato = puntos[-1]
        except: 
            dato = puntos[0]
        if tex:
            self.textoCodigo.append(f"G1 X { dato.x()} Y {dato.y() } {tex}")
        else:
            self.textoCodigo.append(f"G1 X { dato.x()} Y {dato.y() }") #self.puntos[-1])
            
          
    def reinicio(self):
        #print("Reinicio")
        self.area1.puntos = []
        if len(self.area1.scene().items()) > 46:
            for item in self.area1.scene().items():
                self.area1.scene().removeItem(item)
                if len(self.area1.scene().items()) == 46:
                    break
      
        
        self.textoCodigo.setText("")
        
    def rescatarCodigo(self):       
        #print("RescatarCOdigo")
        #borro los puntos
        
        self.area1.puntos = []
        #Limpia la esena
        texto = self.textoCodigo.toPlainText()
        if len(self.area1.scene().items()) > 46:
            for item in self.area1.scene().items():
                
                self.area1.scene().removeItem(item)
                
                if len(self.area1.scene().items()) == 46:
                    break
       
        
        texto = texto.split("\n")
        for linea in texto:
            #print(linea)
            if 'X' in linea and 'Y' in  linea:
                # Dividir la línea en partes 
                partes = linea.split()
                # Inicializar variables para almacenar los valores de X e Y
                valorX = None
                valorY = None
                # buscar los valores de X e Y
                for i in range(len(partes) - 1):
                    if partes[i] == 'X':
                        valorX = float(partes[i + 1])
                    elif partes[i] == 'Y':
                        valorY = float(partes[i + 1])
                    valorI = None
                    valorJ = None
            # con I y J
            if 'I' in linea and 'J' in  linea:
                # Dividir la línea en partes 
                partes = linea.split()
                
                # Inicializar variables para almacenar los valores de X e Y
                valorI = None
                valorJ = None
                # buscar los valores de X e Y
                for i in range(len(partes) - 1):
                    if partes[i] == 'I':
                        valorI = float(partes[i + 1])
                    elif partes[i] == 'J':
                        valorJ = float(partes[i + 1])
            
            try:
                self.area1.rescatarAzul(float(valorX), float(valorY), valorI, valorJ, None) #, "yellow")
            except:
                pass
        
    def eventFilter(self, obj, event):
        #print("Captura los eventos de teclado y mouse")
        if obj is self.rescatarButton and event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_D:
                self.timer.stop()
            return True
        
        return super().eventFilter(obj, event)
        
    def abrirDialogoPerf(self):
        #print("abrir dial p")
        # Crear e mostrar el diálogo"
        dialogo = dialogos.DialogoPerf()
        resultado = dialogo.exec_()
        #print("dil.datos ", dialogo.datos)
        self.anotarMiCodigo(dialogo.datos)
        
        
    def abrirDialogoAyuda(self):
        #print("abrir dial ayuda")
        dialogo = dialogos.DialogoAyuda()
        resultado = dialogo.exec_()
        
        
    def anotarMiCodigo(self, dicc):
        #print("anotarMiCodigo")
        #Elimino los datos que no sirven
        diccLimpio = {}
        for clave, valor in dicc.items():
            if valor != "":
                diccLimpio[clave] = valor
        if self.area1.puntos:
            diccLimpio["partirDe"] = self.area1.puntos[-1]
        else:
            x = round(float(0.0))
            y = round(float(0.0))
            punto = QPointF(x, y)
            diccLimpio["partirDe"] = punto
        elCodigo = calculosYformatos.cYf(diccLimpio) ##MANDAR LA POS_X y POS_Y extraer de la ultima linea de self.textoCodigo
        
        self.textoCodigo.append(elCodigo)
        self.cursor = self.textoCodigo.textCursor()
        self.cursor.setPosition(0)
        
    def cerrarVentana(self):
        # Cierra la aplicación al activar el atajo Alt+Q
        self.close()    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

