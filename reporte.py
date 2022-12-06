from __main__ import app, mysql, request, jsonify

@app.route("/reporte", methods=["POST"])
def reporte():
    if request.method != "POST":
        return "error"
    reporte = {}
    cur = mysql.connection.cursor()
    request_json = request.get_json()
    sexo = request_json["sexo"]
    min_edad = request_json["min_edad"]
    max_edad = request_json["max_edad"]
    min_peso = request_json["min_peso"]
    max_peso = request_json["max_peso"]
    min_altura = request_json["min_altura"]
    max_altura = request_json["max_altura"]
    alimentos = request_json.get("alimentos")
    contaminantes = request_json.get("contaminantes")
    valores_referencia = {}
    id_contaminantes = {}
    for contaminante in contaminantes:
        reporte[contaminante] = {}
        reporte[contaminante]["promedio"] = 0
        reporte[contaminante]["alimentos"] = 0
        cur.execute("SELECT valor_referencia, id_contaminante FROM contaminante WHERE nombre= %s",[contaminante]) #de momento se trabaja con el cadmio
        res = cur.fetchall()
        if(res[0][0]!= ""):
            valores_referencia[contaminante] = res[0][0]
            id_contaminantes[contaminante] = res[0][1]
        else:
            valores_referencia[contaminante] = 0
            id_contaminantes[contaminante] = 0

    for alimento in alimentos:
        cur.execute("SELECT id_alimento FROM alimento WHERE especie=%s",[alimento]) 
        id_alimento=cur.fetchone()[0]
        #reporte[alimento] = {}
        for contaminante in contaminantes:
            formula = 0.0
            c_personas = 0
            max_formula = 0.0

            if float(valores_referencia[contaminante]) == 0.0: 
                continue

            cur.execute("SELECT Avg(cantidad)  FROM  muestreo WHERE id_contaminante=%s AND id_alimento=%s" ,([id_contaminantes[contaminante]],[id_alimento]))
            promedio_contaminate = cur.fetchone()[0]

            if(promedio_contaminate is None or promedio_contaminate == 0):
                continue

            cur.execute("SELECT p.peso, consumo.cantidad FROM (SELECT * FROM persona WHERE sexo=%s AND edad > %s AND edad < %s AND peso > %s AND peso < %s AND altura > %s AND altura < %s) AS p LEFT JOIN consumo ON p.id_folio=consumo.id_folio LEFT JOIN alimento ON consumo.id_alimento=alimento.id_alimento WHERE alimento.especie=%s",[sexo,min_edad,max_edad,min_peso,max_peso,min_altura,max_altura,alimento])
            personas = cur.fetchall()
            
            for persona in personas:
                formula_actual = (float(persona[1]) * float(promedio_contaminate))/(float(valores_referencia[contaminante]) * float(persona[0]))
                if(formula_actual  > max_formula):
                    max_formula = formula_actual
                formula += formula_actual
                c_personas+=1
            
            if(c_personas != 0):
                reporte[contaminante]["promedio"] += (formula/c_personas)
                reporte[contaminante]["alimentos"] += 1
                #reporte[contaminante]["peor_caso"] += max_formula


    return jsonify(reporte)