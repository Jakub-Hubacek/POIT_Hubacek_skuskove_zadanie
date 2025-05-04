# Use Nginx to serve static files
FROM nginx:alpine

# Copy build output to Nginx HTML directory
COPY ./sites/ /usr/share/nginx/html/sites/
COPY ./index.html /usr/share/nginx/html/index.html
COPY ./login.html /usr/share/nginx/html/login.html
# Expose port 80
EXPOSE 80
