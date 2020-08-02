FROM node:alpine3.12
WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /app/package.json
RUN npm install

COPY . .

CMD ["npm","start"]
