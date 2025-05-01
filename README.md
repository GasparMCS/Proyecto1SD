# Tarea 1 - Sistemas Distribuidos

Este proyecto corresponde a la Tarea 1 del curso de Sistemas Distribuidos de la Universidad Diego Portales. Implementa un sistema distribuido que evalúa políticas de cache (TTL y LRU) bajo distintos patrones de tráfico (Uniforme y Poisson), con resultados experimentales medibles.


---

## 🚀 Componentes del sistema

- `scraper`: descarga eventos y los guarda en MongoDB.
- `almacenamiento`: servicio web (FastAPI) que permite consultar eventos, con sistema de caché.
- `generador`: simula tráfico con parámetros controlados y mide estadísticas.

---

## ⚙️ Instalación y ejecución

1. Clona el repositorio:

```bash
git clone https://github.com/Martinxito/Tarea-1-Sistemas-Distribuidos.git
cd Tarea-1-Sistemas-Distribuidos
    Configura las variables de entorno para MongoDB Atlas:
```
Crea un archivo .env con lo siguiente:

MONGO_USER=gasparcampos
MONGO_PASSWORD=gaspar123
MONGO_CLUSTER=cluster0.qs7x48f.mongodb.net
MONGO_DB=eventos
MONGO_COLLECTION=eventos_scrapeados

    Levanta los servicios:

docker-compose up --build

    Para ejecutar solo almacenamiento y generador:

docker-compose up almacenamiento generador

🧪 Experimentos realizados

Se evaluaron las siguientes combinaciones:
1. Solo LRU

    Tamaños de cache: 500, 1000, 1500

    Tráfico: Uniforme y Poisson

    Tiempo: 30 minutos

    Tasa: 15 consultas por segundo

2. Solo TTL

    TTL: 5 min, 10 min, 15 min

    Tráfico: Uniforme y Poisson

3. TTL (5 min) + LRU (500 y 1000)
📊 Métricas recolectadas

    Total de consultas

    HITs y MISSes en cache

    Porcentaje de HIT

    Tiempo promedio de respuesta

    Eliminaciones por LRU

    Eliminaciones estimadas por TTL

💡 Uso del generador de tráfico

Ejemplo de ejecución:

python main.py --duracion 30 --tasa 15 --distribucion poisson

O versión rápida por número exacto de consultas:

python main.py --n 10000 --distribucion uniforme

📌 Endpoints de monitoreo (almacenamiento)
Método	Ruta	Descripción
GET	/eventos/getall_ids	Lista todos los IDs disponibles
GET	/eventos/{id}	Devuelve un evento desde cache o DB
GET	/eventos/lru_stats	Total eliminados por política LRU
GET	/eventos/ttl_stats	Total estimado de TTL eliminados
DELETE	/eventos/cache	Borra todo el cache manualmente
🧠 Justificación técnica

    Se utiliza MongoDB por su soporte nativo a TTL (vía índices).

    LRU se implementa manualmente como política de eliminación por tamaño.

    El generador usa pausas controladas (capped exponential o uniforme) para simular tráfico realista y luego sin pausas para medir rendimiento máximo.

    FastAPI permite exponer métricas de forma simple para análisis.

👨‍💻 Autores

    Martín Ramos Molina

    Gaspar Campos Smith
