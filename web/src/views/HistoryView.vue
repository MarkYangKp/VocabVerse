<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAllLearningRecords, deleteLearningRecord, clearAllLearningRecords } from '@/utils/localStorageUtils'
import type { LearningRecord } from '@/utils/localStorageUtils'

const router = useRouter()
const records = ref<LearningRecord[]>([])
const searchQuery = ref('')
const isLoading = ref(true)

// 获取并格式化日期
const formatDate = (timestamp: number) => {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 过滤记录
const filteredRecords = computed(() => {
  if (!searchQuery.value) {
    return records.value
  }
  
  const query = searchQuery.value.toLowerCase().trim()
  return records.value.filter(record => {
    // 搜索单词列表
    const wordsMatch = record.words.some(word => 
      word.toLowerCase().includes(query)
    )
    
    // 搜索文章内容
    const articleMatch = record.article.article.toLowerCase().includes(query)
    
    return wordsMatch || articleMatch
  })
})

// 加载历史记录
const loadRecords = () => {
  isLoading.value = true
  setTimeout(() => {
    records.value = getAllLearningRecords()
    isLoading.value = false
  }, 300)
}

// 查看记录详情
const viewRecordDetail = (record: LearningRecord) => {
  router.push({
    path: '/record-detail',
    query: { id: record.id }
  })
}

// 删除单个记录
const confirmDeleteRecord = (record: LearningRecord) => {
  ElMessageBox.confirm(
    '此操作将永久删除该学习记录，是否继续？',
    '提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    deleteLearningRecord(record.id)
    ElMessage.success('删除成功')
    loadRecords()
  }).catch(() => {})
}

// 清空所有记录
const confirmClearAllRecords = () => {
  if (records.value.length === 0) {
    ElMessage.info('没有历史记录可清空')
    return
  }
  
  ElMessageBox.confirm(
    '此操作将永久删除所有学习记录，是否继续？',
    '警告',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'error'
    }
  ).then(() => {
    clearAllLearningRecords()
    ElMessage.success('所有记录已清空')
    loadRecords()
  }).catch(() => {})
}

// 获取难度文本描述
const getPassageNeedsText = (passageNeeds: number | string): string => {
  // 将输入转换为数字类型
  const needsNumber = Number(passageNeeds)
  const needsMap: Record<number, string> = {
    1: '考研难度',
    2: '六级难度',
    3: '易于记忆',
    4: '四级难度',
    5: '高中水平'
  }
  return needsMap[needsNumber] || '未知难度'
}

// 获取文章类型文本描述
const getPassageTypeText = (passageType: number | string): string => {
  // 将输入转换为数字类型
  const typeNumber = Number(passageType)
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
  return typeMap[typeNumber] || '未知类型'
}

// 返回首页
const goBack = () => {
  router.push('/')
}

// 组件挂载时加载记录
onMounted(() => {
  loadRecords()
})
</script>

<template>
  <div class="history-container">
    <el-container>
      <el-header height="auto" class="history-header">
        <div class="header-content">
          <div class="logo-area" @click="goBack">
            <el-icon class="logo-icon"><Connection /></el-icon>
            <h1>Word2LLM</h1>
          </div>
          <div class="header-title">
            <h2>学习历史记录</h2>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <div class="history-content">
          <div class="history-actions">
            <el-input
              v-model="searchQuery"
              placeholder="搜索单词或文章内容"
              clearable
              class="search-input"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            
            <div class="action-buttons">
              <el-button type="danger" @click="confirmClearAllRecords" :disabled="records.length === 0">
                <el-icon><Delete /></el-icon>
                清空记录
              </el-button>
              
              <el-button type="primary" @click="goBack">
                <el-icon><Back /></el-icon>
                返回首页
              </el-button>
            </div>
          </div>
          
          <div v-if="isLoading" class="loading-state">
            <el-skeleton :rows="10" animated />
          </div>
          
          <div v-else-if="records.length === 0" class="empty-history">
            <el-empty description="暂无学习历史记录">
              <template #image>
                <el-icon class="empty-icon"><Calendar /></el-icon>
              </template>
              <el-button type="primary" @click="goBack">返回首页开始学习</el-button>
            </el-empty>
          </div>
          
          <div v-else-if="filteredRecords.length === 0" class="empty-search">
            <el-empty description="没有找到匹配的记录">
              <template #image>
                <el-icon class="empty-icon"><Search /></el-icon>
              </template>
            </el-empty>
          </div>
          
          <div v-else class="records-list">
            <el-card
              v-for="record in filteredRecords"
              :key="record.id"
              class="record-card"
              shadow="hover"
            >
              <div class="record-header">
                <div class="record-timestamp">{{ formatDate(record.timestamp) }}</div>
                <div class="record-actions">
                  <el-button 
                    type="danger" 
                    size="small"
                    plain
                    circle
                    @click.stop="confirmDeleteRecord(record)"
                  >
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
              
              <div class="record-content" @click="viewRecordDetail(record)">
                <div class="record-info">
                  <div class="info-item">
                    <el-icon><Reading /></el-icon>
                    <span>{{ getPassageNeedsText(record.article.passage_needs) }}</span>
                  </div>
                  <div class="info-item">
                    <el-icon><Document /></el-icon>
                    <span>{{ getPassageTypeText(record.article.passage_type) }}</span>
                  </div>
                  <div class="info-item">
                    <el-icon><DocumentChecked /></el-icon>
                    <span>{{ record.article.word_count }} 字</span>
                  </div>
                </div>
                
                <div class="record-words">
                  <el-tag 
                    v-for="(word, index) in record.words.slice(0, 8)" 
                    :key="word+index"
                    size="small"
                    class="word-tag"
                  >
                    {{ word }}
                  </el-tag>
                  <el-tag v-if="record.words.length > 8" size="small" type="info">
                    +{{ record.words.length - 8 }} 个单词
                  </el-tag>
                </div>
                
                <div class="record-preview">
                  {{ record.article.article.substring(0, 100) }}...
                </div>
                
                <div class="record-features">
                  <el-tag size="small" type="success" effect="plain">
                    <el-icon><Document /></el-icon>
                    文章
                  </el-tag>
                  <el-tag 
                    size="small" 
                    :type="record.translation ? 'success' : 'info'" 
                    effect="plain"
                  >
                    <el-icon><Connection /></el-icon>
                    翻译 {{ record.translation ? '✓' : '✗' }}
                  </el-tag>
                  <el-tag 
                    size="small" 
                    :type="record.questions ? 'success' : 'info'" 
                    effect="plain"
                  >
                    <el-icon><QuestionFilled /></el-icon>
                    练习题 {{ record.questions ? '✓' : '✗' }}
                  </el-tag>
                </div>
              </div>
            </el-card>
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
.history-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
}

.history-header {
  padding: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  background: linear-gradient(90deg, #409EFF 0%, #53a8ff 100%);
  position: relative;
  overflow: hidden;
}

.history-header::before {
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

.history-header h1 {
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

.history-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px 16px;
}

.history-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.search-input {
  max-width: 350px;
  width: 100%;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.loading-state,
.empty-history,
.empty-search {
  background-color: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.empty-icon {
  font-size: 48px;
  color: #c0c4cc;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.record-card {
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.record-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.record-timestamp {
  color: #909399;
  font-size: 14px;
}

.record-content {
  cursor: pointer;
}

.record-info {
  display: flex;
  gap: 16px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #606266;
}

.info-item .el-icon {
  color: #409EFF;
}

.record-words {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 14px;
}

.word-tag {
  background-color: #f0f2f5;
  margin: 3px 0;
}

.record-preview {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.record-features {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
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

/* 增强响应式布局 */
@media (max-width: 992px) {
  .history-content {
    padding: 16px;
  }
  
  .loading-state,
  .empty-history,
  .empty-search {
    padding: 30px;
  }
}

@media (max-width: 768px) {
  .history-header {
    padding: 0;
  }
  
  .header-content {
    padding: 16px;
  }
  
  .logo-icon {
    font-size: 24px;
  }
  
  .history-header h1 {
    font-size: 24px;
  }
  
  .header-title h2 {
    font-size: 16px;
  }
  
  .history-actions {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    margin-bottom: 20px;
  }
  
  .search-input {
    max-width: 100%;
  }
  
  .action-buttons {
    justify-content: space-between;
  }
  
  .loading-state,
  .empty-history,
  .empty-search {
    padding: 24px;
  }
  
  .empty-icon {
    font-size: 40px;
  }
  
  .record-card:hover {
    transform: translateY(-2px);
  }
  
  .record-info {
    gap: 12px;
  }
  
  .record-preview {
    -webkit-line-clamp: 3;
  }
  
  .app-footer {
    padding: 16px;
  }
}

@media (max-width: 576px) {
  .logo-area:hover {
    transform: none;
  }
  
  .history-content {
    padding: 12px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 10px;
  }
  
  .record-card:hover {
    transform: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }
  
  .record-header {
    margin-bottom: 10px;
    padding-bottom: 8px;
  }
  
  .info-item {
    font-size: 13px;
  }
  
  .record-preview {
    font-size: 13px;
  }
  
  .empty-icon {
    font-size: 36px;
  }
  
  .footer-content p {
    font-size: 13px;
  }
}
</style>
