# Convenience script for building docker


# Handle help request
if [ "$1" == "--help" ]; then
    echo "Usage: build_docker.sh <test|deploy>"
    exit 0
fi

# Handle the path argument to the runWCC.sh
if [ "$#" == 0 ]; then
    echo "No Options given. Building test image 'dexplorer.test:test' by default"
    name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:test"
else
    if [ "$1" == "test"]; then
        echo "Building test docker image: 'dexplorer.test:test'"
        name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:test"
    else
        echo "Building deployment docker image: 'dexplorer.test:live'"
        name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:live"
    fi
fi

build_path=$(dirname $(readlink -f "$0"))
app_path=$(dirname $build_path)

docker_path=$build_path/Dockerfile.test

echo "Executing: " "docker build -t $name -f $docker_path $app_path"
docker build -t $name -f $docker_path $app_path

