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

$ docker run  -d -ti -p 4444:4444 -p 5900:5900  --shm-size=4g --rm selenium/standalone-chrome-debug:latest

  docker run  -d -ti -p 4444:4444 -p 5900:5900  --shm-size=4g --rm selenium/standalone-chrome-debug:3.141.59-zinc

  docker run  -d -ti -p 4444:4444 -p 5900:5900  --shm-size=4g --rm seleniarm/standalone-chromium
  docker run  -d -ti --net=host  --shm-size=4g --rm seleniarm/standalone-chromium
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
      -e DAS_INSTANCE="https://cpd-cpd-instance.apps.cpd48anna.cp.fyre.ibm.com/" \
      -e DAS_USER=root \
      -e DAS_PASSWORD=HelloWorld2022! \
      -e REMOTE_EXECUTOR="http://host.docker.internal:4444/wd/hub" \
      -e CASE=notebook \
      python:3-alpine sh /tmp/selenium-script/docker/bootstrap.sh


  ```

docker run -ti --rm \
 -v /Users/sean/ibmWorkSpace/cpd-stresstest:/tmp/selenium-script \
 -e DAS_INSTANCE="https://cpd.org.tw" \
 -e DAS_USER=user \
 -e DAS_PASSWORD=password \
 -e REMOTE_EXECUTOR="http://host.docker.internal:4444/wd/hub" \
 -e CASE=notebook \
 python:3-alpine sh /tmp/selenium-script/docker/bootstrap.sh

docker run -ti --rm \
 -v C:\Users\157717\Downloads\cpd-healthcheck-main:/tmp/selenium-script \
 -e DAS_INSTANCE="https://cpd-cpd-instance.apps.cp4d2.hosp.ncku.edu.tw/zen/" \
 -e DAS_USER=STI9003 \
 -e DAS_PASSWORD=N123qweasdzxc \
 -e REMOTE_EXECUTOR="http://localhost:4444/wd/hub" \
 --net=host \
 -e CASE=notebook \
 python:3-alpine sh /tmp/selenium-script/docker/bootstrap.sh

docker run -ti --rm `
 -v ${PWD}:/tmp/selenium-script `
 -e DAS_INSTANCE="https://cpd-cpd-instance.apps.cp4d2.hosp.ncku.edu.tw/" `
 -e DAS_USER="STI9003" `
 -e DAS_PASSWORD="N123qweasdzxc" `
 -e REMOTE_EXECUTOR="http://localhost:4444/wd/hub" `
 --net=host `
 -e CASE="spss" `
 python:3-alpine sh /tmp/selenium-script/docker/bootstrap.sh
