FROM node:22-alpine

WORKDIR /frontend

COPY system/application/frontend/package.json system/application/frontend/package-lock.json* ./
RUN npm install

COPY system/application/frontend .

EXPOSE 3000

CMD ["npm", "run", "dev"]