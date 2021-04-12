#!/usr/bin/env python3
import base64
import json
import os.path
import socket

import click
import requests
from banner import BANNER


# Encodes a string to base 64.
def b64enc(data: str):
    encoded_bytes = base64.b64encode(data.encode("utf-8"))
    return str(encoded_bytes, "utf-8")


# Reads a file and converts its contents to base 64.
def read_and_convert(path: str):
    with open(path) as f:
        file_content = ''.join(f.readlines())
        return b64enc(file_content)


# Calls the parsing service with the two base 64 encoded strings.
def call_parsing_service(bpmn_di_1_b64enc, bpmn_di_2_b64enc, url):
    headers = {
        "content-type": "application/json"
    }
    payload = {
        "bpmn_di_1": bpmn_di_1_b64enc,
        "bpmn_di_2": bpmn_di_2_b64enc
    }
    response = requests.post(str(url) + "/parse-bpmn", json=payload, headers=headers)
    response_dict = json.loads(response.content)
    return {"text_1": response_dict['text_1'], "text_2": response_dict['text_2']}


# Calls the twinwords service with the two strings.
def call_twinwords_adapter_service(text_1, text_2, url):
    headers = {
        "content-type": "application/json"
    }
    payload = {
        "text_1": text_1,
        "text_2": text_2
    }
    response = requests.post(str(url) + "/text-similarity", json=payload, headers=headers)
    return response.content


@click.command()
@click.option('--bpmn1-path', '-b1', help='Path to the first bpmn process which is to be compared.')
@click.option('--bpmn2-path', '-b2', help='Path to the second bpmn process which is to be compared.')
@click.option('--docker-host', '-dh', help='Option used in case the backend is started using docker-compose. '
                                           'On Mac/Windows use the following value: host.docker.internal'
                                           'On Linux use the docker host address.'
                                           'The value should be specified without "http://"')
def cbsm_cli(bpmn1_path, bpmn2_path, docker_host):
    print(BANNER)
    if not os.path.isfile(bpmn1_path):
        print(f"Error: path to file ({bpmn1_path}) provided by --bpmn1/-b1 does not exist.")
        return
    if not os.path.isfile(bpmn2_path):
        print(f"Error: path to file ({bpmn2_path}) provided by --bpmn2/-b2 does not exist.")
        return
    if not bpmn1_path.endswith('.bpmn') or not bpmn2_path.endswith('.bpmn'):
        print("Warning: One of the input files does not have an .bpmn extension. Was this intentional?")

    bpmn1_b64enc = read_and_convert(bpmn1_path)
    bpmn2_b64enc = read_and_convert(bpmn2_path)

    if docker_host:
        docker_host_ip = socket.gethostbyname(docker_host)  # Lookup of the IP address
        parsing_service_api_url = f"http://{docker_host_ip}:8000"
        twinwords_service_api_url = f"http://{docker_host_ip}:8001"
    else:
        parsing_service_api_url = "http://127.0.0.1:8000"
        twinwords_service_api_url = "http://127.0.0.1:8001"

    print("Calling parsing service...")
    texts = call_parsing_service(bpmn1_b64enc, bpmn2_b64enc, url=parsing_service_api_url)
    text_1 = texts["text_1"]
    text_2 = texts["text_2"]
    print(f"Text 1: '{text_1}'")
    print(f"Text 2: '{text_2}'")
    print("\nCalling the twinwords adapter service...")
    similarity = call_twinwords_adapter_service(text_1, text_2, url=twinwords_service_api_url)
    print(f"Similarity: {float(similarity) * 100:.2f}%")


if __name__ == '__main__':
    cbsm_cli()
