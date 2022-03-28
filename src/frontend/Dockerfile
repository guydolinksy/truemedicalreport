FROM node:17-alpine AS dev
WORKDIR /opt/frontend/tmr

COPY frontend /opt/frontend
RUN npm i

ENV WDS_SOCKET_PORT=80

CMD npm start
