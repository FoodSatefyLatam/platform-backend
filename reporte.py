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
        cur.execute("SELECT valor_referencia, id_contaminante FROM contaminante WHERE nombre= %s",[contaminante]) #de momento se trabaja con el cadmio
        res = cur.fetchall()
        if(res[0][0]!= ""):
            valores_referencia[contaminante] = res[0][0]
            id_contaminantes[contaminante] = res[0][1]

    for alimento in alimentos:
        cur.execute("SELECT id_alimento FROM alimento WHERE especie=%s",[alimento]) 
        id_alimento=cur.fetchone()[0]
        reporte[alimento] = {}
        for contaminante in contaminantes:
            if float(valores_referencia[contaminante]) == 0.0: 
                continue
            cur.execute("SELECT AVG(p.peso), AVG(consumo.cantidad) FROM (SELECT * FROM persona WHERE sexo=%s AND edad > %s AND edad < %s AND peso > %s AND peso < %s AND altura > %s AND altura < %s) AS p LEFT JOIN consumo ON p.id_folio=consumo.id_folio LEFT JOIN alimento ON consumo.id_alimento=alimento.id_alimento WHERE alimento.especie=%s",[sexo,min_edad,max_edad,min_peso,max_peso,min_altura,max_altura,alimento])
            avgs = cur.fetchall()

            peso_promedio = avgs[0][0]
            consumo_promedio = avgs[0][1]
            cur.execute("SELECT Avg(cantidad)  FROM  muestreo WHERE id_contaminante=%s AND id_alimento=%s" ,([id_contaminantes[contaminante]],[id_alimento]))
            promedio_contaminate = cur.fetchone()[0]

            print("["+ alimento +"]["+ contaminante + "]")
            if consumo_promedio is None or promedio_contaminate is None: 
                reporte[alimento][contaminante] = 0
                
            else:
                print(float(consumo_promedio))
                print(float(promedio_contaminate))
                print(float(valores_referencia[contaminante]))
                print(float(peso_promedio))
                reporte[contaminante] += (float(consumo_promedio) * float(promedio_contaminate))/(float(valores_referencia[contaminante]) * float(peso_promedio))
                #reporte[alimento][contaminante] = (float(consumo_promedio) * float(promedio_contaminate))/(float(valores_referencia[contaminante]) * float(peso_promedio))

    return jsonify(reporte)