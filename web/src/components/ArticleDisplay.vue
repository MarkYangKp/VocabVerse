<script setup lang="ts">
import { ref, watch } from 'vue'
import { marked } from 'marked'
import { ElMessage } from 'element-plus'

const props = defineProps({
  articleData: {
    type: Object,
    default: null
  }
})

const articleHtml = ref('')

// 将Markdown格式的文章转换为HTML，修改为异步方式
watch(() => props.articleData, async (newData) => {
  if (newData && newData.article) {
    articleHtml.value = await marked(newData.article)
  } else {
    articleHtml.value = ''
  }
}, { immediate: true, deep: true })

// 复制文章内容
const copyArticle = () => {
  if (props.articleData && props.articleData.article) {
    navigator.clipboard.writeText(props.articleData.article)
      .then(() => {
        ElMessage.success('文章内容已复制到剪贴板')
      })
      .catch(() => {
        ElMessage.error('复制失败，请手动复制')
      })
  }
}
</script>

<template>
  <div v-if="articleData" class="article-display">
    <div class="article-header">
      <div class="article-info-card">
        <div class="info-row">
          <div class="info-item">
            <el-icon><Reading /></el-icon>
            <span class="info-label">难度级别:</span>
            <span class="info-value">{{ articleData.passage_needs }}</span>
          </div>
          <div class="info-item">
            <el-icon><Document /></el-icon>
            <span class="info-label">文章类型:</span>
            <span class="info-value">{{ articleData.passage_type }}</span>
          </div>
          <div class="info-item">
            <el-icon><DocumentChecked /></el-icon>
            <span class="info-label">字数统计:</span>
            <span class="info-value">{{ articleData.word_count }}</span>
          </div>
        </div>
        <el-button type="primary" size="small" @click="copyArticle" class="copy-btn">
          <el-icon><CopyDocument /></el-icon>
          复制文章
        </el-button>
      </div>
    </div>
    
    <div class="article-content-card">
      <div v-html="articleHtml" class="markdown-content"></div>
    </div>
    
    <div v-if="articleData.alert" class="article-alert">
      <el-alert :title="articleData.alert" type="warning" :closable="false" effect="dark" />
    </div>
  </div>
  
  <div v-else class="loading-article">
    <div class="loading-card">
      <el-skeleton :rows="10" animated />
    </div>
  </div>
</template>

<style scoped>
.article-display {
  padding: 10px;
  /* width: 100vw; */
  transition: all 0.3s ease;
}

.article-header {
  margin-bottom: 20px;
}

.article-info-card {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(145deg, #f8f9fa, #eef2f8);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.article-info-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.info-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.info-item .el-icon {
  color: #409EFF;
}

.info-label {
  font-weight: 500;
  color: #606266;
}

.info-value {
  color: #409EFF;
  font-weight: 600;
}

.copy-btn {
  transition: all 0.2s ease;
  border-radius: 8px;
}

.copy-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.article-content-card {
  padding: 24px;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  min-height: 300px;
}

.article-content-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.article-alert {
  margin-top: 20px;
}

.markdown-content :deep(strong) {
  color: #409EFF;
  font-weight: 600;
  background: linear-gradient(transparent 70%, rgba(64, 158, 255, 0.2) 0%);
  padding: 0 2px;
}

.markdown-content :deep(p) {
  margin-bottom: 16px;
  line-height: 1.8;
  color: #303133;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4) {
  margin-top: 1.5em;
  margin-bottom: 0.8em;
  color: #303133;
}

.loading-article {
  padding: 20px;
}

.loading-card {
  padding: 24px;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

/* 增强响应式布局 */
@media (max-width: 991px) {
  .article-content-card {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .article-info-card {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
    padding: 16px;
  }
  
  .copy-btn {
    align-self: flex-end;
  }
  
  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .article-content-card {
    padding: 16px;
    min-height: 200px;
  }
  
  .article-content-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    transform: none;
  }
}

@media (max-width: 576px) {
  .article-display {
    padding: 5px;
  }
  
  .info-item {
    font-size: 13px;
  }
  
  .markdown-content :deep(p) {
    font-size: 14px;
    line-height: 1.6;
  }
  
  .markdown-content :deep(h1) {
    font-size: 1.4em;
  }
  
  .markdown-content :deep(h2) {
    font-size: 1.3em;
  }
  
  .markdown-content :deep(h3) {
    font-size: 1.2em;
  }
  
  .markdown-content :deep(h4) {
    font-size: 1.1em;
  }
}
</style>
