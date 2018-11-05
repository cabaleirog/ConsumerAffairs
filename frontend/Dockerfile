FROM node:10

# RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY package.json /usr/src/app

RUN npm update -g @angular/cli
# RUN npm update
RUN npm install
# RUN npm audit fix  # FIXME

COPY . /usr/src/app

EXPOSE 4200

CMD ["npm", "start"]
