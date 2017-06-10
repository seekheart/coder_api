# Coders Api

[![Build Status][travis]](https://travis-ci.org/seekheart/coder_api)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()


A restful api for serving data regarding coders and the programming languages
they know and can assist with. The api is primarily used by a discord bot
in the programming discussions discord for quick answers to questions such as
"who knows language X and can help me?" or "what languages does person X know?"

Additionally users can add additional data about what they know to the api
or update data about themselves through the api.

## Getting Started

You will need the following in order to run the api.

- [ ] Python 3.X
- [ ] Mongodb
- [ ] Virtualenv (optional but recommended)

## Installation

To begin if you are using virtualenv you can run:

```bash
virtualenv -p <path to python3> venv
source venv/bin/activate
```

This will spin up a virtual environment with python3 as your default python.

To install the packages and dependencies of the project run the following
at the project root:

```bash
pip install -r requirements.txt
```

## Running the app

Before you can run the app a few environment variables need to be set.
These variables are needed in order to set db and api credentials as well as app
specific settings.

The following variables need to be set.

* APP_ENV - mode in which the app should be run, defaults to dev
* HOST - host address to run app on, defaults to localhost or 0.0.0.0
* PORT - port number to run on, defaults to 3000
* API_USER - api security username for authorization
* API_PW - api security password for authorization
* MONGO_HOST - host address where mongodb is running
* MONGO_PORT - port number where mongodb is running
* MONGO_DB - name of the database in mongodb to use

In addition for `APP_ENV` this variable will determine whether the app outputs
debug messages if not in `PROD` and whether or not `MULTITHREADING` for 
concurrent calls will be allowed.

Finally you will need to have the following collections available in your
mongo database.

* users
* languages

## Author

* **Mike Tung** - *Main Developer* - [Github]

[Github]: https://github.com/seekheart
[travis]: https://travis-ci.org/seekheart/coder_api.svg?branch=master