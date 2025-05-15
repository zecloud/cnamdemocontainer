# Microservice Python avec Dapr

Ce projet est un exemple de microservice Python qui utilise Dapr pour la gestion des bindings, la publication/souscription de messages et l'invocation de services.

## Prérequis

- [Docker](https://www.docker.com/get-started)
- [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)
- Python 3.11+

## Structure du projet

- `app.py` : Application FastAPI avec endpoints utilisant Dapr
- `Dockerfile` : Configuration Docker pour le microservice
- `requirements.txt` : Dépendances Python 
- `components/` : Répertoire contenant les configurations des composants Dapr

## Exécution en mode développement

1. Installez les dépendances :
```
pip install -r requirements.txt
```

2. Démarrez l'application avec Dapr :
```
dapr run --app-id microservice --app-port 5000 --components-path ./components python app.py
```

## Exécution avec Docker

1. Construisez l'image Docker :
```
docker build -t dapr-microservice .
```

2. Exécutez le conteneur avec Dapr :
```
docker run -p 5000:5000 --name dapr-microservice dapr-microservice
```

Pour exécuter avec Dapr Sidecar :
```
dapr run --app-id microservice --app-port 5000 --components-path ./components -- docker run --network host dapr-microservice
```

## API Endpoints

- `GET /` : Endpoint de test
- `POST /send-message` : Envoie un message via un binding Dapr
- `GET /invoke-service/{service_name}` : Invoque une méthode sur un autre service via Dapr

## Bindings Dapr configurés

- `input-binding` : Binding d'entrée (Kafka)
- `output-binding` : Binding de sortie (Kafka)

Pour plus d'informations, consultez la [documentation Dapr](https://docs.dapr.io/).
