# Backend 🐍
PROYECTO DESARROLLO DE SOFTWARE I
## API
*http://fabrica.inf.udec.cl:5001*
### Alimentos 🍞
**Ruta** : */alimentos*

>**`[GET]` Retorna la lista completa de alimentos**
>
>Retorna: 
>```
>["alimento1", "alimento2", "alimento3"]
>```
>
>**`[POST]` Retorna la lista de alimentos con el contaminante dado**
>
>Recibe: 
>```
>{
> "contaminante": "nombre_contaminante"
>}
>```
>
>Retorna: 
>
>```
>["alimento1", "alimento2", "alimento3"]
>```

### Calculadora 🎲
**Ruta:** */calculadora*

>**`[POST]` Retorna la lista de alimentos con el contaminante dado**
>
>Recibe
>```
>{
> "weight": "peso", 
> "amount": "cantidad", 
> "food": "alimento"
>}
>```
>
>Retorna:
>```
>["resultado"]
>```

### Reporte 📄
**Ruta:** */reporte*

>**`[POST]` Retorna la lista de alimentos con el contaminante dado**
>
>Recibe: 
>```
>{
>   "sexo":"1",
>   "min_edad":"0",
>   "max_edad":"120",
>   "min_peso":"0",
>   "max_peso":"300",
>   "min_altura":"0",
>   "max_altura":"200",
>   "contaminantes":[
>      "As"
>   ],
>   "alimentos":[
>      "Albacora"
>   ]
>}
>```
>
>Retorna: 
>
>```
>["alimento1", "alimento2", "alimento3"]
>```