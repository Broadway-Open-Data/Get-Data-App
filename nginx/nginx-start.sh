# On ec2, run this file in a detached session (screen -S nginx)
# Run this command from this file...
echo "**** Server is running! ****"
sudo nginx -c $(pwd)/nginx.conf -g 'daemon off;' -p $(pwd)

# Run this command from the user root (SSH in...)
# sudo nginx -c /home/ec2-user/MVP-FrontEnd/nginx/nginx.conf -g 'daemon off;' -p  /home/ec2-user/MVP-FrontEnd/

# Am currently using the following to reload my nginx
sudo service nginx reload
