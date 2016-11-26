# BLEXT —— One stop blog supplier

BLEXT is a blog website where you can finish the whole "edit - store - publish" blogging process in one place, providing ultimate personal blog experience.

## How to contribute (Mac)

### First of all

0. Please make sure there is python3.x properly installed on your Mac.
1. Fork this repo.
2. `git clone` your forked repo to local and `cd` to the repo root.

### Add upstream

```
$ git remote add upstream https://github.com/seagullbird/BLEXT.git
```

### Set up virtual environment

```
$ pyvenv venv
```

This should add a `venv/` folder under your repo root.  And:

```
$ source venv/bin/activate
```

Will activate the virtual environment while you see a `(venv)` before `$` in your terminal.

### Install requirements

```
(venv) $ pip install -r requirements/dev.txt
```

​	Notice: You may also want to run `pip install --upgrade pip` first to upgrade your pip.

### *Set environment variables

*This step is recommended but you don't necessarily have to do this if you're just taking a quick glance.*

On registration in this application, the server would send an email to the email address you're signing up with. This step is the premise that the server send the email successfully. The server will get sender's email address and password from local environment variables, so let's set it up first.

```
(venv) $ export MAIL_USERNAME=mike@email.com
(venv) $ export MAIL_PASSWORD=mikespassword
```

**Use any of your own workable email addresses to replace Mike's.** This will cause no network security problems to you since  your password is only save in your local environment and will be gone after the terminal is shut down.

### Run server

```
(venv) $ chmod +x manage.py
```

​	To give authorization to `manage.py`.

```
(venv) $ ./manage.py runserver
```

​	To get the server running. Now you can visit [127.0.0.1:5000](http://127.0.0.1:5000) to see the **Blext** app.

### Quit virtual environment

```
(venv) $ deactivate
```

### Make changes

You can change any thing you want and if you think you've made some great contributions to this project, please do create a new pull request. Many thanks.

**Also remember to `git pull upstream master`** each next time before opening this project to keep synchronic with me.

## Versions

### Development

- dev1.0: Initialization. Configuring and initializing.
- dev1.0.1: Created index & sign_in & sign_up front pages without adding functions.
- dev1.1: Finished basic user authentication. Added database migration.
- dev1.1.1: Added three utilities for user profiles. Including changing/resetting password and resetting email.
- dev2.0: Added user page, able to upload `.md` file and show on user index. **Potential bugs remain!** Gonna sleep :)
- dev2.1: Added blog page route, able to read pure text blog. Next step **Mistune**!
- dev3.0: Mistune added, able to read blog pages. :)))
- dev3.1: Added user blogs pagination.
- dev3.2: Added BlogParser.
- dev3.2.1: BlogParser bug fixed.
- dev3.2.2: Added visiting control.
- dev4.0: Added user settings, supported about_me, bio, avatar and blog title. Also moved changing password function to settings.
- dev5.0: Added online markdown edit. Issues: pictures storage, page arrangement.
- dev5.1: Page arrangement unsaticefactorily but practically solved.
- dev5.1.1: Added navbar to editor page.
- dev5.2: Editor can now publish new blogs.
- dev6.0: Brand new markdown editor supported by [Bootstrap-Markdown](http://www.codingdrama.com/bootstrap-markdown/), still cannot full-height the `textarea`. :(
- dev6.1: Arrangement rebuilt. editor area able to auto resize now. BUG: cannot do auto resize after clicking expand/unexpand button.
- dev6.2: Implemented drafts feature. BUGs remain. (Errors occur when visiting illicit routes.)
- dev7.0: Added `category` and `tags` support. Abandoned `blog_parser.py` (Not deleted yet).
- dev7.0.1: Unfinished `cats` & `tags` pages and routes.
- dev8.0: Completed `cats` & `tags`, implemented editing function in blog page, `edit` button. —— Completed almost everything I intended to implement. Except: Funtion for the `Help` button in editor page; Both front and backend input validation; POTENTIAL BUGS and NASTY FRONT PAGES.
- dev8.1: Fixed issue: re-editing of an exsiting blog will create a new blog instead of covering the old one.
- dev8.2: Complete re-editing, no bugs in re-editing `cats` and `tags`.
- dev9.0: Initialization of api\_1_0.
- dev9.1: Bug fixing before creating api.
- dev9.2: Api 1.0 basic exceptions, error handlers, JSON to/from implemented without debugging.
- dev9.3: Finished api preparations. Gonna implement all the resources ports tomorrow.
- dev9.4: Api able to get user information and blogs and cats and tags beastifully. Updating an exsiting blog is the next thing to do.
- dev9.5: Finished api 1.0. All passed test with httpie. Don't know if there are remianing bugs.
- dev9.6: Refactored `blog_parser.py` and restarted it. Changed the way of input.
- dev9.6.1: Slight changes.
- dev10.0: Refactored `blog_parser.py`, and added `ParsingError` exception.
- dev10.0.1: Slight changes.
- dev10.1: Added tests of `models.py` and added code coverage detect.
- dev10.2: Added tests with Flask test client, not finished yet.
- dev10.3: Still in testing process. Code coverage now 74%. Also, **Added .gitignore file.** Virtual environment will not be submitted anymore.


## LICENSE

BLEXT is released under the MIT License. See [LICENSE](https://github.com/seagullbird/BLEXT/blob/master/LICENSE) file for details.