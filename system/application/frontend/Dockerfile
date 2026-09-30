FROM node:22-alpine

WORKDIR /frontend

ENV WATCHPACK_POLLING=true

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]