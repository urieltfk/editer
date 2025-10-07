FROM node:20-alpine

WORKDIR /app

COPY pnpm-lock.yaml package.json ./

RUN npm install -g pnpm
RUN pnpm i

COPY . .

EXPOSE 8000

CMD ["npm", "run", "dev"]

