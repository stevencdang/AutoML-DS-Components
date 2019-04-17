echo "Setting up test env for development"

cwd="$(pwd)"
echo "cwd: " $cwd
venv="$cwd"/venv
echo "venv: " $venv

if [ ! -d $venv ]; then
  virtualenv $venv --python=python3.6
  source $venv/bin/activate
  pip install --upgrade pip
  pip install -r $cwd/requirements.txt
  # Deactiate python venv
  deactivate
fi


