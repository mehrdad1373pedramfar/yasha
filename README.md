yasha
=====

Setting up development Environment on Linux

—------------------------------—

### Installing Dependencies

    $ sudo apt-get install libass-dev libpq-dev postgresql \
        build-essential redis-server redis-tools

### Setup Python environment

    $ sudo apt-get install python3-pip python3-dev
    $ sudo pip3 install virtualenvwrapper
    $ echo "export VIRTUALENVWRAPPER_PYTHON=$(which python3.6)" >> ~/.bashrc
    $ echo "alias v.activate=\"source $(which virtualenvwrapper.sh)\"" >> ~/.bashrc
    $ source ~/.bashrc
    $ v.activate
    $ mkvirtualenv —python=$(which python3.6) —no-site-packages yasha

#### Activating virtual environment
    
    $ workon yasha

#### Upgrade pip, setuptools and wheel to the latest version

    $ pip install -U pip setuptools wheel
  
### Installing Project (edit mode)

So, your changes will affect instantly on the installed version

#### yasha
    
    $ cd /path/to/workspace
    $ git clone git@github.com:mehrdad1373pedramfar/yasha.git
    $ cd yasha
    $ pip install -e .
    
#### Enabling the bash autocompletion for this project

```bash
$ echo "eval \"\$(register-python-argcomplete yasha)\"" >> $VIRTUAL_ENV/bin/postactivate
``` 
### Setup Database


#### Configuration

Create a file named ~/.config/yasha.yml

```yaml

db:
  url: postgresql://postgres:postgres@localhost/yasha_dev
  test_url: postgresql://postgres:postgres@localhost/yasha_test
  administrative_url: postgresql://postgres:postgres@localhost/postgres

```
