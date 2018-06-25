# CMU TA3

## Prerequisites
1. A TA2 is running and accessible.

## Command to launch the docker image
Assuming a TA2 is running at ```localhost:45042```.

```bash
docker run -it -p 9001:443 \
    --mount type=bind,source=<path_to_local_dataset_dir>,target=/input \
    --mount type=bind,source=<any_writable_dir>,target=/output \
    -e "D3MCONFIG=/datashop/workflow_components/D3M/d3m.cfg" \
    -e D3MINPUTDIR=/input \
    -e D3MOUTPUTDIR=/output \
    -e TA2ADDR="localhost:45042" \
    registry.datadrivendiscovery.org/sdang/cmu-ta3:dry_run_demo_test
```

Then point your browser to [https://localhost:9001](https://localhost:9001).
