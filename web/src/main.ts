import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 导入Element Plus的图标
import * as ElementPlusIcons from '@element-plus/icons-vue'

const app = createApp(App)

// 注册所有Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIcons)) {
  app.component(key, component)
}

app.use(router)
app.use(ElementPlus)

app.mount('#app')
