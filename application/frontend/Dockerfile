FROM node:22-alpine

WORKDIR /frontend

COPY ./application/frontend/package.json ./application/frontend/package-lock.json* ./
RUN npm install

COPY ./application/frontend .

EXPOSE 3000

CMD ["npm", "run", "dev"]