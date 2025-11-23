## MS-RECOMENDATIONS-API
Microservicio encargado de recibir requerimientos de búsqueda y retornar un ranking de trabajadores más compatibles usando búsqueda semántica con vectores, pgvector, TEI, y los datos ingeridos por recommendations-engine.

## Flujo 
1. Recibe texto del requerimiento. + parámentros (limit: cantidad de registros a devolver, umbral: limite maximo del concepto del requerimiento)
2. Llama al servidor TEI para generar embedding del requerimiento.
3. Ejecuta una búsqueda vectorial embedding <-> query_embedding.
4. Aplica threshold opcional.
5. Retorna un ranking ordenado.

## Estructura
ms-recommendations-api/
│── main.py                   
│
├── recomendations/
│   ├── config/
│   │     ├── tei_client.py
│   │     ├── dependency_injection.py
│   │     └── routers_config.py
│   │
│   ├── core/  # Api en si
│   │     ├── api/recomendations_router.py
│   │     ├── repository/professional_repository.py
│   │     └── service/
│   │           ├── recomendations_service.py
│   │           └── impl/recomendations_service_impl.py
│   │
│   ├── schema/
│   │     └── recomendation_schema.py
│
└── requirements.txt

## Documentación de APIS
http://127.0.0.1:8095/docs

## ¿Cómo ejecutar?

1. Si no tienes el servicio tei corriendo ejecuta:

cmd: docker run -d --name tei -p 8090:80 -e MODEL_ID=intfloat/e5-small ghcr.io/huggingface/text-embeddings-inference:cpu-latest

El endpoint principal para embeddings es POST /embed con payload {"inputs": ["texto1","texto2"]}

NOTA: Si TEI no funciona
*  cmd: wf.msc
*  agrega una regla de entrada para:
    * Puerto: 8090
    * Protocolo: TCP
    * Acción: permitir

NOTA: Prueba si TEI funciona
cmd: curl -X POST "http://localhost:8090/embed" -H "Content-Type: application/json" -d "{\"inputs\": [\"hola mundo\"]}"


2. ejecutar el docker-compose

docker compose up --build


## LISTOOO YA ESTÁ CORRIENDO EL SERVICIO !!!