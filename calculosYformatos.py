import dialogos
######  calculosYformatos #######
def cYf(dic):
    datos = []
    for clave, valor in dic.items():
        datos.append(valor )
        if clave == "operacion" and valor in [1, "1"]: #Para perfilado de la cara superior
            nroPasadasXYZ = pasadas(dic) # para ver cuanto se repite el codigo
            textoCodigo = elaboraCodigo1(dic, nroPasadasXYZ) 
            return(textoCodigo)
        elif clave == "operacion" and valor[0] == "A":
            #print("operacion A")
            textoCodigo = elaboraCodigoA(dic)
            return textoCodigo
        elif clave == "operacion" and valor in [5, "5"]:
            #print("operacion 5")
            textoCodigo = elaboraCodigo5(dic)
            return textoCodigo
            
            
            
        elif clave == "operacion" and valor[0] in [2, "2"]:
            pass
            
def elaboraCodigo5(dic):
    #print(dic)
    avance = dic["avance"] # proporcion de corte
    avance = float(avance)
    zMax = dic["profPerfora"]
    zMax = float(zMax)
    pos = dic["partirDe"]
    posX = float(pos.x()) # pocision de inicial de X
    posY = float(pos.y()) # pocision de inicial de Y
    
    #if posY == 0.0: print(posX, posY)
    if posX == 0.0 and posY == 0.0:
        abrir = dialogos.AdvPos()
        adv = abrir.exec_()
        if adv == True:
            posX = float(pos.x())
            posY = float(pos.y())
    
    #print("pos", pos)
    partida = pos     # partida.x() y partida.y()
    llegada = pos     # llegada.x() y llegada.y() es donde hace el hueco
    
    texto = f"G1 X {partida.x()} Y {partida.y()}  Z {5} ;Arranca elevando Z"
    texto = f"{texto} \nG1 X {llegada.x()} Y {llegada.y()}  Z {0} ;llega al hueco"
    # Taladrado:
    veces = int(zMax / avance + 5)
    para = False
    zAcum = 0
    posZ = 0
    for n in range(veces):
        if para == False:
            if (zMax - zAcum) < avance: 
                posZ = zMax
                posZ = round(posZ, 4)
                #print(f"zAcum < avance: {zAcum} < {avance}")
                para = True
            else:
                posZ = round(posZ + avance, 4)
            #perforo
            texto = f"{texto} \nG1 Z -{posZ} ;perfora"
            #Descargo
            texto = f"{texto} \nG1 Z {0} ;descarga"
            zAcum += avance
        else: break
        
    return texto
        
        
        
        
        
def pasadas(datos): #### 1.Para perfilado Superior (X Y)
    # Calculo la cantidad de pasadas:")
    """ se da segun el tamaño de la pieza, aumiendo que el usuario ha locado la herramienta en el punto 0,0 y a la altura de la pieza entonces arranco con que los pasos  van a ser por el eje Y:
    datos[4] es la medida del eje Y / datos[2] es el avance en mm del usuario + el diametro de la herramienta y 2 mm mas para asegurar la toda la cara"""
    # la cantidad de pasadas de Y es segun el largo de X
    cantX = (float(datos["piezaY"])  / (float(datos["avance"])*2)) + 2 ## agrego 2 pasadas por las dudas el redondeov * 2por redondo 
    # la cantidad de pasadas de X es segun el largo de Y
    cantY = (float(datos["piezaX"])  / (float(datos["avance"])*2)) + 2 ## agrego 2 pasadas por las dudas el redondeov * 2por redondo 
    """ lo que varia es la distancia que se resta vuelta a vuelta"""
    # La precision en Z es fundamental
    cantZ = (float(datos["planadoZ"]) / float(datos["avance"]))
    cantZ = int(cantZ)
    cantXYZ = {"cantX": cantX, "cantY": cantY, "cantZ": cantZ}
    return cantXYZ
    
def elaboraCodigoA(dic):
    #print("calculosYformatos elabora codigo A -- dic", dic )   
    import math
    # el codigo arranca con la posicion de la herramienta, que es la ultima linea de self.textoCodigo (X{posX}, Y{posY}
    # tiene que empezar el frezado con X = posX Y = posY Z = 0
    pos = dic["partirDe"] # coordenadas de inicio
    avance = dic["avance"] # proporcion de corte EJ: 0.18
    avance = float(avance)
    avanceZ = dic["avanceZ"]
    avanceZ = float(avanceZ)
    herramientaD = dic["diamHerr"] # diametro de la herramienta de corte
    herramientaD = float(herramientaD)
    rH = herramientaD / 2 # Radio de la herramienta
    posX = float(pos.x()) # pocision de inicial de X
    posY = float(pos.y()) # pocision de inicial de Y
    posZ = float(round(0.0, 4))            # pocision de inicial de Z
    zMin = float(dic['zMin']) ## es lo mas bajo del eje z en el centro de la pieza
    diamMin = float(dic['diamMin']) # es la punta del cono
    rMin = round(diamMin/2, 4)
    zMax = float(dic['zMax'] )# es la maxima profundidad de z en el exterior de la pieza
    zMax = round(zMax, 4)
    diamMax = float(dic['diamMax']) # el diametro exterior
    rMax = round(diamMax/2, 4)
    """La herramiienta tiene que ir trabajando de manera circular al rededor del centro de la pieza. en la medida que el eje Z baja
    el centro del circulo se tiene que ir agrandando segun el avance y la profundidad """
    ######## AGREGAR ESTA NOTA: 
    ###### El rectangulo que corresponde al circulo tiene que arrancar en el puno X=0, Y=0 y el centro de la herramienta bicada en X=0,Y=0
    ################# Es importante
    #rect = QRect(0, 0, diamMax, diamMax)
    ## ignoro la pocision de la herramienta
    x = 0
    y = 0
    #centro = rect.center()
    ubiX = float(round(((diamMax / 2) ), 4)) # Ubica la herramienta para iniciar
    ubiY = float(round((rH - avance ), 4)) # Ubica la herramienta para iniciar
    texto = f";INICIO \n ;Ubicar la pieza exterior x en: x={ubiX} exterior y en: x={ubiY} \n ;El centro de la erramienta en x=0, y=0, z=0"
    texto = f"{texto}\n;Diametro maximo: {diamMax}, avance: {avance}"
    # al exterior:
    #texto = f"{texto}\nG1 X {ubiX} Y {ubiY} Z 0.0000"
    radio = ubiX ### para no confundir
    #texto = f"{texto}\nG3 I {radio} J 0 "
    x = ubiX
    y = (-ubiY)
    gcI = 0.0
    gcJ = 0.0    
    
    ####### HIPOTENUSA ########
    #c = √(a^2 + b^2)
    """a = rMax
       b = zMax
       hipo = math.sqrt( a ** 2 + b ** 2) """
    hipo = math.sqrt( rMax ** 2 + zMax ** 2)
    #print("Hipo", hipo)
    nuevoDiamMenor = diamMin # nuevoDiamMenor: existe y se calcula en base al cono que se quiera crear teniendo en cuenta el diamMin y zMin
    pasadasZ = zMax / avanceZ
    pasadasZpasadas = 1
    avanceZacum = 0.0
    ############# prueba ###############
    texto = f"{texto}\n; Rectangulo QUE MARCA LA POSICION DE LA PIEZA"
    texto = f"{texto}\n;ES EL CENTRO DE LA HERRAMIENTA QUE RECORRE EL CONTORNO DE LA PIEZA"
    texto = f"{texto}\nG0 X {diamMax} Y 0 Z -0.0"
    texto = f"{texto}\nG0 X {diamMax} Y {diamMax}" # I 0 J 25.0"
    texto = f"{texto}\nG0 X {0} Y {diamMax}"
    texto = f"{texto}\nG0 X {0} Y -{0}"
    
    ########## FIN PRUEBA #######################
    nz = 0
    frenaZ = False
    #while  zMax > posZ:
    while frenaZ == False:
        # las variables de antes del perfilado de la cara
        x = ubiX
        y = (-ubiY)
        gcI = round(y + rH - avance, 4) #I va fijo
        gcJ = round(rMax + rH - avance, 4) #J varia
        frena = False # orden de detener
        # Perfilado de cara
        for n in range(200000): ## muchas por las dudas... cambiar esto por algo mas profecional
            if gcJ >= rMin: 
                texto = f"{texto}\nG0 X {x} Y {y} Z -{posZ}"
                texto = f"{texto}\nG3 X {x} Y {y} I {gcI} J {gcJ}"
                y = round(y + avance, 4)
                gcJ = round(gcJ - avance, 4)
                
                if posZ == zMax: frenaZ = True
                
                # Si se completo frena
                
                if frena == True:
                    #texto = f"{texto}\nfrena X {x} Y {y} I {gcI} J {gcJ}"
                    # Calculo y acomodo el z
                    if posZ >= zMin:
                        #nuevoDiamMenor = round(diamMin + (avanceZacum * 2), 4)
                        nuevoDiamMenor = round(diamMin + (avanceZacum * 2) + ((hipo + (avanceZacum * 2) - (avanceZ * pasadasZpasadas))), 4)
                    else: pass
                    break
                # Compensa la ultima pasada
                if (gcJ * 2) <= nuevoDiamMenor:
                    gcJ = round(nuevoDiamMenor / 2, 4)
                    y  = round(rMax - (nuevoDiamMenor / 2), 4)
                    frena = True
                # No hay que compensar
                else: pass
            # Si se pasa de lineas frena
            else:
                break
        posZ = round(posZ + avanceZ, 4)
        avanceZacum = round(avanceZacum + avanceZ, 4)
         
        if posZ > zMax:
            posZ = float(round(zMax,4))
            posZ = float(round(posZ,4))
            
        nz += 1
        pasadasZpasadas +=1 
        
    texto = f"{texto}\n;fin nz {nz}"
    return texto
    

    
def elaboraCodigo1(dic, nroPasadasXYZ):
    #print("calculosYformatos dic nroPasadas", dic, nroPasadasXYZ)
    #"def calculosYformatos.eleboraCodigo)
    # el codigo arranca con la posicion de la herramienta, que es la ultima linea de self.textoCodigo (X{posX}, Y{posY}
    # tiene que empezar el frezado con X = posX Y = posY Z = 0
    pos = dic["partirDe"] # coordenadas de inicio
    avance = dic["avance"] # proporcion de corte EJ: 0.18
    avance = float(avance)
    herramientaD = dic["diamHerr"] # diametro de la herramienta de corte
    herramientaD = float(herramientaD)
    posX = float(pos.x()) # pocision de inicial de X
    posY = float(pos.y()) # pocision de inicial de Y
    posZ = 0.0            # pocision de inicial de Z
    
    #ajusteZ = pasadasZ % avance # por si la medida no da
    largoX = float(dic["piezaX"])
    largoY = float(dic["piezaY"])
    # Busco una referencia para saber cuando terminar el codigo
    ref = None
    elMedioEsX = None
    elMedioEsY = None
    if largoX < largoY or largoX == largoY:
        ref = largoX / 2   # es la mitad del ancho
        restoREF = largoX % 2
        elMedioEsX = "si"
    elif largoX > largoY:
        ref = largoY / 2
        elMedioEsY = "si"
    else:
        ref = None    
    # Calculo las distancias de -X y -Y en base a la herramienta y el avance
    desplazaMenosX = float(posX) - (herramientaD / 2) + avance
    desplazaMenosY = float(posY) - (herramientaD / 2) + avance
    minimoZ = float(dic["planadoZ"]) # es la profundidad que dio el usuario (ejemplo 2) ###float(dic["divZ"])
    minimoZ = -minimoZ
    
    # Calculo las distancias de +X y +Y en base a la herramienta y el avance
    desplazaMasX = float(posX) + float(dic["piezaX"]) + (herramientaD / 2) - avance
    desplazaMasY = float(posY) + float(dic["piezaY"]) + (herramientaD / 2) - avance #30 + 5=35 - 2 = 33
    
    totalZ = float(dic["planadoZ"])
    
    #calculo la ultima pasada
    texto =  f"G1 X {posX} Y {posY} Z = 0 ;INICIO" 
    # Ahora ha empieza lo bueno:
    sup = 100 #lineas que entran del lado fino(x) = 10  #por 20*30 = 600 / 4 por pasadas = 300
    avanceAcum = 0.0
    avanceCorregido = 0.0
    vueltasXY = None
    if avance < 1:
        avanceCorregido = ref
    avanceCorregido = ref
    ref = int(ref / avance)  
    # Algunos datos de cabezera:
    texto = f"{texto} \n;Ancho(x) y largo(x): {str(largoX)}, {str(largoY)}"
    texto = f"{texto} \n;Diametro de la Herramienta: {str(herramientaD)} -- Desbaste: {str(avance)}"
    primerZ = True
    primerXY = None
    # Calculo las pasadas de Z y me guardo el ajuste
    parcialZ = float(round((totalZ / avance), 4)) # obtengo el numero entero de veces para el eje z
    parcialZe = int(parcialZ)
    parcialZe = float(parcialZe)
    ajuste = parcialZ - parcialZe      # este es el resto
    ajuste = round(ajuste, 4)
    #print("ajuste", ajuste, "parcial", parcialZ, "parE", parcialZe)
    avanceAcumZ = 0.0
    ultimaLineaDeAjuste = False
    for nz in range(int(totalZ + 100)):
        primerXY = True
        if primerZ == True and nz == 0:
            #texto = f"{texto} \n;ajuste {ajuste} and {nz} == 0"
            posZ = 0
            primerZ = False
        else:
            if ultimaLineaDeAjuste == False:
                posZ += avanceAcumZ # round(float((posZ + avanceAcumZ)), 4)
                posZ = round(avanceAcumZ, 4)
            else:
                posZ += round(float(ajuste), 4)
        for n in range(ref+100): ## +100 total frena antes
            if primerXY == True:
                #ubico la Herramienta:
                x = round(posX - (herramientaD / 2) + avance, 4)
                y = round(posY - (herramientaD / 2) + avance, 4)
                texto = f"{texto} \nG1 X {x} Y {y}  Z -{posZ} ;{n} la ubica"
                y = desplazaMasY
                texto = f"{texto} \nG1 X {x} Y {y} Z -{posZ} ;linea{n}"
                x = desplazaMasX
                texto = f"{texto} \nG1 X {x} Y {y} Z -{posZ} ;linea{n}"
                y = desplazaMenosY
                texto = f"{texto} \nG1 X {x} Y {y} Z -{posZ} ;linea{n}"
                x = round(posX - (herramientaD / 2) + avance + avance, 4)
                texto = f"{texto} \nG1 X {x} Y {y} Z -{posZ} ;linea{n}"
                
                x =  desplazaMenosX + avance
                x = round(x, 4)

                avanceAcum = avance
                texto = f"{texto} \n ;----------------{n}"
                primerXY = False
            else: 
                y = round(desplazaMasY - avanceAcum, 4) #30-2=28
                texto = f"{texto} \nG1 X {round(x,4)} Y {round(y,4)} Z -{posZ} "
                x = round(desplazaMasX - avanceAcum, 4)
                texto = f"{texto} \nG1 X {round(x,4)} Y {round(y,4)} Z -{posZ} "
                y = round(desplazaMenosY + avanceAcum, 4)
                texto = f"{texto} \nG1 X {round(x,4)} Y {round(y,4)} Z -{posZ} "
                avanceAcum += avance
                x = round(desplazaMenosX + avanceAcum, 4)
                texto = f"{texto} \nG1 X {round(x,4)} Y {round(y,4)} Z -{posZ} "
                texto = f"{texto} \n ;FIN vuelta subVuelta:{n}"
                                          
                if ((desplazaMenosX + avanceAcum)-2) > (desplazaMasX - avanceAcum): break
        
         

        if avanceAcumZ == totalZ:
            break
        
        verif = totalZ - avanceAcumZ
        verif = round(verif, 4)
        if verif < avance or verif == 0:
            ultimaLineaDeAjuste = True
            ajuste = round((totalZ - avanceAcumZ), 4)
        if ultimaLineaDeAjuste == False:
            avanceAcumZ += avance
        else:
            avanceAcumZ += ajuste
            
        texto = f"{texto} \n ;FIN vuelta abajo:{nz}"

        if avanceAcumZ > totalZ: break  
        
    return texto

