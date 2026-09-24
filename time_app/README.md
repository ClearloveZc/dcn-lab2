# DCN Lab 2 time application

Adapted from the course sample at https://github.com/metacomp/nyu-cs2262-001-fa20/tree/master/sample_time_app (commit `9006d5042ea6bda9c7a654c1d9f6554bbb76dbc6`). The original MIT license is retained.

`GET /` returns a greeting. `GET /time` computes the current UTC time for every request, returning ISO 8601 text and `Cache-Control: no-store`.

## Docker

From this directory:

```sh
docker build -t leonchai/sample-time-app:latest .
docker run -d --name dcn-lab2-time-app -p 127.0.0.1:8080:8080 leonchai/sample-time-app:latest
curl http://localhost:8080/time
```

The image uses Python 3.12, Flask and Gunicorn, listens on port 8080, and runs as the unprivileged `nyu` user. The original Python 3.5 image and Flask debug server have been replaced.

## Publishing

Published image: https://hub.docker.com/r/leonchai/sample-time-app

The `latest` tag includes Linux AMD64 and ARM64 variants. To rebuild and publish an update using the owner's Docker Hub login:

```sh
docker login
docker buildx build --platform linux/amd64,linux/arm64 -t leonchai/sample-time-app:latest --push .
```

## Kubernetes

```sh
minikube start -p dcn-lab2 --driver=docker --cpus=2 --memory=3072
kubectl apply -f kubernetes.yaml
kubectl rollout status deployment/sample-time-app
kubectl get pods,deployments,services -o wide
minikube -p dcn-lab2 service sample-time-app --url
```

Open the printed URL with `/time` appended. With the Docker driver on macOS, keep the service command running; it provides a local tunnel to the NodePort. The Service uses port 8080 and NodePort 30080.

For the existing task-local setup, run commands from `lab/lab2` with:

```sh
export MINIKUBE_HOME="$PWD/.local/minikube"
export KUBECONFIG="$PWD/.local/kubeconfig"
./tools/minikube -p dcn-lab2 kubectl -- get pods,services
./tools/minikube -p dcn-lab2 service sample-time-app --url
```

The bundled Minikube kubectl matches the cluster version; the preinstalled host kubectl is older.

## Verification

On September 23, 2026 (America/New_York), the ARM64 image ran successfully in Docker and in local Minikube. `/time` returned HTTP 200 and a current UTC timestamp, and repeated browser requests returned different timestamps. The cluster node was Ready, the Deployment had 1/1 available replicas, and both `http://192.168.49.2:30080/time` from inside the local Docker environment and the macOS service tunnel returned HTTP 200.

The multi-platform image was published to Docker Hub, and the Kubernetes Deployment successfully rolled out with `imagePullPolicy: Always`, verifying registry access. Source repository: https://github.com/ClearloveZc/dcn-lab2

Public-cloud deployment is still pending. No public-cloud deployment is claimed.

## Stop local resources

```sh
docker stop dcn-lab2-time-app
minikube -p dcn-lab2 stop
```

These commands stop the experiment without deleting the image or cluster state.
