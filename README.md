# The Button

A simple time tracking service.

[![Requirements Status](https://requires.io/github/MashSoftware/the-button/requirements.svg?branch=main)](https://requires.io/github/MashSoftware/the-button/requirements/?branch=main)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N33KKEF)

## Prerequisites

### Required

- Python 3.7.x or higher
- Postgres 11.x.x or higher

### Optional

- Redis 6.0.x or higher (for rate limiting, otherwise in-memory storage is used)

## Getting started

### Create local Postgres database

```shell
sudo service postgresql start
sudo su - postgres -c "create user mash with password mash"
sudo su - postgres -c "createdb button"
sudo -u postgres psql
grant all privileges on database button to mash;
```

### Create venv and install requirements

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt ; pip3 install -r requirements_dev.txt
```

### Run database migrations

```shell
flask db upgrade
```

### Run app

```shell
flask run
```

## Testing

Run the test suite

```shell
python -m pytest --cov=app --cov-report=term-missing --cov-branch
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/MashSoftware/the-button/tags).

## How to contribute

If you want to contribute to this project, please review the [code of conduct](CODE_OF_CONDUCT.md) and [contribution guidelines](CONTRIBUTING.md).

## Contributors

- [@matthew-shaw](https://github.com/matthew-shaw) (Owner and maintainer)
- [@jonodrew](https://github.com/jonodrew)

## Thanks

- [@ahosgood](https://github.com/ahosgood)
- [@andymantell](https://github.com/andymantell)
- [@annie-birchall](https://github.com/annie-birchall)
- [@joehonywill](https://github.com/joehonywill)
- [@LlamaComedian](https://github.com/LlamaComedian)
- [@mattgirdler](https://github.com/mattgirdler)
- [@russwillis](https://github.com/russwillis)
- [@skipster2k2](https://github.com/skipster2k2)

## Support

This software is provided "as-is" without warranty. Support is provided on a "best endeavours" basis by the maintainers and open source community. Please see the [contribution guidelines](CONTRIBUTING.md) for how to raise a bug report or feature request.
