echo "**** Server is running! ****"
sudo nginx -c $(pwd)/nginx.conf -g 'daemon off;' -p $(pwd)
