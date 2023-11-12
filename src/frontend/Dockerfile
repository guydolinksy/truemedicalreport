FROM node:19.2 AS dev
WORKDIR /opt/frontend/frontend

COPY frontend/frontend/package.json /opt/frontend/frontend/package.json
COPY frontend/frontend/tsconfig.json /opt/frontend/frontend/tsconfig.json
COPY frontend/frontend/config-overrides.js /opt/frontend/frontend/config-overrides.js
RUN npm i --verbose

ENV WDS_SOCKET_PORT=80
ENV PORT=80
ENV NODE_OPTIONS="--openssl-legacy-provider"
CMD npm run start

FROM guydo/tmr-frontend:dev AS prod

COPY frontend/frontend/src /opt/frontend/frontend/src
COPY frontend/frontend/public /opt/frontend/frontend/public

RUN npm run build

CMD npm run serve
