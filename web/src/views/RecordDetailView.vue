<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import ArticleDisplay from '@/components/ArticleDisplay.vue'
import TranslationDisplay from '@/components/TranslationDisplay.vue'
import QuestionDisplay from '@/components/QuestionDisplay.vue'
import { getLearningRecord } from '@/utils/localStorageUtils'
import type { LearningRecord } from '@/utils/localStorageUtils'

const route = useRoute()
const router = useRouter()
const recordId = computed(() => route.query.id as string)
const record = ref<LearningRecord | null>(null)
const activeTab = ref('article')
const isLoading = ref(true)

// 格式化日期
const formatDate = (timestamp: number) => {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 加载记录详情
const loadRecord = () => {
  if (!recordId.value) {
    ElMessage.error('记录ID不能为空')
    router.push('/history')
    return
  }
  
  isLoading.value = true
  
  setTimeout(() => {
    const result = getLearningRecord(recordId.value)
    
    if (!result) {
      ElMessage.error('找不到该学习记录')
      router.push('/history')
      return
    }
    
    record.value = result
    isLoading.value = false
  }, 300)
}

// 返回历史记录页面
const goBack = () => {
  router.push('/history')
}

// 返回首页
const goHome = () => {
  router.push('/')
}

// 组件挂载时加载记录
onMounted(() => {
  loadRecord()
})
</script>

<template>
  <div class="record-detail-container">
    <el-container>
      <el-header height="auto" class="record-header">
        <div class="header-content">
          <div class="logo-area" @click="goHome">
            <el-icon class="logo-icon"><Connection /></el-icon>
            <h1>Word2LLM</h1>
          </div>
          <div class="header-title">
            <h2>学习记录详情</h2>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <div v-if="isLoading" class="loading-state">
          <el-skeleton :rows="15" animated />
        </div>
        
        <div v-else-if="record" class="record-detail-content">
          <div class="record-meta-card">
            <el-descriptions title="记录信息" :column="3" border>
              <el-descriptions-item label="创建时间">
                {{ formatDate(record.timestamp) }}
              </el-descriptions-item>
              <el-descriptions-item label="单词数量">
                {{ record.words.length }} 个单词
              </el-descriptions-item>
              <el-descriptions-item label="文章字数">
                {{ record.article.word_count }} 字
              </el-descriptions-item>
            </el-descriptions>
            
            <div class="word-list-display">
              <div class="section-title">
                <el-icon><Collection /></el-icon>
                <span>单词列表</span>
              </div>
              
              <div class="word-tags">
                <el-tag
                  v-for="(word, index) in record.words"
                  :key="word+index"
                  class="word-tag"
                  effect="light"
                >
                  {{ word }}
                </el-tag>
              </div>
            </div>
            
            <div class="record-actions">
              <el-button type="primary" @click="goBack">
                <el-icon><Back /></el-icon>
                返回历史记录
              </el-button>
            </div>
          </div>
          
          <div class="content-tabs-container">
            <el-tabs v-model="activeTab" type="border-card" class="content-tabs">
              <el-tab-pane label="文章阅读" name="article">
                <ArticleDisplay :article-data="record.article" />
              </el-tab-pane>
              
              <el-tab-pane label="翻译和解释" name="translation">
                <TranslationDisplay :translation-data="record.translation" />
              </el-tab-pane>
              
              <el-tab-pane label="练习题" name="questions">
                <div v-if="record.questions">
                  <QuestionDisplay :question-data="record.questions" />
                </div>
                <div v-else class="feature-unavailable">
                  <el-empty description="该记录没有练习题数据">
                    <template #image>
                      <el-icon class="empty-icon"><QuestionFilled /></el-icon>
                    </template>
                  </el-empty>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </div>
      </el-main>
      
      <el-footer class="app-footer">
        <div class="footer-content">
          <p>
            <el-icon><Connection /></el-icon>
            Word2LLM - 使用AI增强英语学习体验
          </p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<style scoped>
.record-detail-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
}

.record-header {
  padding: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  background: linear-gradient(90deg, #409EFF 0%, #53a8ff 100%);
  position: relative;
  overflow: hidden;
}

.record-header::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
  opacity: 0.6;
  pointer-events: none;
}

.header-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.logo-area:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 28px;
  color: #fff;
}

.record-header h1 {
  margin: 0;
  color: #fff;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: 1px;
}

.header-title h2 {
  margin: 10px 0 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 18px;
  font-weight: normal;
}

.record-detail-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.record-meta-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.word-list-display {
  margin-top: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.section-title .el-icon {
  color: #409EFF;
}

.word-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.word-tag {
  margin: 0;
}

.record-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}

.content-tabs-container {
  width: 100%;
}

.content-tabs {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  background-color: #fff;
}

.feature-unavailable {
  padding: 40px;
}

.empty-icon {
  font-size: 48px;
  color: #c0c4cc;
}

.loading-state {
  background-color: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.app-footer {
  padding: 24px;
  background-color: #fff;
  border-top: 1px solid #e4e7ed;
  margin-top: auto;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.03);
}

.footer-content {
  display: flex;
  justify-content: center;
  align-items: center;
}

.footer-content p {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  margin: 0;
}

.footer-content .el-icon {
  color: #409EFF;
}

@media (max-width: 768px) {
  .record-meta-card {
    padding: 16px;
  }
  
  .word-tags {
    gap: 6px;
  }
}
</style>
