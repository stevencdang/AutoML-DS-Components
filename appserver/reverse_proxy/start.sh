echo "Waiting 60 seconds to start nginx reverse proxy"
sleep 45s
echo "Starting nginx reverse proxy"
envsubst < /etc/nginx/conf.d/reverse_proxy.conf.template > /etc/nginx/conf.d/reverse_proxy.conf && exec nginx -g 'daemon off;'
