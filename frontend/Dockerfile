# Use Node.js LTS base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the source code
COPY . .

# Build the Svelte app
RUN npm run build

# Expose the port the app will run on
EXPOSE 3000

# Start the server
CMD ["node", "build"]
