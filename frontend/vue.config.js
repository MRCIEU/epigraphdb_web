module.exports = {
  devServer: {
    disableHostCheck: true
  },
  chainWebpack: config => {
    config.module
      .rule("raw")
      .test(/\.md$/)
      .use("raw-loader")
      .loader("raw-loader")
      .end();
    config.module
      .rule("vue")
      .use("vue-loader")
      .loader("vue-loader")
      .tap(options => {
        options.prettify = false;
        return options;
      });
  }
};
