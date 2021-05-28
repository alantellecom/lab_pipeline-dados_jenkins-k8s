#!/bin/bash

if kubectl get secrets -n jenkins -o custom-columns=:metadata.name | grep -q 'gcr-json-key'; then
	echo "secrets gcr-json-key already exists"
else
    kubectl create secret docker-registry gcr-json-key \
                            --docker-server=gcr.io \
                            --docker-username=_json_key \
                            --docker-password="$(cat key-gcp.json)" \
                            --docker-email=any@valid.email
fi