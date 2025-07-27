# Stage 1: Build the React app
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app/frontend

# Copy package.json and the lock file to leverage Docker cache
COPY package.json bun.lockb ./

# Install bun globally
RUN npm install -g bun

# Install project dependencies using bun
RUN bun install

# Copy the rest of the source code into the container
COPY . .

# Build the React application for production
RUN bun run build

# Stage 2: Serve the application with a Node.js server
FROM node:18-alpine

# Set the working directory for the server
WORKDIR /app

# Install 'serve', a production-ready static file server
RUN npm install -g serve

# Copy the built application from the 'build' stage to the current stage
COPY --from=build /app/frontend/dist .

# Expose the port that the server will run on
EXPOSE 80

# Command to run the server
# The '-s' flag handles SPA routing by redirecting all requests to index.html
CMD ["serve", "-s", ".", "-l", "80"]
