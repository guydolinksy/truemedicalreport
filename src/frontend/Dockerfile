FROM node:17-alpine AS dev
WORKDIR /opt/frontend/tmr

COPY frontend/tmr/package.json /opt/frontend/tmr/
RUN npm i

COPY frontend/tmr/src /opt/frontend/tmr/src
COPY frontend/tmr/public /opt/frontend/tmr/public

ENV WDS_SOCKET_PORT=80
ENV NODE_OPTIONS="--openssl-legacy-provider"

CMD npm start
