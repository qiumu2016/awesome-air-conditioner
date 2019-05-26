// vue.config.js
module.exports = {
    // 修改的配置
    // 将baseUrl: '/api',改为baseUrl: '/',
    // 改为'./'
    // 将baseUrl改为publicPath以解决build中出现的warning
    publicPath: './',
    //Django要求的静态资源文件夹
    assetsDir: 'static',
    devServer: {
        proxy: {
            '/api': {
                target: 'http://118.89.219.248:8080',
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                  '^/api': ''
                }
            }
        }
    }
}
// .env.development
//VUE_APP_BASE_API= /api
