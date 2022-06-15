const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: "0.0.0.0",
    port: 8080,
    https: false,
    proxy: {
      '/api': {target: 'http://0.0.0.0:5000/'
      },
    },
    headers: {
      "Access-Control-Allow-Origin": "http://0.0.0.0:5000",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
      "Access-Control-Allow-Headers": "Origin, X-Requested-With, content-type, Authorization",
      'Access-Control-Allow-Credentials': true,
    },
  },
})
// module.exports = {
//   transpileDependencies: ["vuetify"],
//   devServer: {
//     host: "localhost", // frontend hostname or ip
//     // disableHostCheck: true,
//     port: 8080, // frontend port
//     https: false, // no ssl
//     proxy: {
//       "/api": {
//         // proxy everything from frontend http://localhost:8080/api/** to backend at http://localhost:8081/api/**
//         // that is why all api path on backend should begin with /api
//         target: "http://0.0.0.0:5000",
//       },
//     },
//     headers: {
//       "Access-Control-Allow-Origin": "*",
//       "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
//       "Access-Control-Allow-Headers": "Origin, X-Requested-With, content-type, Authorization",
//     },
//   },
// };
