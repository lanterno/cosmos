# cosmos-BE

[![Build Status](https://travis-ci.org/zee93/cosmos-BE.svg?branch=master)](https://travis-ci.org/zee93/cosmos-BE)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Cosmos, sheetu, or time 2.0... anyway, this is an application about controlling time.. Check out the project's [documentation](http://zee93.github.io/cosmos-BE/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  
- [Travis CLI](http://blog.travis-ci.com/2013-01-14-new-client/)
- [Heroku Toolbelt](https://toolbelt.heroku.com/)

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Continuous Deployment

Deployment is automated via Travis. When builds pass on the master or qa branch, Travis will deploy that branch to Heroku. Follow these steps to enable this feature.

Initialize the production server:

```
heroku create cosmos-prod --remote prod && \
    heroku addons:create newrelic:wayne --app cosmos-prod && \
    heroku addons:create heroku-postgresql:hobby-dev --app cosmos-prod && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="cosmos-prod" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="cosmos.config" \
        --app cosmos-prod
```

Initialize the qa server:

```
heroku create cosmos-qa --remote qa && \
    heroku addons:create newrelic:wayne --app cosmos-qa && \
    heroku addons:create heroku-postgresql:hobby-dev --app cosmos-qa && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="cosmos-qa" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="cosmos.config" \
        --app cosmos-qa
```

Securely add your Heroku credentials to Travis so that it can automatically deploy your changes:

```bash
travis encrypt HEROKU_AUTH_TOKEN="$(heroku auth:token)" --add
```

Commit your changes and push to master and qa to trigger your first deploys:

```bash
git commit -a -m "ci(travis): add Heroku credentials" && \
git push origin master:qa && \
git push origin master
```

You're now ready to continuously ship! ✨ 💅 🛳
