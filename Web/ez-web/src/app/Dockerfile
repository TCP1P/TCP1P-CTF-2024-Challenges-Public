# Base image
FROM node:20

# Create app directory
WORKDIR /app/

# Install app dependencies
COPY . .

RUN npm install

CMD [ "node", "./app.js" ]
