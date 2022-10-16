FROM node:latest AS dev
WORKDIR /opt/frontend/frontend

COPY frontend/frontend/package.json /opt/frontend/frontend/package.json
COPY frontend/frontend/config-overrides.js /opt/frontend/frontend/config-overrides.js
RUN npm i

ENV WDS_SOCKET_PORT=80
CMD npm run start

FROM node:latest AS build
WORKDIR /opt/frontend/frontend

COPY frontend/frontend/package.json /opt/frontend/frontend/package.json
COPY frontend/frontend/config-overrides.js /opt/frontend/frontend/config-overrides.js
RUN npm i

COPY frontend/frontend/src /opt/frontend/frontend/src
COPY frontend/frontend/public /opt/frontend/frontend/public

ENV NODE_OPTIONS="--openssl-legacy-provider"
RUN npm run build

FROM busybox:latest
WORKDIR /opt/static

COPY --from=build /opt/frontend/frontend/build /opt/static

CMD ["busybox", "httpd", "-f", "-v", "-p", "80"]
