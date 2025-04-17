# Use Node.js base image
FROM node:20

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy rest of the app
COPY . .

# Expose port (adjust if different)
EXPOSE 3000

# Start the app (adjust if using vite, bun, or another)
CMD ["npm", "run", "dev"]

# Copy the start script
COPY start.sh .

# Make the script executable
RUN chmod +x start.sh

# Run both services
CMD ["./start.sh"]
