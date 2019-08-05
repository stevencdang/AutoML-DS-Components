
# Handle help request
if [ "$1" == "--help" ]; then
    echo "Usage: quick_build_docker.sh <build|push> <local|test|deploy>"
    exit 0
fi

build_path=$(dirname $(readlink -f "$0"))
app_path=$(dirname $build_path)
setup_path=$app_path/build

docker_path=$build_path/Dockerfile.backend


echo "Pulling ta3ta2-api source to be built"

cd $app_path/
if [ ! -d "$app_path"/tmp ]; then
  rm -Rf "$app_path"/tmp
fi
mkdir "$app_path"/tmp
cd "$app_path"/tmp
git clone https://gitlab.com/datadrivendiscovery/ta3ta2-api.git
cd ta3ta2-api
git checkout dist-python


$build_path/build_docker.sh $1 $2



