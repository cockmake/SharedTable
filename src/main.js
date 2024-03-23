import {createApp} from 'vue'
import './style.css'
import 'element-plus/dist/index.css'
import App from './App.vue'
import axios from "axios";
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

axios.defaults.baseURL = 'http://support.forwardforever.top:5001'
// axios.defaults.baseURL = 'http://127.0.0.1:5001'
let app = createApp(App)
app.use(ElementPlus, {
    locale: zhCn,
})

app.mount('#app')

