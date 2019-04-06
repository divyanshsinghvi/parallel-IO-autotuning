python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv

cd $HOME/progress
python3 -m virtualenv env

source env/bin/activate
pip install numpy
pip install scipy
pip install -U scikit-learn
pip install pandas
