# Client Dockerfile

FROM node:latest as build

WORKDIR /client

# Add node_modules/.bin to PATH
ENV PATH /client/node_modules/.bin:$PATH

# Install dependencies
COPY package.json ./
#COPY package-lock.json ./

RUN npm install && \
    npm install react-scripts@3.4.1 -g

# Copy the source code to container
COPY . /client

# Build production
RUN npm run build

# Setup NGINX as a proxy server to serve the app
FROM nginx:latest as prod

COPY --from=build /client/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

# Expose HTTP port
EXPOSE 80

# Start NGINX on container start
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]