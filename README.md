## IRS e-Services Mailbox Scraper

This is a screen scraper for the [IRS's e-Services Mailbox](https://www.irs.gov/tax-professionals/e-services-online-tools-for-tax-professionals). The mailbox website is used to distribute newer versions of Modernized e-File (MeF) schemas, business rules, and other files to people who have registered with the e-File program as software developers.

I wrote this scraper because the e-Services site is difficult and annoying to use, and because there's no easier way to get notification of incoming "mailbox" messages. Logging in requires a username, password, and five clicks, but it's easy to make a mistake or let your session time out, at which point you have to clear your cookies before trying again. This scraper will handle the whole login process, print a summary of the messages in your mailbox, and then download any attachments to the messages.

# Installation

This program is written in Python 3. If you haven't yet, install [Python 3](https://www.python.org/) and [pip](https://pip.pypa.io/). [Clone this repository](https://help.github.com/articles/cloning-a-repository/), start a command prompt in that directory, and install dependencies by running `pip -r requirements.txt`. (For bonus points, set up and activate an [isolated Python environment](https://virtualenv.pypa.io/en/stable/) first) Copy the file `credentials.yaml.sample` to `credentials.yaml`, then open it and fill in your username and password for the e-Services website. Finally, run `./crawl.py`.
