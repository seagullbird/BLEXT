# BLEXT —— One stop blog supplier

[![Build Status](https://travis-ci.org/seagullbird/BLEXT.svg?branch=master)](https://travis-ci.org/seagullbird/BLEXT)    [![Documentation Status](https://readthedocs.org/projects/blext/badge/?version=latest)](http://blext.readthedocs.io/en/latest/?badge=latest)

BLEXT is a blog website where you can finish the whole "edit - store - publish" blogging process in one place, providing ultimate personal blog experience.

## Documentation

See the latest [documentation](http://blext.readthedocs.io/en/latest/).

## How to contribute (Mac)

### First of all

0. Please make sure there is python3.x properly installed on your Mac.
1. Fork this repo.
2. `git clone` your forked repo to local and `cd` to the repo root.

### Add upstream

```shell
$ git remote add upstream https://github.com/seagullbird/BLEXT.git
```

### Set up virtual environment

```shell
$ pyvenv venv
```

This should add a `venv/` folder under your repo root.  (**Notice: You can only name your virtual environment folder with 'venv' since this is declated in .gitignore.**)

And:

```shell
$ source venv/bin/activate
```

Will activate the virtual environment while you see a `(venv)` before `$` in your terminal.

### Install requirements

```shell
(venv) $ pip install -r requirements/dev.txt
```

​	Notice: You may also want to run `pip install --upgrade pip` first to upgrade your pip.

### *Set environment variables

*This step is recommended but you don't necessarily have to do this if you're just taking a quick glance.*

On registration in this application, the server would send an email to the email address you're signing up with. This step is the prerequisite that the server send the email successfully. The server will get sender's email address and password from local environment variables, so let's set it up first.

```shell
(venv) $ export MAIL_USERNAME=mike@email.com
(venv) $ export MAIL_PASSWORD=mikespassword
```

**Use any of your own workable email addresses to replace Mike's.** This will cause no network security problems to you since  your password is only save in your local environment and will be gone after the terminal is shut down.

### Run server

```shell
(venv) $ chmod +x manage.py
```

To give authorization to `manage.py`. (You only have to do this once.)

```shell
(venv) $ ./manage.py runserver
```

To get the server running. Now you can visit [127.0.0.1:5000](http://127.0.0.1:5000) to see the **Blext** app.

### Quit virtual environment

```shell
(venv) $ deactivate
```

### Make changes

You can change any thing you want and if you think you've made some great contributions to this project, please do create a new pull request. Many thanks.

**Also remember to `git pull upstream master`** each next time before opening this project to keep synchronic with me.

To submit changes, first run `git push origin master` (after `git add .` and `git commit -m '<description>'`) to push your local repo to your own (forked from this) remote repo, then **create a new pull request** in your own github repo and wait for me to merge!

## Versions

### Development

See [development log](./dev_log.md) for more details.

## LICENSE

BLEXT is released under the MIT License. See [LICENSE](https://github.com/seagullbird/BLEXT/blob/master/LICENSE) file for details.