# BLEXT —— One stop blog supplier

BLEXT is a blog website where you can finish the whole "edit - store - publish" blogging process in one place, providing ultimate personal blog experience.

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

