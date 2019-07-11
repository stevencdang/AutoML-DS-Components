# Build all docker images for Data Explorer

# Handle help request
if [ "$1" == "--help" ]; then
    echo "Usage: build_docker.sh <local|test|deploy>"
    exit 0
fi

if [ "$#" == 0 ]; then
    echo "No Options given. Specify either local, test, or deploy"
    exit 0
elif [ "$#" == 1 ]; then
    if [[ "$1" == "local" ||  "$1" == "test" || "$1" == "deploy" ]]; then
      echo "Running with build argument " $1
      main_build_path=$(dirname $(readlink -f "$0"))
      echo $main_build_path
      # Build Tigris
      cd tigris
      cwd=$(pwd)
      cd mk_docker
      echo "Running command ./build_docker.sh " $1 " from directory: " $(pwd)
      ./build_docker.sh $1
      echo "####### Done building tigris docker ######"
      cd $main_build_path

      # Build Backend Service
      cd backend
      cwd=$(pwd)
      cd mk_docker
      echo "Running command ./build_docker.sh " $1 " from directory: " $(pwd)
      ./build_docker.sh $1
      echo "####### Done building backend docker ######"
      cd $main_build_path

      # Build Frontend Service
      cd frontend
      cwd=$(pwd)
      cd mk_docker
      echo "Running command ./build_docker.sh " $1 " from directory: " $(pwd)
      ./build_docker.sh $1
      echo "####### Done building frontend docker ######"
      cd $main_build_path

      # Build DB
      cd db
      cwd=$(pwd)
      cd mk_docker
      echo "Running command ./build_docker.sh " $1 " from directory: " $(pwd)
      ./build_docker.sh $1
      echo "####### Done building db docker ######"
      cd $main_build_path

      # Build Viz Service
      cd viz
      cwd=$(pwd)
      cd mk_docker
      echo "Running command ./build_docker.sh " $1 " from directory: " $(pwd)
      ./build_docker.sh $1
      echo "####### Done building viz docker ######"
      cd $main_build_path

      # Build Reverse Proxy Service
      cd reverse_proxy
      cwd=$(pwd)
      cd mk_docker
      echo "Running command ./build_docker.sh " $1 " from directory: " $(pwd)
      ./build_docker.sh $1
      echo "####### Done building viz docker ######"
      cd $main_build_path

    else
        echo "Invalid Option given: '" $1 "'. Specify either local, test, or deploy"
        exit 0
    fi
elif [ "$#" == 2 ]; then
    if [[ "$1" == "build" ||  "$1" == "push" ]]; then
      if [[ "$2" == "local" ||  "$2" == "test" || "$2" == "deploy" ]]; then
        echo "Running with build argument " $2
        main_build_path=$(dirname $(readlink -f "$0"))
        echo $main_build_path
        # Build Tigris
        cd tigris
        cwd=$(pwd)
        cd mk_docker
        echo "Running command ./build_docker.sh " $1 " " $2 " from directory: " $(pwd)
        ./build_docker.sh $1 $2
        echo "####### Done building tigris docker ######"
        cd $main_build_path

        # Build Backend Service
        cd backend
        cwd=$(pwd)
        cd mk_docker
        echo "Running command ./build_docker.sh " $1 " " $2 " from directory: " $(pwd)
        ./build_docker.sh $1 $2
        echo "####### Done building backend docker ######"
        cd $main_build_path

        # Build Frontend Service
        cd frontend
        cwd=$(pwd)
        cd mk_docker
        echo "Running command ./build_docker.sh " $1 " " $2 " from directory: " $(pwd)
        ./build_docker.sh $1 $2
        echo "####### Done building frontend docker ######"
        cd $main_build_path

        # Build DB
        cd db
        cwd=$(pwd)
        cd mk_docker
        echo "Running command ./build_docker.sh " $1 " " $2 " from directory: " $(pwd)
        ./build_docker.sh $1 $2
        echo "####### Done building db docker ######"
        cd $main_build_path

        # Build Viz Service
        cd viz
        cwd=$(pwd)
        cd mk_docker
        echo "Running command ./build_docker.sh " $1 " " $2 " from directory: " $(pwd)
        ./build_docker.sh $1 $2
        echo "####### Done building viz docker ######"
        cd $main_build_path

        # Build Reverse Proxy Service
        cd reverse_proxy
        cwd=$(pwd)
        cd mk_docker
        echo "Running command ./build_docker.sh " $1 " " $2 " from directory: " $(pwd)
        ./build_docker.sh $1 $2
        echo "####### Done building Reverse proxy docker ######"
        cd $main_build_path

      else
          echo "Invalid Option given: '" $2 "'. Specify either local, test, or deploy"
          exit 0
      fi
    else
        echo "Invalid Option given: '" $1 "'. Specify either push or build"
        exit 0
    fi

fi
