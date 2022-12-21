module.exports = {
  webpack: (config, env) => {
    // Load source maps in dev mode
    if (env === 'development') {
      config.module.rules.push({
        test: /\.(js|mjs|jsx|ts|tsx)$/,
        use: ['source-map-loader'],
        enforce: 'pre',
      });

      // For `babel-loader` make sure that sourceMap is true.
      config.module.rules = config.module.rules.map(rule => {
        // `create-react-app` uses `babel-loader` in oneOf
        if (rule.oneOf) {
          rule.oneOf.map(oneOfRule => {
            if (
              oneOfRule.loader &&
              oneOfRule.loader.indexOf('babel-loader') !== -1
            ) {
              if (oneOfRule.hasOwnProperty('options')) {
                if (oneOfRule.options.hasOwnProperty('sourceMaps')) {
                  // eslint-disable-next-line no-param-reassign
                  oneOfRule.options.sourceMaps = true;
                }
              }
            }
          });
        }
        return rule;
      });
    }

    return config;
  },
};
