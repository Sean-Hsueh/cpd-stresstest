apk add git 

export GIT_SSL_NO_VERIFY=1

git config --global credential.username $GIT_USERNAME
git config --global credential.helper "!echo password=$GIT_PASSWORD; echo"
git clone https://gitlab.nchc.org.tw/cp4d/selenium-script.git /tmp/selenium-script

pip install /tmp/selenium-script
pip install selenium pytz


