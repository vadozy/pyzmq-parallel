Zero MQ sandbox

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- Setting up venv

$ python -m venv venv
$ . ./venv/bin/activate
$ (venv) pip install --upgrade pip
$ (venv) pip install -r requirements.txt
$ (venv) pip install -e .

$ jupyter notebook

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- When upgrading versions use this
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
$ . ./venv/bin/activate
$ (venv) pip install -r requirements.txt --upgrade
