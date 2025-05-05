FROM nginx:alpine

COPY ./sites/ /usr/share/nginx/html/sites/
COPY ./index.html /usr/share/nginx/html/index.html
COPY ./login.html /usr/share/nginx/html/login.html

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
