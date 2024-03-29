# Selenium Script

## Prepare Python virtual env

```shell
$ python3 -m venv selenium-venv
$ source selenium-venv/bin/active
$ pip3 install pytz jupyter selenium

# install local DasUITesting package
$ pip3 install .
```

## Create python script from ipynb

```shell
$ make nb_convert_py

```

## Create script configmap

```shell
$ make configmap

$ oc apply -f selenium-chrome-standalone.yaml
$ oc apply -f selenium-py.yaml
$ oc logs selenium -f

```

## Use Docker

### Launch Remote Browser Driver

Port 4444 is Remote Browser Driver port, 5900 is vnc server port.
You can see browser behavior by using VNC viewer connect to localhost:5900.

```
$ cd selenium-script

$ docker run  -ti -p 4444:4444 -p 5900:5900  --shm-size=2g --rm selenium/standalone-chrome-debug:latest
```

### Run Selenium script

- environment variables

  - `CASE`: `project` or `notebook`
  - `DAS_INSTANCE`: CPD instance URL
  - `DAS_USER`: CPD username
  - `DAS_PASSWORD`: CPD user password
  - `REMOTE_EXECUTOR`: Selenium remote browser driver. You can use docker command to create one.

- run script

  ```
  $ cd selenium-script
  $ docker run  -ti --rm \
      -v `pwd`:/tmp/selenium-script  \
      -e DAS_INSTANCE="https://cpd.org.tw" \
      -e DAS_USER=user \
      -e DAS_PASSWORD=password \
      -e REMOTE_EXECUTOR="http://host.docker.internal:4444/wd/hub" \
      -e CASE=notebook \
      python:3-alpine sh /tmp/selenium-script/docker/bootstrap.sh


  ```
