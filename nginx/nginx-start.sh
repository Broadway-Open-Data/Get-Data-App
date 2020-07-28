sudo nginx -c $(pwd)/nginx.conf -g 'daemon off;' -p $(pwd)
echo "**** Server is running! ****"
