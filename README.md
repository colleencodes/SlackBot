# SlackBot: Starter to Customized Bot

Writing a Slack bot seemed like a fun side project, so I found this tutorial online:

__'How to Build Your First Slack Bot with Python'__ by Matt Makai
<https://www.fullstackpython.com/blog/build-first-slack-bot-python.html>

It's a nice, small tutorial that makes getting one's first Slack bot up and running quickly an simple thing to do!

**24 February 2018**
Started the project yesterday, and got the first draft of it running today. Some things I noted that were different than the tutorial because I was developing on a Windows machine:
	..* to activate the virtualenv, use starterbot\Scripts\activate.bat instead of source starterbot/bin/activate
	..* to set an environment variable in Windows development, use `set <var_name>=<var_value>` instead of `export <var_name>=<var_value>`
	..* to create files from the command line, use `echo.><file_name>` (which is a file with one empty line) or `type nul > <file_name>` (0 byte file)
	<https://stackoverflow.com/questions/30011267/windows-equivalent-of-touch-i-e-the-node-js-way-to-create-an-index-html>
	..* Of particular importance for this project, I found out that the acronym **RTM** stands for **Real Time Messages**!
