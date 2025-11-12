# Use a Node base image
FROM node:20-alpine

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first (for caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the source code
COPY . .

# Expose Angular dev server port
EXPOSE 4200

# Default command to run Angular dev server (include reloading for hotfix)
CMD ["npx", "ng", "serve", "--host", "0.0.0.0", "--poll=2000"]
