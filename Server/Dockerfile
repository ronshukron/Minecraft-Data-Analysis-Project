# Use the official Node.js image as the base image
FROM node:20

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    if [ ! -e /usr/bin/python ]; then ln -s /usr/bin/python3 /usr/bin/python; fi

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Copy app source
COPY . .

# Expose port
EXPOSE 8080

# Start the application
CMD [ "node", "server.js" ]
