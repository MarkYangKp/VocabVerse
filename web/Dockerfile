FROM node:20.9.0 AS build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install --registry=https://registry.npmmirror.com
# RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build-stage /app/dist /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]