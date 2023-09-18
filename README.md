This is a simple application which provides web services to facilitate group chat and manage data.

pre-requisites:
python version 3.5 and above
Ubuntu version = 18.02; (although works with windows and mac as well)

cd to the project:
create a virtualenv:
python3 -m venv venv

pip3 install -r requirements.txt

To run the testcases defined in E2Etests.py:
make sure the server is up and running : python3 manage.py runserver
to run the testcases: python3 E2Etests.py