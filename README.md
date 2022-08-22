# Proofscape Manage

Proofscape Manage is intended for use by anyone interested in developing for the
Proofscape projects. Its purpose is to help you set up and manage a development
environment. It is designed for Unix-based systems, such as Linux or macOS.
If anyone with expertise would like to help develop a Windows version, this would
be most welcome.

You must have `git` and `docker` already installed. You need the ability to install
a Python 3.8 virtual environment. If you want to develop client-side code, you
need `npm`.

You will also need a good internet connection, as various steps involve pulling
git repos, libraries from package repositories, and large Docker images from the
web.


## Root Directory

Choose a place in your filesystem for Proofscape to live. We recommend
`~/proofscape`, but you can choose any directory you want. For the remainder
of this guide, we will refer to this directory as `PFSC_ROOT`.

When making your choice, bear in mind that all of your Proofscape _content_
repos (if you plan on developing content) will live under `PFSC_ROOT/lib`,
while all the source repos will live under `PFSC_ROOT/src`. So choose a
convenient location.


## Clone this repo, under the root dir

Make the root directory if it doesn't already exist, `cd` into it, and clone this
repo there.

    $ mkdir PFSC_ROOT
    $ cd PFSC_ROOT
    $ git clone https://github.com/proofscape/pfsc-manage.git


## Establish and activate a virtual environment

This project is designed for Python 3.8. If this is not available on
your system, we recommend using [`pyenv`](https://github.com/pyenv/pyenv) to
make it available.

Here and later in this guide, we will write a `pyenv` line to remind you to
use the right version of Python. If you choose to use an alternative way of
setting up a Python virtual environment at the desired version, you can ignore
these lines.

Set up the virtual environment as follows:

    $ cd pfsc-manage
    $ pyenv shell 3.8.12
    $ python -m venv venv
    $ . venv/bin/activate
    (venv) $ pip install -U pip
    (venv) $ pip install -e .

The last command performs a local installation of the `pfsc-manage` package
defined in this project. (See `setup.py` and `manage.py`.) This provides you
with a command line tool, `pfsc`, which you can use to perform all actions
necessary to set up the development environment, build docker images, run
container networks, etc.


## Make a `conf.py`

Make a copy of the sample config file, at the top level of `pfsc-manage`:

    $ cp sample_conf.py conf.py

The copy _must_ be called `conf.py`.

You can use `conf.py` to make various settings, which should help you tailor
the tools provided by this repo to your use cases.

Note that `conf.py` is listed in `.gitignore`. It is not under
version control, so you should make backup copies as you see fit.

### Multiple configurations

Alternatively, you may make as many copies of `sample_conf.py` as
you want, and store them in the `conf_dir` directory under any names you
choose. `*.py` files in this directory are ignored by `git`, so you should
again make your own backup copies.

Under this design, the `conf.py` at the top level of the project should not
be a file, but a symlink to one of the modules you define in `conf_dir`.


## Build the directory structure

A working Proofscape system needs several subdirectories under `PFSC_ROOT`.
To make these, simply use:

    (venv) $ pfsc makestruct

Note 1: Whenever you want to use the `pfsc` tool, the virtual environment
always needs to be active. This is indicated by the `(venv) $` prompt.

Note 2: If you followed the recommended practice and put this repo (`pfsc-manage`)
directly under `PFSC_ROOT`, then the `pfsc makestruct` command will automatically
find the root dir, and figure out where to make all the subdirs. If you did it
differently, then you'll have to run `pfsc makestruct --help` for help on making
it work.

After running the `pfsc makestruct` command you should now have the following
directory structure:

    PFSC_ROOT
     |-- build
     |-- deploy
     |    |-- .ssl
     |-- graphdb
     |-- lib
     |-- PDFLibrary
     |-- pfsc-manage
     |-- src
          |-- tmp


## Clone source repos

The purpose of the `PFSC_ROOT/src` dir is to be the home of any and all cloned
source repos on which you are working, or which are needed for building Docker
images. You're going to need at least the
`pfsc-server` repo, so go ahead and run

    (venv) $ pfsc repo clone server

Afterward you might want to quickly `cd` into `PFSC_ROOT/src` and check that you
did indeed get a cloned copy of the `pfsc-server` Git repo.

If you are also interested in doing client-side development then you should also

    (venv) $ pfsc repo clone ise
    (venv) $ pfsc repo clone moose

in order to clone the `pfsc-ise` and `pfsc-moose` repos.

Note that these commands aren't doing anything too fancy. They are just `cd`-ing
into `PFSC_ROOT/src` and then running `git clone` with the approrpiate `URLs`. If
you wanted to, you could do this manually instead.


## Install Dependencies

Install the dependencies for any repos you have cloned.

### `pfsc-server`

Like `pfsc-manage`, `pfsc-server` is a Python project. We therefore recommend
opening a new terminal tab, so that you can have a different virtual environment
active in each one. If you don't want to do that, you can always

    (venv) $ deactivate

before switching between projects.

Now enter the `pfsc-server` project directory, and install the dependencies:

    $ cd PFSC_ROOT/src/pfsc-server
    $ pyenv shell 3.8.12
    $ python -m venv venv
    $ . venv/bin/activate
    (venv) $ pip install -U pip
    (venv) $ pip install -r req/dev.txt
    (venv) $ pip install -r req/run.txt

### `pfsc-ise`

For the JavaScript projects, you need `npm`.

    $ cd PFSC_ROOT/src/pfsc-ise
    $ npm install

### `pfsc-moose`

    $ cd PFSC_ROOT/src/pfsc-moose
    $ npm install


## Build Docker images

For most development tasks you're going to need at least the `pfsc-server`
Docker image. The first time you build this can be quite slow, since we need
to begin by pulling base images.

First make sure the `DOCKER_CMD` setting in your `conf.py` is what it needs
to be (see comments in `conf.py`).

You're encouraged to look at

    (venv) $ pfsc build server --help

and read about options that may eventually become relevant for you, but in
order to get started quickly just do

    (venv) $ pfsc build server latest

Again, this may take a while.


## Make a first deployment directory

One of the main services provided by the `pfsc-manage` project is to automatically
generate deployment code. This includes docker-compose YAMLs, Nginx confs, `.env`
files, and more.

The command that generates all these files for you is `pfsc deploy generate`, and
you can learn a lot from

    (venv) $ pfsc deploy generate --help

The expectation is that you will use `pfsc deploy generate` many times. Each time
you use it, it generates a new directory under `PFSC_ROOT/deploy`. You can either
set the name of the generated directory using the `--dirname` option, or else let
its name be automatically generated, using random words and a timestamp.

We will refer to each such directory as a _deployment directory_.
You can feel free to delete these directories any time you want, but do not rename
them, since their names are built into the code they contain, and they will not
work if renamed.

In order to generate your first deployment directory, run

    (venv) $ pfsc deploy generate

and accept the default setting for each interactive prompt that comes up (just hit
enter/return on each one). Now `cd` to `PFSC_ROOT/deploy` and you should see the new
directory. Its name will consist of random words and a timestamp.

For the remainder of this guide we will refer to the deployment directory you just
generated as `FIRST_DEPLOY_DIR`.

Before we move on, you should `cd` into `FIRST_DEPLOY_DIR` and take a look around.
Examine the contents of each of the generated files, and understand (or at least guess)
what they will do for you.

Note that among the generated files is a copy of `conf.py` as it stood
at the time that you ran `pfsc deploy generate`. This should help you to recreate the
same deployment later, if need be.


## Set up databases

THIS SECTION IS OPTIONAL

Depending on how you will set up your graph database (gdb), you may want to
define indexes to accelerate queries.
Now that we have a deployment directory (which defines the location of the
gdb, among  other things), we can do this as follows.

### Defining indexes if using Neo4j

NOTE: If you accepted the default settings when you ran `pfsc deploy generate`,
then you are _not_ using Neo4j, and should skip this section.

If you are going to use Neo4j as your graph database engine, and want to define
indexes to accelerate queries, you can proceed as follows.

First, we need a Neo4j container to be running.
Therefore do the following:

    (venv) $ cd PFSC_ROOT/deploy/FIRST_DEPLOY_DIR/layers
    (venv) $ ./dc 100_db.yml up
    (venv) $ pfsc gdb setup

Here you are using the automatically generated `dc` script to bring up just the
database layer of containers, before asking `pfsc gdb setup` to make the desired
indexes in the graph database.

Before taking down the Neo4j container, you might want to navigate to
`localhost:7474` in a web browser (substitute your chosen port number if you changed
this setting in your `conf.py`) and run

    CALL db.indexes()

in the Neo4j interactive browser, in order to see the indexes you just made.

In any case, when you're ready, take the database layer down with

    (venv) $ ./dc 100_db.yml down

### Coming soon...

Support for setting up other graph databases...



## Local config

You will sometimes be running the Proofscape server locally (like when running
its unit tests) and sometimes in a Docker container (like when testing through
a web browser). Therefore each deployment dir contains two corresponding config
files, `local.env` and `docker.env`, as you can see in `FIRST_DEPLOY_DIR`.

You don't have to worry about using `docker.env`. It is volume-mounted into the
appropriate container(s) by the `docker-compose` code in `FIRST_DEPLOY_DIR`, so
this is taken care of automatically.

You do however have to be conscious about the local configuration. Each time you
run `pfsc deploy generate`, the `local.env` for your new deployment dir is symlinked
into `PFSC_ROOT/src/pfsc-server/instance/.env` (unless you use the `-L`
or `--no-local` flag). This means that in general _the most recently generated
deployment dir is the one whose `local.env` will configure the Proofscape server
during unit tests_.

If you want to reactivate the `local.env` from an older deployment dir, you can
always do this using the `pfsc deploy local` command. For example, suppose you
have

    PFSC_ROOT
     |-- deploy
          |-- foo
          |-- bar

and `bar`'s `local.env` is currently active. (Again, this simply means that the
symlink at `PFSC_ROOT/src/pfsc-server/instance/.env` currently points to it.)
If you wanted to instead reactivate `foo`'s `local.env`, you could do this with

    (venv) $ pfsc deploy local foo

In fact even

    (venv) $ pfsc deploy local f

would work, since, rather than spelling out the entire name of the desired
deployment dir, any prefix that uniquely determines the directory will work.


## Under construction

More sections to this guide will be coming soon. In the meantime we invite you
to use [the Discussions tab for this repo](https://github.com/proofscape/pfsc-manage/discussions)
if you need help.
