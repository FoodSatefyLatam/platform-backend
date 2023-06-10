# Backend 🐍
PROYECTO DESARROLLO DE SOFTWARE I
## API
*http://fabrica.inf.udec.cl:5001*
### Alimentos 🍞
**Ruta** : */alimentos*

>**`[GET]` Retorna la lista completa de alimentos**
>
>```
>[
>    "alimento1", 
>    "alimento2", 
>    "alimento3"
>]
>```
>
>**`[POST]` Retorna la lista de alimentos con el contaminante dado**
>
>Recibe: 
>```
>{
> "contaminantes": [
>   "contaminante1", 
>   "contaminante2" 
> ]
>}
>```
>
>Retorna: 
>
>```
>[
>    "alimento1", 
>    "alimento2", 
>    "alimento3"
>]
>```
### contaminantes ☣️
**Ruta** : */contaminantes*
>**`[GET]` Retorna la lista completa de contaminantes**
>Retorna: 
>
>```
>[
>  "As",
>  "As i",
>  "Cd",
>  "Hg",
>  "Pb"
>]
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
> "contaminante": "nombre_contaminante"
>}
>```
>
>Retorna:
>```
>{
> "estado": "bien/mal",
> "formula": resultado de formula,
> "contaminantes_promedio": cantidad de contaminante promedio del alimento
>}
>
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
>{
>    "As": {
>        "alimentos": 0,
>        "promedio": 0
>    },
>    "As i": {
>        "alimentos": 2,
>        "promedio": 0.004504549869401107
>    },
>    "Cd": {
>        "alimentos": 2,
>        "promedio": 0.005152554738551069
>    },
>    "Hg": {
>        "alimentos": 0,
>        "promedio": 0
>    },
>    "Pb": {
>        "alimentos": 0,
>        "promedio": 0
>    }
>}
>```
