# KATE Project

This is the entire code base for the KATE website. 

## Installation

To install this app, you'll need to go through a few steps.
I recommend using virtualenv, especially with virtualenv-wrapper.

1. Checkout this repository
2. Copy (not move) the settings_local.template to the kate3 project folder
3. Rename the file to settings_local.py
4. Update that file with your environment settings
5. Run `pip install -r requirements.pip`
6. Run `./manage.py syncdb --migrate`

## Server Setup

Right now the project is ran under Gunicorn, which is proxied through
by Apache. There is a `gunicorn.sh` file for starting, stopping,
and restarting the server. There is also a fab file for deployment.