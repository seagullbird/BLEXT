User's Guide
=============
This guidance will help you go through BLEXT's features and things you should know quickly.

.. _blog format:

Blog Format
-----------
BLEXT use in-body header to indicate a blog's basic information including title, category and tags. In order to create a blog nicely, it is recommended to follow this format. (You can choose not to but the consequences are not foreseed.)

.. code-block:: text

	---
	title: <title>
	category: <category>
	tags: [<tag1>(,tag2, ...)]
	---
	[<summary>
	<!-- more -->]
	<blog-text>

And notice:

1. Content between ``---`` is called the header in BLEXT and should not be ignored.
2. ``summary`` is also meant to be created in markdown, and should always be tailed by ``<!-- more -->`` at the next line.
3. ``summary`` can be ignored, and if so, ignore ``<!-- more -->`` as well.
4. There can be as many tags as you want but only one category is needed.

An simple example:

.. code-block:: text

	---
	title: My First BLEXT Blog
	category: First
	tags: [tag1, tag2]
	---
	> This is my first BLEXT Blog!
	<!-- more -->
	## Hello World
	My **first** BLEXT blog is now established.
