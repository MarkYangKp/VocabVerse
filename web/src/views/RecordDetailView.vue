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
const activeTab = ref(route.query.tab?.toString() || 'article')
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

// 获取难度文本描述 - 适配新旧API格式
const getPassageNeedsText = (record: LearningRecord): string => {
  if (!record || !record.article) return '未知难度'
  
  // 优先使用新参数
  if (record.article.difficulty_level) {
    const difficultyMap: Record<string, string> = {
      'a1': 'CEFR A1 (初级)',
      'a2': 'CEFR A2',
      'b1': 'CEFR B1',
      'b2': 'CEFR B2',
      'c1': 'CEFR C1',
      'c2': 'CEFR C2',
      'easy': '简单',
      'intermediate': '中等',
      'advanced': '高级',
      'high_school': '高中水平',
      'cet4': '四级难度',
      'cet6': '六级难度',
      'graduate': '考研难度',
      'memory_friendly': '易于记忆'
    }
    return difficultyMap[record.article.difficulty_level] || record.article.difficulty_level
  }
  
  // 兼容旧参数
  const passageNeeds = Number(record.article.passage_needs)
  const needsMap: Record<number, string> = {
    1: '考研难度',
    2: '六级难度',
    3: '易于记忆',
    4: '四级难度',
    5: '高中水平'
  }
  return needsMap[passageNeeds] || '未知难度'
}

// 获取文章类型文本描述 - 适配新旧API格式
const getPassageTypeText = (record: LearningRecord): string => {
  if (!record || !record.article) return '未知类型'
  
  // 优先使用新参数
  if (record.article.article_type) {
    const typeMap: Record<string, string> = {
      'news': '新闻',
      'short_story': '短篇故事',
      'science': '科普文章',
      'blog': '博客/观点文',
      'academic': '学术论文',
      'email': '电子邮件/信件',
      'dialogue': '对话体',
      'argumentative': '议论文',
      'narrative': '叙事文',
      'descriptive': '描写文',
      'business': '商业报告',
      'technical': '技术报告',
      'editorial': '社论',
      'social_media': '社交媒体文案'
    }
    return typeMap[record.article.article_type] || record.article.article_type
  }
  
  // 兼容旧参数
  const passageType = Number(record.article.passage_type)
  const typeMap: Record<number, string> = {
    1: '议论文',
    2: '说明文',
    3: '短篇小说',
    4: '叙事文',
    5: '描写文',
    6: '商业报告',
    7: '技术报告',
    8: '新闻报道',
    9: '社论',
    10: '博客文章',
    11: '社交媒体文案'
  }
  return typeMap[passageType] || '未知类型'
}

// 页面标题计算属性
const pageTitle = computed(() => {
  if (!record.value) return '学习记录详情'
  return `学习记录 - ${formatDate(record.value.timestamp)}`
})

// 转换记录中的文章数据，确保类型兼容
const compatibleArticleData = computed(() => {
  if (!record.value || !record.value.article) return null
  
  const article = record.value.article
  
  // 创建一个新对象，确保类型兼容
  return {
    record_id: article.record_id,
    article_type: article.article_type || undefined,
    difficulty_level: article.difficulty_level || undefined,
    tone_style: article.tone_style,
    topic: article.topic,
    sentence_complexity: article.sentence_complexity,
    word_count: article.word_count,
    article: article.article,
    // 使用类型断言解决title属性的类型问题
    title: (article as any).title,
    alert: article.alert,
    // 若原始类型为数字，转换为字符串
    passage_needs: article.passage_needs !== undefined 
      ? String(article.passage_needs) 
      : undefined,
    passage_type: article.passage_type !== undefined 
      ? String(article.passage_type) 
      : undefined
  }
})

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
            <h1>词境</h1>
          </div>
          <div class="header-title">
            <h2>{{ pageTitle }}</h2>
          </div>
          <div class="header-actions">
            <el-button type="primary" plain @click="goBack">
              <el-icon><Back /></el-icon>
              返回历史
            </el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <div v-if="isLoading" class="loading-state">
          <el-skeleton :rows="15" animated />
        </div>
        
        <div v-else-if="record" class="record-detail-content">
          <div class="record-meta-card">
            <el-descriptions :column="3" border>
              <template #title>
                <div class="meta-title">
                  <el-icon><DataAnalysis /></el-icon>
                  <span>记录信息</span>
                </div>
              </template>
              <el-descriptions-item label="创建时间">
                <el-tag type="info" effect="plain">{{ formatDate(record.timestamp) }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="单词数量">
                <el-tag type="primary" effect="plain">{{ record.words.length }} 个单词</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="文章字数">
                <el-tag type="success" effect="plain">{{ record.article.word_count }} 字</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="文章类型">
                <el-tag type="success" effect="plain">{{ getPassageTypeText(record) }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="难度级别">
                <el-tag type="primary" effect="plain">{{ getPassageNeedsText(record) }}</el-tag>
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
          </div>
          
          <div class="content-tabs-container">
            <el-tabs 
              v-model="activeTab" 
              type="border-card" 
              class="content-tabs"
              stretch
            >
              <el-tab-pane label="文章阅读" name="article">
                <div class="tab-content-wrapper">
                  <ArticleDisplay :article-data="compatibleArticleData" />
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="翻译和解释" name="translation">
                <div class="tab-content-wrapper">
                  <TranslationDisplay :translation-data="record.translation" />
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="练习题" name="questions">
                <div class="tab-content-wrapper">
                  <div v-if="record.questions">
                    <QuestionDisplay :question-data="record.questions" />
                  </div>
                  <div v-else class="feature-unavailable">
                    <el-empty description="该记录没有练习题数据">
                      <template #image>
                        <el-icon class="empty-icon"><QuestionFilled /></el-icon>
                      </template>
                      <el-button type="primary" plain round size="small">
                        返回文章阅读
                      </el-button>
                    </el-empty>
                  </div>
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
            词境 - 使用AI增强英语学习体验
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
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
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
  font-size: 24px;
  color: #fff;
}

.record-header h1 {
  margin: 0;
  color: #fff;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 1px;
}

.header-title h2 {
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  font-weight: normal;
}

.header-actions {
  display: flex;
  gap: 12px;
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

.meta-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #303133;
  font-weight: 600;
}

.meta-title .el-icon {
  color: #409EFF;
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
  gap: 10px;
  background: #f9fafc;
  padding: 16px;
  border-radius: 8px;
}

.word-tag {
  margin: 0;
  transition: all 0.2s;
}

.word-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
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

.tab-content-wrapper {
  padding: 16px 0;
}

.feature-unavailable {
  padding: 40px;
  text-align: center;
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
  padding: 20px;
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
  .header-content {
    flex-direction: column;
    align-items: center;
    padding: 16px;
    gap: 12px;
  }
  
  .header-title {
    text-align: center;
  }
  
  .record-meta-card {
    padding: 16px;
  }
  
  .word-tags {
    padding: 12px;
    gap: 6px;
  }
  
  .tab-content-wrapper {
    padding: 8px 0;
  }
  
  .feature-unavailable {
    padding: 24px;
  }
}

@media (max-width: 576px) {
  .record-header h1 {
    font-size: 20px;
  }
  
  .header-title h2 {
    font-size: 14px;
  }
  
  .section-title {
    font-size: 15px;
  }
  
  .word-tags {
    padding: 10px;
  }
  
  .word-tag {
    font-size: 12px;
  }
  
  .empty-icon {
    font-size: 36px;
  }
  
  .feature-unavailable {
    padding: 16px;
  }
}
</style>
