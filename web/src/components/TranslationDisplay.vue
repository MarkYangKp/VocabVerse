<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { marked } from 'marked' // 新增: 引入 marked

const props = defineProps({
  translationData: {
    type: Object,
    default: null
  }
})

const languagePoints = ref<{ word: string, explanation: string }[]>([])
const translation = ref('')

// 监听传入的数据并更新组件状态
watch(() => props.translationData, (newData) => {
  if (newData) {
    languagePoints.value = newData.language_points || []
    translation.value = newData.translation || ''
  } else {
    languagePoints.value = []
    translation.value = ''
  }
}, { immediate: true, deep: true })

// 新增: 计算属性，将翻译内容转换为 HTML(markdown)
const translationHtml = computed(() => marked(translation.value || ''))

// 复制翻译内容
const copyTranslation = () => {
  if (translation.value) {
    navigator.clipboard.writeText(translation.value)
      .then(() => {
        ElMessage.success('翻译内容已复制到剪贴板')
      })
      .catch(() => {
        ElMessage.error('复制失败，请手动复制')
      })
  }
}
</script>

<template>
  <div v-if="translationData" class="translation-display">
    <!-- 单词解释部分 -->
    <div class="translation-section words-section">
      <div class="section-header">
        <h3>
          <el-icon><Collection /></el-icon>
          <span>单词解释</span>
        </h3>
      </div>
      
      <template v-if="languagePoints.length">
        <div class="words-list">
          <el-collapse accordion>
            <el-collapse-item 
              v-for="point in languagePoints" 
              :key="point.word"
            >
              <template #title>
                <div class="word-title">
                  <span class="word-text">{{ point.word }}</span>
                  <el-tag size="small" effect="plain" class="word-tag">词汇</el-tag>
                </div>
              </template>
              <div class="word-explanation-card">
                <div class="explanation-content">{{ point.explanation }}</div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </template>
      
      <div v-else class="empty-card">
        <el-empty description="没有单词解释数据" :image-size="80">
          <template #image>
            <el-icon class="empty-icon"><Document /></el-icon>
          </template>
        </el-empty>
      </div>
    </div>
    
    <!-- 文章翻译部分 -->
    <div class="translation-section article-section">
      <div class="section-header">
        <h3>
          <el-icon><Connection /></el-icon>
          <span>文章翻译</span>
        </h3>
        <el-button type="primary" size="small" @click="copyTranslation" class="copy-btn">
          <el-icon><CopyDocument /></el-icon>
          复制翻译
        </el-button>
      </div>
      
      <div class="translation-content-card">
        <template v-if="translation">
          <div class="translation-text" v-html="translationHtml"></div> <!-- 修改: 用 v-html 渲染 markdown -->
        </template>
        <template v-else>
          <div class="empty-card centered">
            <el-empty description="没有翻译数据" :image-size="80">
              <template #image>
                <el-icon class="empty-icon"><DocumentCopy /></el-icon>
              </template>
            </el-empty>
          </div>
        </template>
      </div>
    </div>
  </div>
  
  <div v-else class="loading-translation">
    <div class="loading-card top">
      <el-skeleton :rows="3" animated />
    </div>
    <div class="loading-card bottom">
      <el-skeleton :rows="6" animated />
    </div>
  </div>
</template>

<style scoped>
.translation-display {
  padding: 10px;
}

.translation-section {
  margin-bottom: 32px;
  transition: all 0.3s ease;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.section-header .el-icon {
  color: #409EFF;
}

.copy-btn {
  transition: all 0.2s ease;
  border-radius: 8px;
}

.copy-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.words-list {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.word-title {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 10px;
}

.word-text {
  font-weight: 500;
  font-size: 16px;
  color: #303133;
}

.word-tag {
  color: #409EFF;
  font-size: 12px;
}

.word-explanation-card {
  background: linear-gradient(to right, #f8f9fa, #eef2f8);
  border-radius: 8px;
  overflow: hidden;
}

.explanation-content {
  padding: 16px;
  line-height: 1.8;
  color: #303133;
  font-size: 15px;
}

.translation-content-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  min-height: 200px;
}

.translation-content-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.translation-text {
  line-height: 1.8;
  white-space: pre-wrap;
  color: #303133;
  font-size: 15px;
}

.empty-card {
  padding: 24px;
  background-color: #f9fafc;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.empty-card.centered {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 160px;
}

.empty-icon {
  font-size: 32px;
  color: #c0c4cc;
}

.loading-translation {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.loading-card {
  padding: 24px;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.loading-card.top {
  height: 180px;
}

.loading-card.bottom {
  height: 220px;
}

/* 增强响应式布局 */
@media (max-width: 991px) {
  .translation-content-card {
    padding: 20px;
  }
  
  .explanation-content {
    padding: 14px;
  }
}

@media (max-width: 768px) {
  .translation-display {
    padding: 5px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .section-header h3 {
    font-size: 16px;
  }
  
  .copy-btn {
    align-self: flex-end;
  }
  
  .translation-content-card {
    padding: 16px;
    min-height: 150px;
  }
  
  .translation-content-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    transform: none;
  }
  
  .word-text {
    font-size: 15px;
  }
  
  .translation-text {
    font-size: 14px;
    line-height: 1.6;
  }
  
  .empty-card {
    padding: 16px;
  }
}

@media (max-width: 576px) {
  .translation-section {
    margin-bottom: 20px;
  }
  
  .word-explanation-card {
    background: #f8f9fa;
  }
  
  .explanation-content {
    padding: 12px;
    font-size: 14px;
    line-height: 1.6;
  }
  
  .empty-icon {
    font-size: 24px;
  }
  
  .loading-card {
    padding: 16px;
  }
}
</style>
