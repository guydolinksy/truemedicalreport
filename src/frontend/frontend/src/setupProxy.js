/*
 Refer to
 https://create-react-app.dev/docs/proxying-api-requests-in-development#configuring-the-proxy-manually

 Sometimes we're running the proxy server locally, without k8s ingress / nginx
 */

const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  const proxy_port = process.env.REACT_APP_TMR_PROXY_BACKEND_TO_PORT;

  if (proxy_port) {
    console.info(`Proxying api to port ${proxy_port}`);
    const apiBaseUrl = `http://127.0.0.1:${proxy_port}`;

    app.use(
      createProxyMiddleware('/api', {
        target: apiBaseUrl,
      }),
    );

    app.use(
      createProxyMiddleware('/api/sync', {
        target: apiBaseUrl,
        ws: true,
      }),
    );
  }
};
