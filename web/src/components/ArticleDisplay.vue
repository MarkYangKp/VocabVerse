<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { marked } from 'marked'
import { ElMessage } from 'element-plus'

// 定义接口类型
interface ArticleData {
  article?: string;
  difficulty_level?: string;
  article_type?: string;
  tone_style?: string;
  topic?: string;
  word_count?: number;
  sentence_complexity?: number;
  passage_needs?: string; // 旧API
  passage_type?: string;  // 旧API
  alert?: string;
  [key: string]: any;     // 允许其他属性
}

// 定义映射类型
type DifficultyMapType = {
  [key: string]: string;
  a1: string;
  a2: string;
  b1: string;
  b2: string;
  c1: string;
  c2: string;
  easy: string;
  intermediate: string;
  advanced: string;
  high_school: string;
  cet4: string;
  cet6: string;
  graduate: string;
  memory_friendly: string;
}

type ArticleTypeMapType = {
  [key: string]: string;
  news: string;
  short_story: string;
  science: string;
  blog: string;
  academic: string;
  email: string;
  dialogue: string;
  argumentative: string;
  narrative: string;
  descriptive: string;
  business: string;
  technical: string;
  editorial: string;
  social_media: string;
}

type ToneStyleMapType = {
  [key: string]: string;
  formal: string;
  semi_formal: string;
  informal: string;
  humorous: string;
  academic: string;
  business: string;
  conversational: string;
  technical: string;
  professional: string;
}

type TopicMapType = {
  [key: string]: string;
  general: string;
  technology: string;
  business: string;
  health: string;
  science: string;
  education: string;
  environment: string;
  entertainment: string;
  sports: string;
  politics: string;
  culture: string;
  history: string;
  travel: string;
  food: string;
  fashion: string;
  art: string;
  literature: string;
  economics: string;
  philosophy: string;
  psychology: string;
}

const props = defineProps({
  articleData: {
    type: Object as () => ArticleData | null,
    default: null
  }
})

const articleHtml = ref('')
const showAllParams = ref(false)

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

// 获取中文名称的映射
const difficultyMap = computed((): DifficultyMapType => {
  return {
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
})

const articleTypeMap = computed((): ArticleTypeMapType => {
  return {
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
})

const toneStyleMap = computed((): ToneStyleMapType => {
  return {
    'formal': '正式',
    'semi_formal': '半正式',
    'informal': '非正式/口语化',
    'humorous': '幽默/轻松',
    'academic': '学术严谨',
    'business': '商务',
    'conversational': '对话式',
    'technical': '技术性',
    'professional': '专业'
  }
})

const topicMap = computed((): TopicMapType => {
  return {
    'general': '一般/通用',
    'technology': '科技',
    'business': '商业',
    'health': '健康',
    'science': '科学',
    'education': '教育',
    'environment': '环境',
    'entertainment': '娱乐',
    'sports': '体育',
    'politics': '政治',
    'culture': '文化',
    'history': '历史',
    'travel': '旅游',
    'food': '美食',
    'fashion': '时尚',
    'art': '艺术',
    'literature': '文学',
    'economics': '经济',
    'philosophy': '哲学',
    'psychology': '心理学'
  }
})

// 获取参数值，支持新API格式
const getDifficultyText = computed(() => {
  if (!props.articleData) return '未知难度'
  
  // 使用新的difficulty_level参数
  if (props.articleData.difficulty_level) {
    const key = props.articleData.difficulty_level as string
    return difficultyMap.value[key] || key
  }
  
  // 兼容旧参数
  return props.articleData.passage_needs || '未知难度'
})

const getArticleTypeText = computed(() => {
  if (!props.articleData) return '未知类型'
  
  // 使用新的article_type参数
  if (props.articleData.article_type) {
    const key = props.articleData.article_type as string
    return articleTypeMap.value[key] || key
  }
  
  // 兼容旧参数
  return props.articleData.passage_type || '未知类型'
})

const getToneStyleText = computed(() => {
  if (!props.articleData || !props.articleData.tone_style) return '未指定'
  const key = props.articleData.tone_style as string
  return toneStyleMap.value[key] || key
})

const getTopicText = computed(() => {
  if (!props.articleData || !props.articleData.topic) return '未指定'
  const key = props.articleData.topic as string
  return topicMap.value[key] || key
})

const toggleParamsDisplay = () => {
  showAllParams.value = !showAllParams.value
}
</script>

<template>
  <div v-if="articleData" class="article-display">
    <div class="article-header">
      <div class="article-info-card">
        <!-- 基本信息行 -->
        <div class="info-row">
          <div class="info-item">
            <el-icon><Reading /></el-icon>
            <span class="info-label">难度级别:</span>
            <span class="info-value">{{ getDifficultyText }}</span>
          </div>
          <div class="info-item">
            <el-icon><Document /></el-icon>
            <span class="info-label">文章类型:</span>
            <span class="info-value">{{ getArticleTypeText }}</span>
          </div>
          <div class="info-item">
            <el-icon><DocumentChecked /></el-icon>
            <span class="info-label">字数统计:</span>
            <span class="info-value">{{ articleData.word_count }}</span>
          </div>
          <div class="toggle-more">
            <el-button type="text" size="small" @click="toggleParamsDisplay">
              {{ showAllParams ? '收起参数' : '更多参数' }}
              <el-icon class="el-icon--right">
                <component :is="showAllParams ? 'ArrowUp' : 'ArrowDown'" />
              </el-icon>
            </el-button>
          </div>
        </div>
        
        <!-- 扩展信息行 - 仅在showAllParams为true时显示 -->
        <div v-if="showAllParams" class="extended-info-row">
          <div class="info-item" v-if="articleData.tone_style">
            <el-icon><ChatDotRound /></el-icon>
            <span class="info-label">语气风格:</span>
            <span class="info-value">{{ getToneStyleText }}</span>
          </div>
          <div class="info-item" v-if="articleData.topic">
            <el-icon><Collection /></el-icon>
            <span class="info-label">主题领域:</span>
            <span class="info-value">{{ getTopicText }}</span>
          </div>
          <div class="info-item" v-if="articleData.sentence_complexity">
            <el-icon><Finished /></el-icon>
            <span class="info-label">句子复杂度:</span>
            <span class="info-value">{{ Math.round(articleData.sentence_complexity * 100) }}%</span>
          </div>
        </div>
        
        <div class="button-row">
          <el-button type="primary" size="small" @click="copyArticle" class="copy-btn">
            <el-icon><CopyDocument /></el-icon>
            复制文章
          </el-button>
        </div>
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
  transition: all 0.3s ease;
}

.article-header {
  margin-bottom: 20px;
}

.article-info-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
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

.info-row, .extended-info-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
}

.extended-info-row {
  padding-top: 8px;
  border-top: 1px dashed #e4e7ed;
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

.toggle-more {
  margin-left: auto;
}

.button-row {
  display: flex;
  justify-content: flex-end;
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
    gap: 12px;
    padding: 16px;
  }
  
  .info-row, .extended-info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    width: 100%;
  }
  
  .toggle-more {
    margin-left: 0;
    width: 100%;
    display: flex;
    justify-content: flex-end;
  }
  
  .button-row {
    width: 100%;
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
