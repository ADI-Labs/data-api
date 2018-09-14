read -p 'uni: ' uni
read -sp 'password: ' password

echo '{"login":{"uni": $uni, "password": $password}}' > config.json

git pull origin master
git remote add dokku dokku@208.68.37.106:data-api
git push -f dokku master
git remote rm dokku