# leto-modelizer-ia-api

## Description

This file describes how to contribute and develop for this open-source project.

### Requirements

* pipenv

    Install pipenv:  ``` pip install pipenv ```

    Create virtual environment and install dependencies from your repo: ``` pipenv install ```

    Install dev dependencies: ``` pipenv install --dev ```

    Activate virtual environment: ``` pipenv shell ```

    To deactivate your virtual environment: ``` deactivate ```

## Checkstyle

Before pushing your branch and open/synchronize a pull-request, you have to verify the checkstyle of your application. Here is the command to do so (on the root folder):

```shell
black .
```

## Dependencies update

You can check update of your code dependencies by running this command:

```shell
pipenv check
```

## How to launch unit tests

In order to launch the tests, you must be in the DataCollector root folder and from it, you have to launch the following command:
```sh
pytest
```

To launch it with the coverage:
```sh
pytest --cov=. --cov-report term-missing
```

To launch it with the coverage and generate an HTML report:
```sh
pytest --cov=. --cov-report term-missing --cov-report html
firefox htmlcov/index.html
```

## How to release

We use [Semantic Versioning](https://semver.org/spec/v2.0.0.html) as guideline for the version management.

Steps to release:
- Create a new branch labeled `release/vX.Y.Z` from the latest `main`.
- Improve the version number in `package.json`, `package-lock.json` and `changelog.md`.
- Verify the content of the `changelog.md`.
- Commit the modifications with the label `Release version X.Y.Z`.
- Create a pull request on GitHub for this branch into `main`.
- Once the pull request validated and merged, tag the `main` branch with `vX.Y.Z`.
- After the tag is pushed, make the release on the tag in GitHub.

## Git: Default branch

The default branch is `main`. Direct commit on it is forbidden. The only way to update the application is through pull request.

Release tags are only done on the `main` branch.

## Git: Branch naming policy

`[BRANCH_TYPE]/[BRANCH_NAME]`

* `BRANCH_TYPE` is a prefix to describe the purpose of the branch. Accepted prefixes are:
  * `feature`, used for feature development
  * `bugfix`, used for bug fix
  * `improvement`, used for refacto
  * `library`, used for updating library
  * `prerelease`, used for preparing the branch for the release
  * `release`, used for releasing project
  * `hotfix`, used for applying a hotfix on main
* `BRANCH_NAME` is managed by this regex: `[a-z0-9._-]` (`_` is used as space character).