FROM node:18-alpine AS dev
WORKDIR /opt/frontend/tmr

COPY frontend/tmr/package.json /opt/frontend/tmr/package.json
RUN npm i

ENV WDS_SOCKET_PORT=80
ENV NODE_OPTIONS="--openssl-legacy-provider"
CMD npm start

FROM node:18-alpine AS build
WORKDIR /opt/frontend/tmr

COPY frontend/tmr/package.json /opt/frontend/tmr/package.json
RUN npm i

COPY frontend/tmr/src /opt/frontend/tmr/src
COPY frontend/tmr/public /opt/frontend/tmr/public
RUN npm build

FROM nginx:latest
COPY --from=build /opt/frontend/tmr/build /opt/frontend


