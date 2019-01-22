# Convenience script for building docker


# Handle help request
if [ "$1" == "--help" ]; then
    echo "Usage: build_docker.sh <test|deploy>"
    exit 0
fi

# Handle the path argument to the runWCC.sh
if [ "$#" == 0 ]; then
    echo "No Options given. Building test image 'tigris.appserver:test' by default"
    name="tigris.appserver:test"
else
    if [ "$1" == "test"]; then
        echo "Building test docker image: 'tigris.appserver:test'"
        name="tigris.appserver:test"
    else
        echo "Building deployment docker image: 'tigris.appserver:live'"
        name="tigris.appserver:live"
    fi
fi

build_path=$(dirname $(readlink -f "$0"))
app_path=$(dirname $build_path)

docker_path=$build_path/Dockerfile.appserver

echo "Executing: " "docker build -t $name -f $docker_path $app_path"
docker build -t $name -f $docker_path $app_path

