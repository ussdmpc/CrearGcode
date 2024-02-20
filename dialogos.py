from PyQt5.QtWidgets import QApplication, QDialog, QRadioButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QTextEdit
import json

class AdvPos(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Configuración")
        self.setGeometry(200, 200, 400, 200)
        self.l = QLabel("Advertencia:\n EL punto de parteida es x=0 Y=0\nMarcar los puntos...")
        
        # Botones
        self.botonAceptar = QPushButton("Aceptar", self)
        self.botonAceptar.clicked.connect(self.aceptar)
        
        self.botonCancelar = QPushButton("Cancelar", self)
        self.botonCancelar.clicked.connect(self.cancelar)
        
        layoutVertical = QVBoxLayout(self)
        layoutVertical.addWidget(self.l) 
        layoutVertical.addWidget(self.botonAceptar)
        layoutVertical.addWidget(self.botonCancelar)
    
    # aceptar el ponto X=0.0 Y=0.0
    def aceptar(self):
        # Queda como esta
        queda = True
        self.accept()
        return queda
    def cancelar(self):
        # Cerrar el cuadro de diálogo sin capturar datos
        self.reject()    
        
class DialogoAyuda(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Ayuda")
        self.setGeometry(200, 200, 600, 400)
        
        self.ayuda = QTextEdit()

        self.botonCancelar = QPushButton("Cancelar", self)
        self.botonCancelar.clicked.connect(self.cancelar)
       
        layoutVertical = QVBoxLayout(self)
        layoutVertical.addWidget(self.ayuda)
        layoutVertical.addWidget(self.botonCancelar)
        
        try:
            with open('ayuda.txt', 'r') as archivo:
                ayu = archivo.read()
            #return ayu
        except FileNotFoundError:
            print("Archivo de ayuda no encontrado.")
            return None
            
        self.ayuda.setPlainText(ayu)

        
        
    def cancelar(self):
        # Cerrar el cuadro de diálogo sin capturar datos
        self.reject()
        
      
if __name__ == "__main__":
    app = QApplication([])
    dialogo = DialogoConf()
    dialogo.exec_()
        
        
        
class DialogoPerf(QDialog):
    def __init__(self):
        super().__init__()
        print("DialogoPerf")
        
        self.setWindowTitle("Perfilados pre determinados")
        self.setGeometry(200, 200, 400, 200)

        # Crear los QRadioButton
        self.radioPerfxy = QRadioButton("1.Para perfilado Superior (X Y)")
        self.radioPerfxy.setToolTip("Planado de la cara superior")
        
        self.radioPerfxz = QRadioButton("2.Para perfilado Lateral (X Z)")
        self.radioPerfxz.setVisible(False) #Borrar para habilitar
        self.radioPerfxz.setToolTip("Habilitar cuando pase la fiaca")
        
        self.radioPerfyz = QRadioButton("3.Para perfilado Lateral (Y Z)")
        self.radioPerfyz.setVisible(False) #Borrar para habilitar
        self.radioPerfyz.setToolTip("... sigo con fiaca")
        
        self.radioMedioCa = QRadioButton("4.Para hacer calado de Medio Caño")
        self.radioMedioCa.setVisible(False) #Borrar para habilitar
        self.radioMedioCa.setToolTip("Lo necesito pero es medio difisil de calcular")
        
        self.radioPerfSimple = QRadioButton("5.Para Perforacio Simple")
        self.radioPerfSimple.setToolTip("Como sugerencia marcar el taladrado desde el punto X:0 Y:0 desde las entradas de coordenadas\n y agregar el taladrado, es medio pesado poner los mismos datos con cada hueco... pero bue!!... será algun día")
        
        self.radioHuecoMayor = QRadioButton("6.Para Perforacion de hueco mayor al de la herramienta")
        self.radioHuecoMayor.setVisible(False) #Borrar para habilitar
        self.radioHuecoMayor.setToolTip("Tambien me falta de hacer")
        
        # Check para hacer cono
        self.checkPerfCono = QCheckBox("A.Para Conica desde redondo")
        self.checkPerfCono.setToolTip("Para hacer conos en piezas Cilindricas")         
        
        # de paso cañazo y hacemos el listadito
        self.listaRadios = [self.radioPerfxy, self.radioPerfxz, self.radioPerfyz, self.radioMedioCa, self.radioPerfSimple, self.radioHuecoMayor]
        
        # Conectar la señal de cambio para manejar la visibilidad de QLabel y QLineEdit
        self.radioPerfxy.toggled.connect(self.mostrar_campos_adicionales)
        self.radioPerfxz.toggled.connect(self.mostrar_campos_adicionales)
        self.radioPerfyz.toggled.connect(self.mostrar_campos_adicionales)
        self.radioMedioCa.toggled.connect(self.mostrar_campos_adicionales)
        self.radioPerfSimple.toggled.connect(self.mostrar_campos_adicionales)
        self.radioHuecoMayor.toggled.connect(self.mostrar_campos_adicionales)
        self.checkPerfCono.stateChanged.connect(self.mostrar_campos_adicionales)
        
        # Crear QLabel y QLineEdit adicionales
        self.lTexto = QLabel(" ")
        
        self.lDiametro = QLabel("Diametro de la Herramienta:")
        self.eDiametro = QLineEdit()
        self.eDiametro.setToolTip("Es el diametro de la herramienta")

        self.lAvance = QLabel("Avance (mm):")
        self.eAvance = QLineEdit()
        self.eAvance.setToolTip("Es la porcion de corte de la herramienta se ajusta segun la velocidad de corte y las caracteristicas particulares de cada herramienta\n\n TAMBIEN DETERMINA, en una PERFORACION, cada cuantos mm la mecha tiene que hacer descarga. ")
        
        self.l1 = QLabel("Tamaño de la pieza X (mm):")
        self.e1 = QLineEdit()
        
        self.l2 = QLabel("Tamaño de la pieza Y (mm):")
        self.e2 = QLineEdit()
        
        self.l3 = QLabel("Profundidad Z (mm):")
        self.e3 = QLineEdit()
        
        self.l4 = QLabel("Defasaje de la Herramienta X (mm):")
        self.e4 = QLineEdit()
        
        self.l5 = QLabel("Defasaje de la Herramienta Y (mm):")
        self.e5 = QLineEdit()
        
        #Listado de etiquetas y de lineas de texto:
        self.labels = [self.lTexto, self.lDiametro, self.lAvance, self.l1, self.l2, self.l3, self.l4, self.l5]
        self.etiquetas = [self.eDiametro, self.eAvance, self.e1, self.e2, self.e3, self.e4, self.e5]

        # Botones Aceptar y Cancelar
        self.botonAceptar = QPushButton("Aceptar", self)
        self.botonAceptar.clicked.connect(self.aceptar)
        
        self.botonCancelar = QPushButton("Cancelar", self)
        self.botonCancelar.clicked.connect(self.cancelar)
        
        # Acomodar los widgets en un diseño vertical
        layoutVertical = QVBoxLayout(self)
        layoutVertical.addWidget(self.radioPerfxy)
        layoutVertical.addWidget(self.checkPerfCono)
        layoutVertical.addWidget(self.radioPerfxz)
        layoutVertical.addWidget(self.radioPerfyz)
        layoutVertical.addWidget(self.radioMedioCa)
        layoutVertical.addWidget(self.radioPerfSimple)
        layoutVertical.addWidget(self.radioHuecoMayor)
        layoutVertical.addWidget(self.lTexto)
        layoutVertical.addWidget(self.lDiametro)
        layoutVertical.addWidget(self.eDiametro)
        layoutVertical.addWidget(self.lAvance)
        layoutVertical.addWidget(self.eAvance)
        layoutVertical.addWidget(self.l1)
        layoutVertical.addWidget(self.e1)
        layoutVertical.addWidget(self.l2)
        layoutVertical.addWidget(self.e2)
        layoutVertical.addWidget(self.l3)
        layoutVertical.addWidget(self.e3)
        layoutVertical.addWidget(self.l4)
        layoutVertical.addWidget(self.e4)
        layoutVertical.addWidget(self.l5)
        layoutVertical.addWidget(self.e5)
        layoutVertical.addWidget(self.botonAceptar)
        layoutVertical.addWidget(self.botonCancelar)
        self.datos = {}
        
        self.radioPerfxy.setChecked(True)
        
        #### BORRAR ####
        self.botonAceptar.setFocus(True)
        
    def mostrar_campos_adicionales(self):
        # Mostrar u ocultar QLabel y QLineEdit adicionales según el estado
        #print("DialogoPerf mostrar_campos_adicionales")
        self.limpiarE()
        for radio in self.listaRadios:
            if radio.isChecked():
                titulo = radio.text()
                if titulo == "1.Para perfilado Superior (X Y)":
                    estado = radio.isChecked()
                    if self.checkPerfCono.isChecked():
                        self.lTexto.setVisible(estado)
                        self.lTexto.setText(self.checkPerfCono.text())
                        self.lDiametro.setVisible(estado)
                        self.lDiametro.setText("Diametro de la Herramienta")
                        self.eDiametro.setVisible(estado)
                        self.lAvance.setVisible(estado)
                        self.eAvance.setVisible(estado)
                        self.l1.setVisible(estado)
                        self.l1.setText("Diametro Maximo (en mm):") 
                        self.e1.setVisible(estado)
                        self.e1.setToolTip("Es el diametro maximo que tiene nuestra pieza\n Leer las instrucciones de como Fijar la pieza a la maquina")
                        self.l2.setVisible(estado)
                        self.l2.setText("Z Maximo (en mm):")  
                        self.e2.setVisible(estado)
                        self.e2.setToolTip("El frezado es conico, por tanto: el 'Z MAXIMO' es lo maximo a rebajar en el exterior de la pieza\n Leer las instrucciones de como Fijar la pieza a la maquina")
                        self.l3.setVisible(estado)
                        self.l3.setText("Diametro minimo (en mm)") 
                        self.e3.setVisible(estado)
                        self.e3.setToolTip("Es el diametro de la punta del cono. Se recomienda un diametro acorde a el:'Avance Z'")
                        self.l4.setVisible(estado)
                        self.l4.setText("Z minimo (en mm)") 
                        self.e4.setVisible(estado)
                        self.e4.setToolTip("Puede que prefiera una forma cilindrica o punta. De igual manera tenga en cuenta el 'AvanceZ'")
                        self.l5.setVisible(estado)
                        self.l5.setText("Avance Z (en mm):") 
                        self.e5.setVisible(estado)
                        self.e5.setToolTip("Por fin el AvanceZ. A menor valor mejor resolucion de frezado y un tiempo mayor. Sin embargo, tenga en cuenta las caracteristicas de la herramienta a utilizar")
                    else:
                        self.lTexto.setVisible(estado)
                        self.lTexto.setText(titulo)
                        self.lDiametro.setVisible(estado)
                        self.lDiametro.setText("Diametro de la Herramienta")
                        self.eDiametro.setVisible(estado)
                        self.lAvance.setVisible(estado)
                        self.eAvance.setVisible(estado)
                        self.l1.setVisible(estado)
                        self.l1.setText("Largo de la cara X (en mm):")
                        self.e1.setVisible(estado)
                        self.e1.setToolTip("El tamaño de la cara sobre el eje 'X'")
                        self.l2.setVisible(estado)
                        self.l2.setText("Largo de la cara Y (en mm):")
                        self.e2.setVisible(estado)
                        self.e2.setToolTip("El tamaño de la cara paralela al eje 'Y'")
                        self.l3.setVisible(estado)
                        self.l3.setText("Profundidad de desbaste (Z, en mm)")
                        self.e3.setVisible(estado)
                        self.e3.setToolTip("Cuanto se desea rebajar?")
                        self.l4.setVisible(False)
                        self.e4.setVisible(False)
                        self.l5.setVisible(False)
                        self.e5.setVisible(False)
                elif titulo == "2.Para perfilado Lateral (X Z)":
                    estado = radio.isChecked()
                    self.lTexto.setVisible(estado)
                    self.lTexto.setText(titulo)
                    self.lDiametro.setVisible(estado)
                    self.lDiametro.setText("Diametro de la Herramienta")
                    self.eDiametro.setVisible(estado)
                    self.lAvance.setVisible(estado)
                    self.eAvance.setVisible(estado)
                    self.l1.setVisible(estado)
                    self.l1.setText("Largo de la cara X (en mm):")
                    self.e1.setVisible(estado)
                    self.l2.setVisible(estado)
                    self.l2.setText("Largo de la cara Z (en mm):")
                    self.e2.setVisible(estado)
                    self.l3.setVisible(estado)
                    self.l3.setText("Profundidad de desbaste (Y, en mm, Pocitivo(Yn.n o Negativo Y-n.n)")
                    self.e3.setVisible(estado)
                    self.l4.setVisible(False)
                    self.e4.setVisible(False)
                    self.l5.setVisible(False)
                    self.e5.setVisible(False)
                elif titulo == "3.Para perfilado Lateral (Y Z)":
                    estado = radio.isChecked()
                    self.lTexto.setVisible(estado)
                    self.lTexto.setText(titulo)
                    self.lDiametro.setVisible(estado)
                    self.lDiametro.setText("Diametro de la Herramienta")
                    self.eDiametro.setVisible(estado)
                    self.lAvance.setVisible(estado)
                    self.eAvance.setVisible(estado)
                    self.l1.setVisible(estado)
                    self.l1.setText("Largo de la cara Y (en mm):")
                    self.e1.setVisible(estado)
                    self.l2.setVisible(estado)
                    self.l2.setText("Largo de la cara Z (en mm):")
                    self.e2.setVisible(estado)
                    self.l3.setVisible(estado)
                    self.l3.setText("Profundidad de desbaste (X, en mm, Pocitivo(Xn.n) o Negativo(Xn.n)")
                    self.e3.setVisible(estado)
                    self.l4.setVisible(False)
                    self.e4.setVisible(False)
                    self.l5.setVisible(False)
                    self.e5.setVisible(False)
                elif titulo == "4.Para hacer calado de Medio Caño":
                    estado = radio.isChecked()
                    self.lTexto.setVisible(estado)
                    self.lTexto.setText(titulo)
                    self.lDiametro.setVisible(estado)
                    self.lDiametro.setText("Diametro de la Herramienta")
                    self.eDiametro.setVisible(estado)
                    self.lAvance.setVisible(estado)
                    self.eAvance.setVisible(estado)
                    self.l1.setVisible(estado)
                    self.l1.setText("Horientacion (X o Y):")
                    self.e1.setVisible(estado)
                    self.l2.setVisible(estado)
                    self.l2.setText("Largo de la caladura (Sobre X o Y):")
                    self.e2.setVisible(estado)
                    self.l3.setVisible(estado)
                    self.l3.setText("Diametro (en mm)")
                    self.e3.setVisible(estado)
                    self.l4.setVisible(estado)
                    self.l4.setText("Profundidad (en mm)")
                    self.e4.setVisible(estado)
                    self.l5.setVisible(False)
                    self.e5.setVisible(False)
                elif titulo == "5.Para Perforacio Simple":
                    estado = radio.isChecked()
                    self.lTexto.setVisible(estado)
                    self.lTexto.setText(titulo)
                    self.lDiametro.setVisible(estado)
                    self.lDiametro.setText("Se supone que el diametro de la herramienta es del mismo que se desea el hueco")
                    self.eDiametro.setVisible(False)
                    self.lAvance.setVisible(estado)
                    self.eAvance.setVisible(estado)
                    self.l1.setVisible(estado)
                    self.l1.setText("Profundidad (Z, en mm):")
                    self.e1.setVisible(estado)
                    self.e1.setToolTip("Cuanto es lo mazimo que tiene que recorrer el eje Z")
                    self.l2.setVisible(False)
                    #self.l2.setText(False)    #"Descargas cada: ( en mm. Veces que entra y sale)")
                    self.e2.setVisible(False)
                    self.l3.setVisible(False)
                    self.e3.setVisible(False)
                    self.l4.setVisible(False)
                    self.e4.setVisible(False)
                    self.l5.setVisible(False)
                    self.e5.setVisible(False)
                elif titulo == "6.Para Perforacion de hueco mayor al de la herramienta":
                    estado = radio.isChecked()
                    self.lTexto.setVisible(estado)
                    self.lTexto.setText(titulo)
                    self.lDiametro.setVisible(estado)
                    self.lDiametro.setText("Diametro de la Herramienta")
                    self.eDiametro.setVisible(estado)
                    self.lAvance.setVisible(estado)
                    self.eAvance.setVisible(estado)
                    self.l1.setVisible(estado)
                    self.l1.setText("Diametro de Perforacion (en mm):")
                    self.e1.setVisible(estado)
                    self.l2.setVisible(estado)
                    self.l2.setText("Profundidad (Z, en mm):")
                    self.e2.setVisible(estado)
                    self.l3.setVisible(False)
                    self.l3.setText("")
                    self.e3.setVisible(False)
                    self.l4.setVisible(False)
                    self.e4.setVisible(False)
                    self.l5.setVisible(False)
                    self.e5.setVisible(False)
                else:
                    pass

    def aceptar(self):
        # Capturar los datos ingresados y cerrar el cuadro de diálogo
        self.datos = {"operacion": self.lTexto.text()[0:1], 
                        self.lDiametro.text(): self.eDiametro.text(), 
                        self.lAvance.text(): self.eAvance.text(), 
                        self.l1.text(): self.e1.text(), 
                        self.l2.text(): self.e2.text(),
                        self.l3.text(): self.e3.text(),
                        self.l4.text(): self.e4.text(),
                        self.l5.text(): self.e5.text()}
        # MODIFICO EL DICCIONARIO PORQUE ME VUELVE LOCO:
        if "Diametro de la Herramienta" in self.datos:
            self.datos["diamHerr"] = self.datos.pop("Diametro de la Herramienta")

        if "Avance (mm):" in self.datos:
            self.datos["avance"] = self.datos.pop("Avance (mm):")
            
        if "Largo de la cara X (en mm):" in self.datos:
            self.datos["piezaX"] = self.datos.pop("Largo de la cara X (en mm):")
            
        if "Largo de la cara Y (en mm):" in self.datos:
            self.datos["piezaY"] = self.datos.pop("Largo de la cara Y (en mm):")
            
        if "Largo de la cara Z (en mm):" in self.datos:
            self.datos["piezaZ"] = self.datos.pop("Largo de la cara Z (en mm):")
            
        if "Profundidad de desbaste (Z, en mm)" in self.datos:
            self.datos["planadoZ"] = self.datos.pop("Profundidad de desbaste (Z, en mm)")
            
        if "Profundidad de desbaste (Y, en mm, Pocitivo(Yn.n o Negativo Y-n.n)" in self.datos:
            self.datos["DesbasteY"] = self.datos.pop("Profundidad de desbaste (Y, en mm, Pocitivo(Yn.n o Negativo Y-n.n)")
            
        if "Profundidad de desbaste (X, en mm, Pocitivo(Xn.n) o Negativo(Xn.n)" in self.datos:
            self.datos["DesbasteX"] = self.datos.pop("Profundidad de desbaste (X, en mm, Pocitivo(Xn.n) o Negativo(Xn.n)")
            
        if "Horientacion (X o Y):" in self.datos:
            self.datos["HorientaXY"] = self.datos.pop("Horientacion (X o Y):")
            
        if "Largo de la caladura (Sobre X o Y):" in self.datos:
            self.datos["largoCaladura"] = self.datos.pop("Largo de la caladura (Sobre X o Y):")
            
        if "Diametro (en mm)" in self.datos:
            self.datos["DiamMedioCa"] = self.datos.pop("Diametro (en mm)")
            
        if "Diametro (en mm)" in self.datos:
            self.datos["profMedioCa"] = self.datos.pop("Diametro (en mm)")
            
        if "Diametro de Perforacion (en mm):" in self.datos:
            self.datos["profZ"] = self.datos.pop("Diametro de Perforacion (en mm):")
            
        if "Descargas cada: ( en mm. Veces que entra y sale)" in self.datos:
            self.datos["descargasMM"] = self.datos.pop("Descargas cada: ( en mm. Veces que entra y sale)")
            
        if "Diametro de Perforacion (en mm):" in self.datos:
            self.datos["diamPerf""Diametro de Perforacion (en mm):"] = self.datos.pop("Diametro de Perforacion (en mm):")
            
        if "Profundidad (en mm)" in self.datos:
            self.datos["hundeMedioCa"] = self.datos("Profundidad (en mm)") 
            
        if "Profundidad (Z, en mm):" in self.datos:
            self.datos["profPerfora"] = self.datos.pop("Profundidad (Z, en mm):")
            
        if "Z minimo (en mm)" in self.datos:
            self.datos["zMin"] = self.datos.pop("Z minimo (en mm)")
            
        if "Diametro minimo (en mm)" in self.datos:
            self.datos["diamMin"] = self.datos.pop("Diametro minimo (en mm)")
            
        if "Z Maximo (en mm):"in self.datos:
            self.datos["zMax"] = self.datos.pop("Z Maximo (en mm):")
            
        if "Diametro Maximo (en mm):" in self.datos:
            self.datos["diamMax"] = self.datos.pop("Diametro Maximo (en mm):")
            
        if "Avance Z (en mm):" in self.datos:
            self.datos["avanceZ"] = self.datos.pop("Avance Z (en mm):")
        ### ya se que lo podria haber hecho desde un principio, pero esto fue/es a modo de auto castigo 
        
        self.accept()
        return(self.datos)
        
    def limpiarE(self):
        print("DialogoPerf limpiarE")
        self.datos = {}
        self.eDiametro.setText("")
        self.eAvance.setText("")
        self.e1.setText("")
        self.e2.setText("")
        self.e3.setText("")
        self.e4.setText("")
        self.e5.setText("")
        
    def cancelar(self):
        # Cerrar el cuadro de diálogo sin capturar datos
        self.reject()

if __name__ == "__main__":
    app = QApplication([])
    dialogo = DialogoPerf()
    dialogo.exec_()

