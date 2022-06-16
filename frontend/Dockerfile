FROM node:16 as builder

CMD mkdir /app
WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install
COPY . ./
RUN yarn build

FROM nginx:1.21-alpine
COPY --from=builder /app/dist/ /usr/share/nginx/html