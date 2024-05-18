# Use the official Node.js image as the base image
FROM node:20

# Install Python and virtualenv
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    if [ ! -e /usr/bin/python ]; then ln -s /usr/bin/python3 /usr/bin/python; fi

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Create and activate a virtual environment
RUN python -m venv /venv

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install the Python dependencies within the virtual environment
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Set the PATH to use the virtual environment
ENV PATH="/venv/bin:$PATH"

# Expose port
EXPOSE 8080

# Start the application
CMD [ "node", "server.js" ]
