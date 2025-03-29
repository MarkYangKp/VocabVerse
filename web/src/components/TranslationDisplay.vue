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
// 新增: 使用 Map 跟踪每个单词的显示/隐藏状态
const wordVisibility = ref(new Map<string, boolean>())

// 监听传入的数据并更新组件状态
watch(() => props.translationData, (newData) => {
  if (newData) {
    languagePoints.value = newData.language_points || []
    translation.value = newData.translation || ''
    
    // 初始化单词可见性状态，默认全部隐藏
    const newWordVisibility = new Map<string, boolean>()
    languagePoints.value.forEach(point => {
      newWordVisibility.set(point.word, false)
    })
    wordVisibility.value = newWordVisibility
  } else {
    languagePoints.value = []
    translation.value = ''
    wordVisibility.value = new Map<string, boolean>()
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

// 当前选中的单词
const currentWord = ref('')

// 处理单词点击，记忆最后点击的单词
const handleWordClick = (word: string) => {
  currentWord.value = word
}

// 新增: 切换单词解释的显示/隐藏状态
const toggleWordExplanation = (word: string, event: Event) => {
  // 阻止冒泡，避免触发外层的点击事件
  event.stopPropagation()
  
  // 切换显示状态
  const currentVisibility = wordVisibility.value.get(word) || false
  wordVisibility.value.set(word, !currentVisibility)
}

// 新增: 判断单词解释是否显示
const isWordExplanationVisible = (word: string): boolean => {
  return wordVisibility.value.get(word) || false
}

// 新增: 渲染单词解释为HTML
const renderExplanation = (explanation: string) => {
  return marked(explanation || '')
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
        <div class="section-actions" v-if="languagePoints.length">
          <el-tooltip content="点击单词展开/收起解释" placement="top">
            <el-button type="info" plain size="small" circle>
              <el-icon><InfoFilled /></el-icon>
            </el-button>
          </el-tooltip>
        </div>
      </div>
      
      <template v-if="languagePoints.length">
        <div class="words-list">
          <el-row :gutter="16">
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="8" 
              v-for="point in languagePoints"
              :key="point.word"
            >
              <div class="word-card" 
                :class="{ 'active-word': currentWord === point.word }"
                @click="handleWordClick(point.word)"
              >
                <div class="word-header" @click="toggleWordExplanation(point.word, $event)">
                  <div class="word-text">{{ point.word }}</div>
                  <div class="word-actions">
                    <el-tag size="small" effect="light" class="word-tag">词汇</el-tag>
                    <el-icon class="toggle-icon" :class="{ 'is-expanded': isWordExplanationVisible(point.word) }">
                      <ArrowDown />
                    </el-icon>
                  </div>
                </div>
                <div class="word-content" v-show="isWordExplanationVisible(point.word)">
                  <div class="explanation-content" v-html="renderExplanation(point.explanation)"></div>
                </div>
              </div>
            </el-col>
          </el-row>
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
  transition: var(--transition-normal, all 0.3s ease);
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
  color: var(--primary-color, #409EFF);
}

.section-actions {
  display: flex;
  gap: 10px;
}

.copy-btn {
  transition: var(--transition-fast, all 0.2s ease);
  border-radius: var(--border-radius-sm, 8px);
}

.copy-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.words-list {
  border-radius: var(--border-radius-md, 12px);
  overflow: hidden;
}

.word-card {
  background-color: #fff;
  border-radius: var(--border-radius-sm, 8px);
  overflow: hidden;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  transition: var(--transition-normal, all 0.3s ease);
  cursor: pointer;
  border: 1px solid #eaeefb;
}

.word-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  border-color: rgba(64, 158, 255, 0.3);
}

.active-word {
  border-color: var(--primary-color, #409EFF);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.15);
}

.word-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: linear-gradient(to right, #f0f7ff, #e6f0ff);
  border-bottom: 1px solid rgba(64, 158, 255, 0.1);
  cursor: pointer;
}

.word-text {
  font-weight: 600;
  font-size: 16px;
  color: var(--primary-color, #409EFF);
}

.word-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.word-tag {
  color: var(--primary-color, #409EFF);
  font-size: 12px;
}

.toggle-icon {
  transition: transform 0.3s ease;
  color: #909399;
}

.toggle-icon.is-expanded {
  transform: rotate(180deg);
}

.word-content {
  padding: 16px;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.explanation-content {
  line-height: 1.8;
  color: #303133;
  font-size: 15px;
}

.translation-content-card {
  background-color: #fff;
  border-radius: var(--border-radius-md, 12px);
  padding: 24px;
  box-shadow: var(--card-shadow, 0 4px 16px rgba(0, 0, 0, 0.06));
  transition: var(--transition-normal, all 0.3s ease);
  min-height: 200px;
}

.translation-content-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.translation-text {
  line-height: 1.8;
  color: #303133;
  font-size: 15px;
}

.translation-text :deep(p) {
  margin-bottom: 16px;
}

.translation-text :deep(strong) {
  color: var(--primary-color, #409EFF);
  font-weight: 600;
}

.translation-text :deep(h1),
.translation-text :deep(h2),
.translation-text :deep(h3),
.translation-text :deep(h4) {
  margin-top: 1.5em;
  margin-bottom: 0.8em;
  color: #303133;
}

.empty-card {
  padding: 24px;
  background-color: #f9fafc;
  border-radius: var(--border-radius-md, 12px);
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
  border-radius: var(--border-radius-md, 12px);
  background-color: #fff;
  box-shadow: var(--card-shadow, 0 4px 16px rgba(0, 0, 0, 0.06));
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
    box-shadow: var(--card-shadow, 0 4px 16px rgba(0, 0, 0, 0.06));
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
  
  .word-card:hover {
    transform: none;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  }
}

@media (max-width: 576px) {
  .translation-section {
    margin-bottom: 20px;
  }
  
  .word-header {
    padding: 10px 12px;
  }
  
  .word-content {
    padding: 12px;
  }
  
  .explanation-content {
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

.explanation-content :deep(p) {
  margin-bottom: 12px;
}

.explanation-content :deep(strong) {
  color: var(--primary-color, #409EFF);
  font-weight: 600;
}

.explanation-content :deep(code) {
  background-color: #f8f8f8;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: monospace;
  color: #e6a23c;
}

.explanation-content :deep(ul), 
.explanation-content :deep(ol) {
  padding-left: 20px;
  margin-bottom: 12px;
}

.explanation-content :deep(li) {
  margin-bottom: 4px;
}
</style>
