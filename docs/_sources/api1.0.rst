API v1.0
===============
Before everything, I have to claim that this is only a testing API for development usage, and it is not guaranteed without any bugs and may well be updated soon. 

Authentication
----------------
BLEXT adopts `Basic access authentication`_ for API authentication. Include your email and password (or token and an empty string) in http request headers and the server on receiving your request will automatically extract them and try to verify your infomation.

Notice that this version of API doesn't support anonymous users, which means you have to do anything below **after** receiveing a valid authentication. And any serving response is done based on a valid authentication.

Remember, since the http server won't remember any status, **each time an request is made there is an authentication required.** Therefore I strongly recommend you only use :ref:`Basic Authentication` once and use :ref:`Token Authentication` afterwards.

.. _Basic access authentication: https://en.wikipedia.org/wiki/Basic_access_authentication

.. _Basic Authentication:

Basic Authentication
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: shell

	$ http --json --auth email:PASSWORD GET https://blext.herokuapp.com/api/v1.0/token
	HTTP/1.1 200 OK
	Connection: keep-alive
	Content-Length: 163
	Content-Type: application/json
	Date: Tue, 06 Dec 2016 07:43:46 GMT
	Server: gunicorn/18.0
	Via: 1.1 vegur

	{
	    "expiration": 3600,
	    "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ4MTAxMDIyNiwiZXhwIjoxNDgxMDEzODI2fQ.eyJpZCI6MX0.OzzWcW3wvBOb6nTskRuUy-3nnB89bXgtiW8YaAKERiU"
	}

.. _Token Authentication:

Token Authentication
~~~~~~~~~~~~~~~~~~~~~~
Once you've received a token you can use it as the authentication instead of email and password. Just replace ``email`` with your token and ``PASSWORD`` with an empty string:

.. code-block:: shell

	$ http --json --auth token: GET/POST <some/other/apis/mentioned/below>

However, the token has an expiration time as you can also see from the first response, initialzed to 3600s. Which means you'll have to apply for another valid token after one hour.

Users
----------------
To get information based on a valid token or an email & PASSWORD pair.

Basic User information
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: shell

	$ http --json --auth token: GET https://blext.herokuapp.com/api/v1.0/user/
	HTTP/1.1 200 OK
	Connection: keep-alive
	Content-Length: 310
	Content-Type: application/json
	Date: Tue, 06 Dec 2016 08:18:52 GMT
	Server: gunicorn/18.0
	Via: 1.1 vegur

	{
	    "avatar_url": "http://...",
	    "blog_count": 1,
	    "blogs": "http://blext.herokuapp.com/api/v1.0/blogs/",
	    "categories": "http://blext.herokuapp.com/api/v1.0/categories",
	    "tags": "http://blext.herokuapp.com/api/v1.0/tags",
	    "url": "http://blext.herokuapp.com/api/v1.0/user/",
	    "username": "username"
	}

The response in json format represents following information:

+------------+----------------------------------------------------------------+
| Name       | Description                                                    |
+============+================================================================+
| avatar_url | The URL for user's avatar.                                     |
+------------+----------------------------------------------------------------+
| blog_count | The number of blogs under the user's name.                     |
+------------+----------------------------------------------------------------+
| blogs      | The API URL with which you can find all the user's blogs.      |
+------------+----------------------------------------------------------------+
| categories | The API URL with which you can find all the user's categories. |
+------------+----------------------------------------------------------------+
| tags       | The API URL with which you can find all the user's tags.       |
+------------+----------------------------------------------------------------+
| url        | The The API URL with which you can the user's information.     |
+------------+----------------------------------------------------------------+
| username   | User's username.                                               |
+------------+----------------------------------------------------------------+

User Categories
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: shell

	$ http --json --auth token: GET https://blext.herokuapp.com/api/v1.0/categories
	HTTP/1.1 200 OK
	Connection: keep-alive
	Content-Length: 60
	Content-Type: application/json
	Date: Tue, 06 Dec 2016 08:49:56 GMT
	Server: gunicorn/18.0
	Via: 1.1 vegur

	{
	    "categories": [
	        {
	            "name": "First"
	        }
	    ]
	}

User Tags
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: shell

	$ http --json --auth token: GET https://blext.herokuapp.com/api/v1.0/tags
	HTTP/1.1 200 OK
	Connection: keep-alive
	Content-Length: 60
	Content-Type: application/json
	Date: Tue, 06 Dec 2016 08:49:56 GMT
	Server: gunicorn/18.0
	Via: 1.1 vegur

	{
	    "tags": [
	        {
	            "name": "First"
	        }
	    ]
	}

Blogs
----------------
Currently based on authentication with blogs API you can: :ref:`get all blogs`, :ref:`get a single blog`, :ref:`get a blog's category`, :ref:`get a blog's tags`, :ref:`publish a new blog` and :ref:`update an existing blog`.

.. _get all blogs:

Get All Blogs
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: shell

	$ http --json --auth token: GET https://blext.herokuapp.com/api/v1.0/blogs/
	HTTP/1.1 200 OK
	Connection: keep-alive
	Content-Length: 701
	Content-Type: application/json
	Date: Tue, 06 Dec 2016 09:02:21 GMT
	Server: gunicorn/18.0
	Via: 1.1 vegur

	{
	    "blogs": [
	        {
	            "author": "http://blext.herokuapp.com/api/v1.0/user/",
	            "body": "<blog body>",
	            "category": "http://blext.herokuapp.com/api/v1.0/category/1",
	            "draft": false,
	            "id": 1,
	            "summary_text": "<summary text>",
	            "tags": "http://blext.herokuapp.com/api/v1.0/tags/1",
	            "timestamp": "Sun, 27 Nov 2016 03:12:45 GMT",
	            "title": "<title>",
	            "url": "http://blext.herokuapp.com/api/v1.0/blogs/1"
	        },

	        {
	            "author": "http://blext.herokuapp.com/api/v1.0/user/",
	            "body": "<blog body>",
	            "category": "http://blext.herokuapp.com/api/v1.0/category/2",
	            "draft": false,
	            "id": 2,
	            "summary_text": "<summary text>",
	            "tags": "http://blext.herokuapp.com/api/v1.0/tags/2",
	            "timestamp": "Sun, 27 Nov 2016 03:12:45 GMT",
	            "title": "<title>",
	            "url": "http://blext.herokuapp.com/api/v1.0/blogs/2"
	        }
	    ],
	    "count": 2,
	    "next": null,
	    "prev": null
	}

Each blog included in the ``blogs`` list contains the information below.

+--------------+---------+--------------------------------------------------------------+
| Name         | Type    | Description                                                  |
+==============+=========+==============================================================+
| author       | string  | The API URL with which you can get the author's information. |
+--------------+---------+--------------------------------------------------------------+
| body         | string  | The blog's body, in pure text.                               |
+--------------+---------+--------------------------------------------------------------+
| category     | string  | The API URL with which you can get the blog's category.      |
+--------------+---------+--------------------------------------------------------------+
| draft        | boolean | Whether this blog is a draft.                                |
+--------------+---------+--------------------------------------------------------------+
| id           | int     | The blog's id, with which you can get an particular blog.    |
+--------------+---------+--------------------------------------------------------------+
| summary_text | string  | The blog's summary, in pure text.                            |
+--------------+---------+--------------------------------------------------------------+
| tags         | string  | The API URL with which you can get the blog's tags.          |
+--------------+---------+--------------------------------------------------------------+
| timestamp    | string  | The time this blog was initially built.                      |
+--------------+---------+--------------------------------------------------------------+
| title        | string  | The blog's title.                                            |
+--------------+---------+--------------------------------------------------------------+
| url          | string  | The API URL with which you can get this blog.                |
+--------------+---------+--------------------------------------------------------------+

Note that not all the blogs are served at one time if the total amount exceeds a particular number. Instead, blogs are served in pagination. Refer to the URL provided in ``prev`` and ``next`` for a new page of blogs if any.

.. _get a single blog:

Get a Single Blog
~~~~~~~~~~~~~~~~~~~~~~
Getting a single blog is as easy as getting them all, except that a blog id must be followed.

.. code-block:: shell

	$ http --json --auth token: GET https://blext.herokuapp.com/api/v1.0/blogs/1
	HTTP/1.1 200 OK
	Connection: keep-alive
	Content-Length: 583
	Content-Type: application/json
	Date: Tue, 06 Dec 2016 09:19:30 GMT
	Server: gunicorn/18.0
	Via: 1.1 vegur

	{
        "author": "http://blext.herokuapp.com/api/v1.0/user/",
        "body": "<blog body>",
        "category": "http://blext.herokuapp.com/api/v1.0/category/1",
        "draft": false,
        "id": 1,
        "summary_text": "<summary text>",
        "tags": "http://blext.herokuapp.com/api/v1.0/tags/1",
        "timestamp": "Sun, 27 Nov 2016 03:12:45 GMT",
        "title": "<title>",
        "url": "http://blext.herokuapp.com/api/v1.0/blogs/1"
    }


.. _get a blog's category:

Get a Blog's Category
~~~~~~~~~~~~~~~~~~~~~~
With a blog id followed.

.. code-block:: shell	

	$ http --json --auth token: GET https://blext.herokuapp.com/api/v1.0/category/1
	HTTP/1.1 200 OK
	Connection: keep-alive
	Content-Length: 22
	Content-Type: application/json
	Date: Tue, 06 Dec 2016 09:22:02 GMT
	Server: gunicorn/18.0
	Via: 1.1 vegur

	{
	    "name": "First"
	}

.. _get a blog's tags:

Get a Blog's Tags
~~~~~~~~~~~~~~~~~~~~~~
With a blog id followed.

.. code-block:: shell

	$ http --json --auth token: GET https://blext.herokuapp.com/api/v1.0/tags/1
	HTTP/1.1 200 OK
	Connection: keep-alive
	Content-Length: 87
	Content-Type: application/json
	Date: Tue, 06 Dec 2016 09:23:19 GMT
	Server: gunicorn/18.0
	Via: 1.1 vegur

	{
	    "tags": [
	        {
	            "name": "first"
	        },
	        {
	            "name": "my"
	        }
	    ]
	}


.. _publish a new blog:

Publish a New Blog
~~~~~~~~~~~~~~~~~~~~~~
A ``POST`` method is needed to publish a new blog. On publishing, make sure your data includes both *blog body* and *draft* value indicating whether you want to publish this blog as a draft or not.

.. code-block:: shell

	$ http --json --auth token: POST https://blext.herokuapp.com/api/v1.0/blogs/ \
	> "body=<body>" \
	> "draft=false"

If your *blog body* is properly composed according to the :ref:`blog format <blog format>`, the response will contain the Location of this new blog with a status code 201. Otherwise, an error response will be sent.

.. _update an existing blog:

Update an Existing Blog
~~~~~~~~~~~~~~~~~~~~~~~~~
Updating an existing blog is pretty much the same as creating a new one. Except that if an existing blog is to be updated, a blog id should be provided. Besides, you should use ``PUT`` instead of ``POST`` to update an existing blog.

.. code-block:: shell

	$ http --json --auth token: PUT https://blext.herokuapp.com/api/v1.0/blogs/1 \
	> "body=<body>" \
	> "draft=false"

And everything else including the response is the same as creating a new blog.
