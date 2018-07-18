# CMU TA3

## Prerequisites
1. A TA2 is running and accessible.

## Command to launch the docker image
Assuming a TA2 is running at ```localhost:45042```.

```bash
docker run -it \
    --rm \
    -p 8080:80 \
    --mount type=bind,source=<path_to_local_dataset_dir>,target=/input \
    --mount type=bind,source=<any_writable_dir>,target=/output \
    -e "D3MCONFIG=/datashop/workflow_components/D3M/d3m.cfg" \
    -e D3MINPUTDIR=/input \
    -e D3MOUTPUTDIR=/output \
    -e TA2ADDR="localhost:45042" \
    -e TA2NAME=<name_of_the_TA2> \
    registry.datadrivendiscovery.org/sdang/cmu-ta3:live
```

Example of using CMU TA2 that runs at port 45042
```bash
docker run -it \
    --rm \
    -p 8080:80 \
    --mount type=bind,source=/data/data/d3m/dryrun2018summer/input,target=/input \
    --mount type=bind,source=/data/data/d3m/dryrun2018summer/output,target=/output \
    -e "D3MCONFIG=/datashop/workflow_components/D3M/d3m.cfg" \
    -e D3MINPUTDIR=/input \
    -e D3MOUTPUTDIR=/output \
    -e TA2ADDR="localhost:45042" \
    -e TA2NAME="cmu" \
    registry.datadrivendiscovery.org/sdang/cmu-ta3:live
```

Then point your browser to [https://localhost:8080](https://localhost:8080).
