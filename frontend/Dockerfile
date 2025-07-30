# Stage 1: Build the React app
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app/frontend

# Copy package.json and lock file
COPY package.json bun.lockb ./

# Install bun
RUN npm install -g bun

# Install dependencies
RUN bun install

# Copy the rest of the app
COPY . .

# Build the app
RUN bun run build

# Stage 2: Serve using Nginx
FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy the build output to nginx's public directory
COPY --from=build /app/frontend/dist /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
