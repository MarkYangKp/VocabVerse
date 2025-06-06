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

// 排序方式
const sortOrder = ref('newest')

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

// 根据排序方式返回排序后的记录
const sortedRecords = computed(() => {
  const filtered = filteredRecords.value
  
  if (sortOrder.value === 'newest') {
    return [...filtered].sort((a, b) => b.timestamp - a.timestamp)
  } else if (sortOrder.value === 'oldest') {
    return [...filtered].sort((a, b) => a.timestamp - b.timestamp)
  } else if (sortOrder.value === 'wordsMore') {
    return [...filtered].sort((a, b) => b.words.length - a.words.length)
  } else if (sortOrder.value === 'wordsLess') {
    return [...filtered].sort((a, b) => a.words.length - b.words.length)
  }
  
  return filtered
})

// 记录分组信息
const recordStats = computed(() => {
  return {
    total: records.value.length,
    withTranslation: records.value.filter(r => r.translation).length,
    withQuestions: records.value.filter(r => r.questions).length,
    totalWords: [...new Set(records.value.flatMap(r => r.words))].length
  }
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
const getPassageNeedsText = (passageNeeds: number | string | undefined): string => {
  // 如果未定义，返回默认值
  if (passageNeeds === undefined) {
    return '未知难度';
  }
  
  // 将输入转换为数字类型
  const needsNumber = Number(passageNeeds);
  const needsMap: Record<number, string> = {
    1: '考研难度',
    2: '六级难度',
    3: '易于记忆',
    4: '四级难度',
    5: '高中水平'
  }
  return needsMap[needsNumber] || '未知难度';
}

// 获取文章类型文本描述
const getPassageTypeText = (passageType: number | string | undefined): string => {
  // 如果未定义，返回默认值
  if (passageType === undefined) {
    return '未知类型';
  }
  
  // 将输入转换为数字类型
  const typeNumber = Number(passageType);
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
  return typeMap[typeNumber] || '未知类型';
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
    <div class="page-background"></div>
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header height="auto" class="history-header">
        <div class="header-content">
          <div class="header-left">
            <div class="logo-area" @click="goBack">
              <el-icon class="logo-icon"><Connection /></el-icon>
              <h1>词境</h1>
            </div>
          </div>
          <div class="header-center">
            <h2>学习历史记录</h2>
          </div>
          <div class="header-right">
            <el-button type="primary" plain round @click="goBack">
              <el-icon><Back /></el-icon>
              返回主页
            </el-button>
          </div>
        </div>
      </el-header>
      
      <!-- 主要内容区域 -->
      <el-main>
        <div class="history-content">
          <!-- 搜索和操作区域 -->
          <div class="history-actions">
            <div class="action-left">
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
            </div>
            
            <div class="action-center" v-if="records.length > 0">
              <el-radio-group v-model="sortOrder" size="small" class="sort-options">
                <el-radio-button label="newest">最新优先</el-radio-button>
                <el-radio-button label="oldest">最早优先</el-radio-button>
                <el-radio-button label="wordsMore">单词数多</el-radio-button>
                <el-radio-button label="wordsLess">单词数少</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="action-right">
              <el-button type="danger" @click="confirmClearAllRecords" :disabled="records.length === 0">
                <el-icon><Delete /></el-icon>
                清空记录
              </el-button>
            </div>
          </div>
          
          <!-- 统计信息卡片 -->
          <div v-if="records.length > 0" class="stats-card">
            <div class="stat-item">
              <div class="stat-value">{{ recordStats.total }}</div>
              <div class="stat-label">学习记录</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-value">{{ recordStats.totalWords }}</div>
              <div class="stat-label">不同单词</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-value">{{ recordStats.withTranslation }}</div>
              <div class="stat-label">含翻译解析</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-value">{{ recordStats.withQuestions }}</div>
              <div class="stat-label">含练习题</div>
            </div>
          </div>
          
          <!-- 加载状态 -->
          <div v-if="isLoading" class="loading-state">
            <el-skeleton :rows="10" animated />
          </div>
          
          <!-- 空记录状态 -->
          <div v-else-if="records.length === 0" class="empty-history">
            <el-empty description="暂无学习历史记录">
              <template #image>
                <el-icon class="empty-icon"><Calendar /></el-icon>
              </template>
              <el-button type="primary" @click="goBack" round>返回首页开始学习</el-button>
            </el-empty>
          </div>
          
          <!-- 搜索无结果状态 -->
          <div v-else-if="filteredRecords.length === 0" class="empty-search">
            <el-empty description="没有找到匹配的记录">
              <template #image>
                <el-icon class="empty-icon"><Search /></el-icon>
              </template>
              <el-button @click="searchQuery = ''" size="small" type="primary" plain>
                清除搜索
              </el-button>
            </el-empty>
          </div>
          
          <!-- 记录列表 -->
          <div v-else class="records-list">
            <el-card
              v-for="record in sortedRecords"
              :key="record.id"
              class="record-card"
              shadow="hover"
            >
              <!-- 记录头部 -->
              <div class="record-header">
                <div class="record-timestamp">
                  <el-icon><Clock /></el-icon>
                  {{ formatDate(record.timestamp) }}
                </div>
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
              
              <!-- 记录内容 -->
              <div class="record-content" @click="viewRecordDetail(record)">
                <!-- 记录信息 -->
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
                
                <!-- 单词标签 -->
                <div class="record-words">
                  <el-tag 
                    v-for="(word, index) in record.words.slice(0, 8)" 
                    :key="word+index"
                    size="small"
                    class="word-tag"
                    effect="plain"
                  >
                    {{ word }}
                  </el-tag>
                  <el-tag v-if="record.words.length > 8" size="small" type="info" effect="plain">
                    +{{ record.words.length - 8 }} 个单词
                  </el-tag>
                </div>
                
                <!-- 文章预览 -->
                <div class="record-preview">
                  {{ record.article.article.substring(0, 80) }}...
                </div>
                
                <!-- 功能标签 -->
                <div class="record-features">
                  <el-tag size="small" type="success" effect="dark">
                    <el-icon><Document /></el-icon>
                    文章
                  </el-tag>
                  <el-tag 
                    size="small" 
                    :type="record.translation ? 'success' : 'info'" 
                    :effect="record.translation ? 'dark' : 'plain'"
                  >
                    <el-icon><Connection /></el-icon>
                    翻译 {{ record.translation ? '✓' : '✗' }}
                  </el-tag>
                  <el-tag 
                    size="small" 
                    :type="record.questions ? 'success' : 'info'" 
                    :effect="record.questions ? 'dark' : 'plain'"
                  >
                    <el-icon><QuestionFilled /></el-icon>
                    练习题 {{ record.questions ? '✓' : '✗' }}
                  </el-tag>
                </div>
                
                <div class="view-details">
                  <el-icon><Right /></el-icon>
                  <span>查看详情</span>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </el-main>
      
      <!-- 页脚 -->
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
/* 全局容器样式 */
.history-container {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 背景效果 */
.page-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f0f4f8 0%, #d7e3f0 100%);
  z-index: -1;
}

.main-container {
  position: relative;
  z-index: 1;
  min-height: 100vh;
}

/* 顶部导航栏样式 */
.history-header {
  padding: 0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
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
  background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%);
  opacity: 0.6;
  pointer-events: none;
  animation: pulse 15s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.header-content {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;
}

.header-left, .header-right {
  flex: 1;
}

.header-right {
  display: flex;
  justify-content: flex-end;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: var(--transition-normal);
}

.logo-area:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 24px;
  color: #fff;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.history-header h1 {
  margin: 0;
  color: #fff;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 1px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.header-center h2 {
  margin: 0;
  color: rgba(255, 255, 255, 0.95);
  font-size: 18px;
  font-weight: normal;
  letter-spacing: 0.5px;
  text-align: center;
}

/* 主内容区域样式 */
.history-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
}

/* 搜索和操作区域样式 */
.history-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius-md);
  padding: 16px;
  box-shadow: var(--card-shadow);
}

.action-left, .action-right, .action-center {
  display: flex;
  align-items: center;
}

.search-input {
  max-width: 350px;
  width: 100%;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: var(--border-radius-sm);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.sort-options {
  margin: 0 auto;
}

.action-right .el-button {
  border-radius: var(--border-radius-sm);
  transition: var(--transition-normal);
}

.action-right .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 统计卡片样式 */
.stats-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius-md);
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: var(--card-shadow);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background-color: rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

/* 状态显示区域样式 */
.loading-state,
.empty-history,
.empty-search {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: var(--border-radius-lg);
  padding: 40px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);
}

.empty-icon {
  font-size: 48px;
  color: #a0a8b8;
  margin-bottom: 16px;
}

/* 记录列表样式 */
.records-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.record-card {
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: var(--transition-normal);
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: none;
  height: 100%;
}

.record-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.record-card :deep(.el-card__body) {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* 记录头部样式 */
.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.record-timestamp {
  color: #606a78;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.record-actions .el-button {
  transition: var(--transition-normal);
}

.record-actions .el-button:hover {
  transform: rotate(15deg);
}

/* 记录内容样式 */
.record-content {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.record-info {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #4a5568;
  background: rgba(0, 0, 0, 0.03);
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 13px;
}

.info-item .el-icon {
  color: #3a7bd5;
}

/* 单词标签样式 */
.record-words {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.word-tag {
  border-radius: 6px;
  margin: 0;
  transition: var(--transition-normal);
}

.word-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 文章预览样式 */
.record-preview {
  color: #4a5568;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  background: rgba(0, 0, 0, 0.02);
  padding: 12px;
  border-radius: 8px;
  border-left: 3px solid #3a7bd5;
  flex: 1;
}

/* 功能标签样式 */
.record-features {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.record-features .el-tag {
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: var(--transition-normal);
}

.record-features .el-tag:hover {
  transform: translateY(-2px);
}

/* 查看详情按钮 */
.view-details {
  display: flex;
  align-items: center;
  gap: 6px;
  justify-content: center;
  color: var(--primary-color);
  font-size: 14px;
  padding: 8px;
  border-radius: 8px;
  background: rgba(64, 158, 255, 0.1);
  transition: var(--transition-normal);
  margin-top: auto;
}

.record-card:hover .view-details {
  background: rgba(64, 158, 255, 0.2);
}

/* 页脚样式 */
.app-footer {
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  margin-top: auto;
  box-shadow: var(--footer-shadow);
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
  color: #606a78;
  margin: 0;
  font-size: 14px;
}

.footer-content .el-icon {
  color: #3a7bd5;
}

/* 响应式布局 */
@media (max-width: 992px) {
  .history-content {
    padding: 16px;
  }
  
  .records-list {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
  }
  
  .loading-state,
  .empty-history,
  .empty-search {
    padding: 30px;
  }
  
  .stats-card {
    padding: 16px;
  }
  
  .stat-value {
    font-size: 20px;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 12px;
    padding: 16px;
  }
  
  .header-left, .header-right {
    width: 100%;
    justify-content: center;
  }
  
  .header-right {
    margin-top: 8px;
  }
  
  .logo-icon {
    font-size: 20px;
  }
  
  .history-header h1 {
    font-size: 20px;
  }
  
  .history-actions {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .search-input {
    max-width: 100%;
  }
  
  .action-center {
    order: 3;
    width: 100%;
    justify-content: center;
  }
  
  .action-right {
    order: 2;
    justify-content: flex-end;
  }
  
  .stats-card {
    flex-wrap: wrap;
    gap: 16px;
  }
  
  .stat-divider {
    display: none;
  }
  
  .stat-item {
    width: 50%;
    flex: none;
  }
  
  .records-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 576px) {
  .logo-area:hover {
    transform: none;
  }
  
  .header-center h2 {
    font-size: 16px;
  }
  
  .history-content {
    padding: 12px 8px;
  }
  
  .history-actions,
  .stats-card {
    padding: 12px;
    border-radius: 10px;
  }
  
  .stat-value {
    font-size: 18px;
  }
  
  .stat-label {
    font-size: 12px;
  }
  
  .record-card {
    border-radius: 10px;
  }
  
  .record-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  }
  
  .info-item {
    padding: 4px 8px;
    font-size: 12px;
  }
  
  .record-preview {
    font-size: 13px;
    padding: 10px;
  }
  
  .view-details {
    font-size: 12px;
    padding: 6px;
  }
  
  .empty-icon {
    font-size: 36px;
  }
  
  .loading-state,
  .empty-history,
  .empty-search {
    padding: 24px;
    border-radius: 10px;
  }
  
  .app-footer {
    padding: 16px;
  }
  
  .footer-content p {
    font-size: 12px;
  }
}
</style>
