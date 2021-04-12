# Client (CBSM CLI - Content Based Similarity Matching Command Line Interface)


## Requirements

Python 3.x is required for starting the CLI.

## Dependencies

- pip install click
- pip install requests

## Using the CLI

**NOTE**: In order to use the CLI, you first have to start the backend services! You can either start these by hand, or by using docker-compose.

The CLI has the following options:
- b1, --bpmn1-path TEXT Mandatory. Path to the first bpmn process which is to be compared.
- b2, --bpmn2-path TEXT Mandatory. Path to the second bpmn process which is to be compared.
- dh, --docker-host TEXT Optional. Option used in case the backend is started using docker-compose. On Mac/Windows use the following value: host.docker.internal. On Linux use the docker host address. The value should be specified without "http://"

**If the backend services were started by hand**, then CLI expects the services to be on the following URLs:
- Parsing service: 127.0.0.1:8000
- Twinwords service: 127.0.0.1:8001


### Example usage

If the servers were started by hand:
```
cbsm-cli.py -b1=../input/Application_processing_parallel_(en).bpmn -b2=../input/Car_re-allocation_(en).bpmn
```

If the servers were started by docker-compose:
```
cbsm-cli.py -b1=../input/Application_processing_parallel_(en).bpmn -b2=../input/Car_re-allocation_(en).bpmn -dh=host.docker.internal
```
