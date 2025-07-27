# Stage 1: Build the React app
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app/frontend

# Install dependencies
COPY package.json bun.lockb ./
RUN npm install -g bun
RUN bun install

# Copy source code and build
COPY . .
RUN bun run build

# Stage 2: Serve with NGINX
FROM nginx:stable-alpine

# Copy custom NGINX config (optional)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy React build from Stage 1
COPY --from=build /app/frontend/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
