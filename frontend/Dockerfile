FROM node:22

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Levanta servidor de desarrollo
CMD ["npm", "run", "dev", "--", "--host"]
