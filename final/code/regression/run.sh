python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv

cd ../
python3 -m virtualenv env

source env/bin/activate
pip install numpy
pip install scipy
pip install scikit-learn
pip install pandas
python -m pip install jupyter
