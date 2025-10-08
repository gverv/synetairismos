const path = require("path");

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "../static/frontend"),
    filename: "bundle.js",
    publicPath: "/static/frontend/"
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: { loader: "babel-loader" }
      }
    ]
  },
  resolve: {
    extensions: [".js", ".jsx"]
  }
};
