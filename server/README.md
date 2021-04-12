# Server

This folder contains the source code for the backend microservices.

## Files

## Requirements

Python 3.x is required for starting the backend services.

## Dependencies

- pip install fastapi
- pip install uvicorn
- pip install requests

**Important**: Make sure that the python site packages are included in your path.

## Running the applications

**NOTE**: These commands only work properly if your working directory is in *server/parsing* or *server/twinwords*

**IMPORTANT**: Before continuing, make sure that you set the TWINWORDS_API_KEY environment variable! Otherwise the Twinwords adapter service won't be able to talk to the Twinwords API.
The value for this variable is included in the twinwords_api.env file. When using docker-compose, this step is not needed.

```shell script
# Parsing service
cd server/parsing
uvicorn parsing_service:app --port=8000

# Twinwords adapter service
cd server/twinwords
uvicorn twinwords_service:app --port=8001
```

**Important**: If you get an error which says "uvicorn: command not found", then either add the site packages to your path or run the services as such:

```shell script
# Parsing service
cd server/parsing
python -m uvicorn parsing_service:app --port=8000

# Twinwords adapter service
cd server/twinwords
python -m uvicorn twinwords_service:app --port=8001
```

Alternative: Use the provided docker-compose.yaml file.


## Docker

This directory contains a Dockerfile which makes dockerizing these microservices easy. 

## Algorithm for converting the BPMN Process to text

Two approaches were implemented:
- depth first walk of the BPMN process
    - advantage: The ordering of the elements somewhat corresponds to the way the process would be executed. 
    - disadvantage: Can't handle loops in the BPMN process.
- simply extracting the texts from the BPMN process>
    - advantage: More flexible, works for any kind of BPMN process
    - disadvantage: The extracted texts are in random order
    
The text similarity calculating algorithm used by the Twinwords Text Similarity API is invariant to the order of the elements. As such, the disadvantage of the simple approach is not relevant and the advantage of the more complicated approach is not worth it.
