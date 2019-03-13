
# Packaging source into "program" directory
cwd=$(pwd)
# Get lib dir
cd ../lib
libdir=$(pwd)
cd $cwd
# Get build_components dir
cd ../build_components
build_dir=$(pwd)
cd $cwd
# base component project directory
cd ..
wcc_dir=$(pwd)
cd $cwd


srcdir=$(pwd)
# Ensure environment has already been setup
if [ ! -d "$wcc_dir"/venv ]; then
    echo "Virtual environment hasn't bee nconfigured yet. Setting up virtual env"
    $build_dir/setup_test.sh
fi

# Ensure settings.cfg has been created. If not, default to copying sample
if [ ! -f "$srcdir"/src/settings.cfg ]; then
    echo "Settings.cfg does not exist. Creating copy from template"
    cp $srcdir/src/settings.cfg.sample $srcdir/src/settings.cfg
fi

echo "Packaging python source to be built into 'program' directory: $srcdir/program"
if [ ! -d "$srcdir"/program ]; then
    mkdir "$srcdir"/program
else
    # Clean out the old source before continuing
    rm -R "$srcdir"/program
    mkdir "$srcdir"/program
fi
# Copy all source files to the "program" folder for runWCC.sh to copy into new component folder
cd $srcdir/src
# Replicate directory structure
find "$srcdir"/src -mindepth 1 -type d -printf %P\\n | xargs -I {} mkdir "$srcdir/program/{}"
# Copy files
find "$srcdir"/src -type f -name "*.py"  -printf %P\\n | xargs -I {} cp "$srcdir"/src/{} "$srcdir"/program/{}
find "$srcdir"/src -type f -name "*.cfg"  -printf %P\\n | xargs -I {} cp "$srcdir"/src/{} "$srcdir"/program/{}
find "$srcdir"/src -type f -name "*.cfg.sample"  -printf %P\\n | xargs -I {} cp "$srcdir"/src/{} "$srcdir"/program/{}
cd $cwd

cd $libdir
### Copy Dataset dir
# Replicate directory structure
mkdir "$srcdir"/program/ls_dataset
find "$libdir"/ls_dataset -type d -printf %P\\n | xargs -I {} mkdir "$srcdir/program/ls_dataset/{}"
# Copy source files
find "$libdir"/ls_dataset -type f -name "*.py"  -printf %P\\n | xargs -I {} cp "$libdir"/ls_dataset/{} "$srcdir"/program/ls_dataset/{}
### Copy Utilities dir
# Replicate directory structure
mkdir "$srcdir"/program/ls_utilities
find "$libdir"/ls_utilities -type d -printf %P\\n | xargs -I {} mkdir "$srcdir/program/ls_utilities/{}"
# Copy source files
find "$libdir"/ls_utilities -type f -name "*.py"  -printf %P\\n | xargs -I {} cp "$libdir"/ls_utilities/{} "$srcdir"/program/ls_utilities/{}
### Copy Problem Description dir
# Replicate directory structure
mkdir "$srcdir"/program/ls_problem_desc
find "$libdir"/ls_problem_desc -type d -printf %P\\n | xargs -I {} mkdir "$srcdir/program/ls_problem_desc/{}"
# Copy source files
find "$libdir"/ls_problem_desc -type f -name "*.py"  -printf %P\\n | xargs -I {} cp "$libdir"/ls_problem_desc/{} "$srcdir"/program/ls_problem_desc/{}
### Copy D3mTA2 dir
# Replicate directory structure
mkdir "$srcdir"/program/d3m_ta2
find "$libdir"/d3m_ta2 -type d -printf %P\\n | xargs -I {} mkdir "$srcdir/program/d3m_ta2/{}"
# Copy source files
find "$libdir"/d3m_ta2 -type f -name "*.py"  -printf %P\\n | xargs -I {} cp "$libdir"/d3m_ta2/{} "$srcdir"/program/d3m_ta2/{}
### Copy Modeling dir
# Replicate directory structure
mkdir "$srcdir"/program/modeling
find "$libdir"/modeling -type d -printf %P\\n | xargs -I {} mkdir "$srcdir/program/modeling/{}"
# Copy source files
find "$libdir"/modeling -type f -name "*.py"  -printf %P\\n | xargs -I {} cp "$libdir"/modeling/{} "$srcdir"/program/modeling/{}
### Copy D3m_Eval dir
# Replicate directory structure
mkdir "$srcdir"/program/d3m_eval
find "$libdir"/d3m_eval -type d -printf %P\\n | xargs -I {} mkdir "$srcdir/program/d3m_eval/{}"
# Copy source files
find "$libdir"/d3m_eval -type f -name "*.py"  -printf %P\\n | xargs -I {} cp "$libdir"/d3m_eval/{} "$srcdir"/program/d3m_eval/{}
### Copy iviz dir
# Replicate directory structure
mkdir "$srcdir"/program/ls_iviz
find "$libdir"/ls_iviz -type d -printf %P\\n | xargs -I {} mkdir "$srcdir/program/ls_iviz/{}"
# Copy source files
find "$libdir"/ls_iviz -type f -name "*.py"  -printf %P\\n | xargs -I {} cp "$libdir"/ls_iviz/{} "$srcdir"/program/ls_iviz/{}


cd $cwd


