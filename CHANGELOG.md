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
