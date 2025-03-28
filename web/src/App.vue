<script setup lang="ts">
import { onMounted } from 'vue'

// 页面加载完成后应用动画
onMounted(() => {
  document.body.classList.add('app-loaded')
})
</script>

<template>
  <div class="app-wrapper">
    <RouterView v-slot="{ Component }">
      <transition name="fade-slide" mode="out-in">
        <component :is="Component" />
      </transition>
    </RouterView>
  </div>
</template>

<style scoped>
:root {
  --primary-color: #409EFF;
  --primary-gradient: linear-gradient(90deg, #409EFF 0%, #53a8ff 100%);
  --secondary-color: #67C23A;
  --warning-color: #E6A23C;
  --danger-color: #F56C6C;
  --info-color: #909399;
  --background-gradient: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  --card-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  --header-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  --footer-shadow: 0 -4px 12px rgba(0, 0, 0, 0.03);
  --border-radius-sm: 8px;
  --border-radius-md: 12px;
  --border-radius-lg: 16px;
  --transition-fast: all 0.2s ease;
  --transition-normal: all 0.3s ease;
  --transition-slow: all 0.5s ease;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  scroll-behavior: smooth;
  background: var(--background-gradient);
  color: #303133;
}

#app, .app-wrapper {
  height: 100%;
}

/* 全局转场动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

body {
  opacity: 0;
  transition: opacity 0.8s ease;
}

body.app-loaded {
  opacity: 1;
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-thumb {
  background: #c0c4cc;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #909399;
}

::-webkit-scrollbar-track {
  background: #f5f7fa;
  border-radius: 4px;
}

/* 公共动画类 */
.hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* 响应式布局辅助类 */
@media (max-width: 768px) {
  .hide-on-mobile {
    display: none !important;
  }
}

@media (min-width: 769px) {
  .show-on-mobile {
    display: none !important;
  }
}
</style>
