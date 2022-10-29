## 0.25.1 (------)

Features:

* Now use `tar` with symlink dereferencing to construct `docker build`
  contexts. This means that (a) source repos can live anywhere, as long as
  there is a symlink in `PFSC_ROOT/src` pointing to them, and (b) builds are
  much faster on Ubuntu nodes.


## 0.25.0 (221028)

Breaking Changes:

* In a move to no longer repeat ourselves with JS version numbers, we load JS
  assets in new ways ([#1](https://github.com/proofscape/pfsc-manage/pull/1)).

* The `pfsc license about` command is commented out. This is no longer needed,
  as the `pfsc-ise` and `pbe` projects now generate their own "About" dialogs.

Requires:

* `pfsc-server >= 0.25.0`
* `pfsc-ise >= 25.0`

## 0.24.0 (221016)

Features:

* Include `pfsc.ini` in dev bind mounts
* Improve `pfsc build oca`
* Improve EULA

Breaking Changes:

* Use updated URLs for `pfsc-pdf` and for `pfsc-server`'s native static assets.

Requires:

* `pfsc-server >= 0.24.0`
* `pfsc-ise >= 24.0`

## 0.23.3 (220920)

Features:

* Make RedisInsight optional in MCA deployments using RedisGraph.
* Improve the generated `admin.sh` script in deploy dirs, by giving
  complete set of bind mounts to the admin container.
* Make location of `graphdb` dir configurable.
