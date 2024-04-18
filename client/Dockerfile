FROM node:20.12-slim

COPY package.json /client/

WORKDIR /client

RUN npm i
RUN npm i -g @angular/cli
COPY . /client

EXPOSE 4200
CMD ng serve --host 0.0.0.0