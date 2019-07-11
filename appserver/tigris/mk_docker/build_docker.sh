# Convenience script for building docker


# Handle help request
if [ "$1" == "--help" ]; then
    echo "Usage: build_docker.sh <build|push> <local|test|deploy>"
    exit 0
fi

build_path=$(dirname $(readlink -f "$0"))/DataShopDocker
app_path=$build_path

docker_path=$build_path/Dockerfile.tigris

echo "Executing: " "docker build -t $name -f $docker_path $app_path"
docker build -t $name -f $docker_path $app_path


# Handle the path argument to the runWCC.sh
if [ "$#" == 0 ]; then
    echo "No Options given. Building local test image 'dexplorer.tigris:test' by default"
    name="dexplorer.tigris:local"
elif [ "$#" == 1 ]; then
    if [ "$1" == "local" ]; then
        echo "Building docker image for local testing: 'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:local'"
        name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:local"
    elif [ "$1" == "test" ]; then
        echo "Building test docker image: 'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:test'"
        name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:test"
    elif [ "$1" == "deploy" ]; then
        echo "Building deployment docker image:  'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live'"
        name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live"
    else
        echo "Unknown argument given. Building deployment docker image:  'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live'"
        name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live"
    fi

    echo "Executing: " "docker build -t $name -f $docker_path $app_path"
    docker build -t $name -f $docker_path $app_path

elif [ "$#" == 2 ]; then
    if [ "$1" == "build" ]; then
      if [ "$2" == "local" ]; then
          echo "Building docker image for local testing: 'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:local'"
          name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:local"
      elif [ "$2" == "test" ]; then
          echo "Building test docker image: 'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:test'"
          name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:test"
      elif [ "$2" == "deploy" ]; then
          echo "Building deployment docker image:  'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live'"
          name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live"
      else
          echo "Unknown argument given. Building deployment docker image:  'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live'"
          name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live"
      fi

      echo "Executing: " "docker build -t $name -f $docker_path $app_path"
      docker build -t $name -f $docker_path $app_path

    elif [ "$1" == "push" ]; then
      if [ "$2" == "local" ]; then
          echo "Pushing local docker image: 'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:local'"
          name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:local"
      elif [ "$2" == "test" ]; then
          echo "Pushing test docker image: 'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:test'"
          name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:test"
      elif [ "$2" == "deploy" ]; then
          echo "Pushing deployment docker image:  'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live'"
          name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live"
      else
          echo "Unknown argument given. Pushing deployment docker image:  'registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live'"
          name="registry.datadrivendiscovery.org/sdang/cmu-ta3/dexplorer.tigris:live"
      fi
      docker push $name
    else
      echo "Unknown argument given " $1 " must be either <build|push>"
    fi
fi

