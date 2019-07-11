# Convenience script for building docker


# Handle help request
if [ "$1" == "--help" ]; then
    echo "Usage: build_docker.sh <test|deploy|local>"
    exit 0
fi

# Handle the path argument to the runWCC.sh
if [ "$#" == 0 ]; then
    echo "No Options given. Building local test image 'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:test' by default"
    name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:local"
else
    if [ "$1" == "local" ]; then
        echo "Building docker image for local testing: 'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:local'"
        name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:local"
    elif [ "$1" == "test" ]; then
        echo "Building test docker image: 'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:test'"
        name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:test"
    elif [ "$1" == "deploy" ]; then
        echo "Building deployment docker image:  'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:live'"
        name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:live"
    else
        echo "Unknown argument given. Building deployment docker image:  'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:live'"
        name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:live"
    fi
fi

#if [ "$#" == 0 ]; then
    #echo "No Options given. Building local image 'dexplorer.test:local' by default"
    #name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:test"
#else
    #if [ "$1" == "test"]; then
        #echo "Building test docker image: 'dexplorer.test:test'"
        #name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:test"
    #else
        #echo "Building deployment docker image: 'dexplorer.test:live'"
        #name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.test:live"
    #fi
#fi

build_path=$(dirname $(readlink -f "$0"))
app_path=$(dirname $build_path)

docker_path=$build_path/Dockerfile.test

echo "Executing: " "docker build -t $name -f $docker_path $app_path"
docker build -t $name -f $docker_path $app_path

