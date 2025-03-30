<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import { useRouter } from 'vue-router'
import WordInput from '@/components/WordInput.vue'
import ArticleDisplay from '@/components/ArticleDisplay.vue'
import TranslationDisplay from '@/components/TranslationDisplay.vue'
import QuestionDisplay from '@/components/QuestionDisplay.vue'
import { saveLearningRecord } from '@/utils/localStorageUtils'

// 定义类型
interface GenerationConfig {
  // 兼容旧参数
  passageNeeds: number
  passageType: number
  wordNum: string
  
  // 新API参数
  article_type: string
  difficulty_level: string
  tone_style: string
  article_length: string
  topic: string
  custom_word_count: number
  sentence_complexity: number
}

// 定义响应式状态
const wordList = ref<string[]>([])
const config = reactive<GenerationConfig>({
  // 兼容旧参数
  passageNeeds: 2, // 默认六级难度
  passageType: 1, // 默认议论文
  wordNum: '300', // 修改为单一数字格式，不使用范围表示
  
  // 新API参数
  article_type: 'argumentative', // 默认议论文
  difficulty_level: 'cet6', // 默认六级难度
  tone_style: 'formal', // 默认正式语气
  article_length: 'medium', // 默认中等长度
  topic: 'general', // 默认主题
  custom_word_count: 300, // 自定义词数，默认300
  sentence_complexity: 0.6 // 句子复杂度，默认0.6
})

// 文章状态
const articleGenerated = ref(false)
const articleData = ref<any>(null)
const translationData = ref<any>(null)
const questionData = ref<any>(null)
const activeTab = ref('article')
const recordId = ref<number | null>(null)

// 高级设置显示开关
const showAdvancedSettings = ref(false)

// 获取路由器实例
const router = useRouter()

// 接收从子组件传来的单词列表
const onWordsUpdated = (words: string[]) => {
  wordList.value = words
}
//环境变量中的API基础路径
const baseApiUrl = import.meta.env.VITE_API_BASE_URL

// API基础路径 - 需要调整为正确的路径格式
const apiUrl = baseApiUrl || 'http://localhost:9988/v1';

// 优化视觉反馈
const isGenerating = ref(false)
const loadingText = ref('')

// 根据新接口定义枚举选项
const articleTypeOptions = [
  { value: 'news', label: '新闻' },
  { value: 'short_story', label: '短篇故事' },
  { value: 'science', label: '科普文章' },
  { value: 'blog', label: '博客/观点文' },
  { value: 'academic', label: '学术论文' },
  { value: 'email', label: '电子邮件/信件' },
  { value: 'dialogue', label: '对话体' },
  { value: 'argumentative', label: '议论文' },
  { value: 'narrative', label: '叙事文' },
  { value: 'descriptive', label: '描写文' },
  { value: 'business', label: '商业报告' },
  { value: 'technical', label: '技术报告' },
  { value: 'editorial', label: '社论' },
  { value: 'social_media', label: '社交媒体文案' }
]

const difficultyLevelOptions = [
  { value: 'a1', label: 'CEFR A1 (初级)' },
  { value: 'a2', label: 'CEFR A2' },
  { value: 'b1', label: 'CEFR B1' },
  { value: 'b2', label: 'CEFR B2' },
  { value: 'c1', label: 'CEFR C1' },
  { value: 'c2', label: 'CEFR C2' },
  { value: 'easy', label: '简单' },
  { value: 'intermediate', label: '中等' },
  { value: 'advanced', label: '高级' },
  { value: 'high_school', label: '高中水平' },
  { value: 'cet4', label: '四级难度' },
  { value: 'cet6', label: '六级难度' },
  { value: 'graduate', label: '考研难度' },
  { value: 'memory_friendly', label: '易于记忆' }
]

const toneStyleOptions = [
  { value: 'formal', label: '正式' },
  { value: 'semi_formal', label: '半正式' },
  { value: 'informal', label: '非正式/口语化' },
  { value: 'humorous', label: '幽默/轻松' },
  { value: 'academic', label: '学术严谨' },
  { value: 'business', label: '商务' },
  { value: 'conversational', label: '对话式' },
  { value: 'technical', label: '技术性' },
  { value: 'professional', label: '专业' }
]

const articleLengthOptions = [
  { value: 'short', label: '短篇(100-200词)' },
  { value: 'medium', label: '中篇(300-500词)' },
  { value: 'long', label: '长篇(600-1000词)' },
  { value: 'custom', label: '自定义' }
]

const topicOptions = [
  { value: 'general', label: '一般/通用' },
  { value: 'technology', label: '科技' },
  { value: 'business', label: '商业' },
  { value: 'health', label: '健康' },
  { value: 'science', label: '科学' },
  { value: 'education', label: '教育' },
  { value: 'environment', label: '环境' },
  { value: 'entertainment', label: '娱乐' },
  { value: 'sports', label: '体育' },
  { value: 'politics', label: '政治' },
  { value: 'culture', label: '文化' },
  { value: 'history', label: '历史' },
  { value: 'travel', label: '旅游' },
  { value: 'food', label: '美食' },
  { value: 'fashion', label: '时尚' },
  { value: 'art', label: '艺术' },
  { value: 'literature', label: '文学' },
  { value: 'economics', label: '经济' },
  { value: 'philosophy', label: '哲学' },
  { value: 'psychology', label: '心理学' }
]

// 辅助计算属性：是否显示自定义字数输入框
const showCustomWordCount = computed(() => {
  return config.article_length === 'custom'
})

// 当旧参数更改时，同步到新参数
watch(() => config.passageNeeds, (newValue) => {
  syncPassageNeeds(newValue)
})

watch(() => config.passageType, (newValue) => {
  syncPassageType(newValue)
})

// 生成文章
const generateArticle = async () => {
  if (wordList.value.length === 0) {
    ElMessage.warning('请先输入或上传单词')
    return
  }

  isGenerating.value = true
  loadingText.value = '正在生成文章，请稍候...'

  try {
    // 构建请求体，仅使用新API参数，不包含已弃用的旧参数
    const requestBody = {
      words: wordList.value,
      // 新API参数
      article_type: config.article_type,
      difficulty_level: config.difficulty_level,
      tone_style: config.tone_style,
      article_length: config.article_length,
      topic: config.topic,
      sentence_complexity: config.sentence_complexity,
      // 当选择自定义长度时使用
      custom_word_count: config.article_length === 'custom' ? config.custom_word_count : undefined
    };

    const response = await fetch(`${apiUrl}/api/learning/word2passage`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      throw new Error(`API响应错误: ${response.status}`);
    }

    const responseData = await response.json();
    articleData.value = responseData;
    articleGenerated.value = true;
    
    // 如果API返回了alert消息，显示给用户
    if (articleData.value.alert) {
      ElMessage.warning(articleData.value.alert);
    }

    // 保存到本地缓存
    const uniqueId = `record_${Date.now()}_${Math.floor(Math.random() * 10000)}`;
    
    saveLearningRecord({
      id: uniqueId,
      timestamp: Date.now(),
      words: [...wordList.value],
      article: { ...articleData.value }
    });

    // 自动获取翻译和问题
    loadingText.value = '文章已生成，正在获取更多内容...'
    setTimeout(() => {
      getTranslation();
      getQuestions();
    }, 300);

  } catch (error) {
    console.error('生成文章失败:', error);
    // 提供更详细的错误信息
    if (error instanceof Error) {
      ElMessage.error(`生成文章失败: ${error.message}`);
    } else {
      ElMessage.error('生成文章失败，请稍后再试');
    }
  } finally {
    setTimeout(() => {
      isGenerating.value = false;
    }, 500);
  }
}

// 获取翻译和解释 - 更新为新API格式
const getTranslation = async () => {
  if (!articleGenerated.value) return;

  // 不显示全屏loading，改为后台静默获取
  const isAutoLoad = translationData.value === null && activeTab.value !== 'translation';
  
  let loading = null;
  if (!isAutoLoad) {
    loading = ElLoading.service({
      lock: true,
      text: '正在获取翻译和解释...',
      background: 'rgba(255, 255, 255, 0.7)'
    });
  }

  try {
    const response = await fetch(`${apiUrl}/api/learning/passage2explanation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        words: wordList.value,
        passage: articleData.value.article
      })
    });
    
    if (!response.ok) {
      throw new Error(`API响应错误: ${response.status}`);
    }

    translationData.value = await response.json();
    
    // 更新本地缓存
    if (articleData.value) {
      const uniqueId = `record_${Date.now()}_${Math.floor(Math.random() * 10000)}`;
      
      saveLearningRecord({
        id: uniqueId,
        timestamp: Date.now(),
        words: [...wordList.value],
        article: { ...articleData.value },
        translation: { ...translationData.value }
      });
    }
  } catch (error) {
    console.error('获取翻译和解释失败:', error);
    if (!isAutoLoad) {
      ElMessage.error('获取翻译和解释失败，请稍后再试');
    }
  } finally {
    if (loading) {
      loading.close();
    }
  }
}

// 获取习题 - 更新为新API格式
const getQuestions = async () => {
  if (!articleGenerated.value) return;

  // 不显示全屏loading，改为后台静默获取
  const isAutoLoad = questionData.value === null && activeTab.value !== 'questions';
  
  let loading = null;
  if (!isAutoLoad) {
    loading = ElLoading.service({
      lock: true,
      text: '正在生成习题...',
      background: 'rgba(255, 255, 255, 0.7)'
    });
  }

  try {
    const response = await fetch(`${apiUrl}/api/learning/passage2question`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        words: wordList.value,
        passage: articleData.value.article,
        difficulty: "适中" // 使用默认难度
      })
    });
    
    if (!response.ok) {
      throw new Error(`API响应错误: ${response.status}`);
    }

    questionData.value = await response.json();
    
    // 更新本地缓存
    if (articleData.value) {
      const uniqueId = `record_${Date.now()}_${Math.floor(Math.random() * 10000)}`;
      
      saveLearningRecord({
        id: uniqueId,
        timestamp: Date.now(),
        words: [...wordList.value],
        article: { ...articleData.value },
        translation: translationData.value ? { ...translationData.value } : undefined,
        questions: [...questionData.value]
      });
    }
  } catch (error) {
    console.error('获取习题失败:', error);
    if (!isAutoLoad) {
      ElMessage.error('获取习题失败，请稍后再试');
    }
  } finally {
    if (loading) {
      loading.close();
    }
  }
}

// 辅助函数：旧参数映射到新参数（用于UI展示）
const mapPassageNeedsToNewFormat = (passageNeeds: number): string => {
  const needsMap: Record<number, string> = {
    1: 'graduate', // 考研难度
    2: 'cet6', // 六级难度
    3: 'memory_friendly', // 易于记忆
    4: 'cet4', // 四级难度
    5: 'high_school' // 高中水平
  }
  return needsMap[passageNeeds] || 'intermediate'
}

const mapPassageTypeToNewFormat = (passageType: number): string => {
  const typeMap: Record<number, string> = {
    1: 'argumentative', // 议论文
    2: 'science', // 说明文
    3: 'short_story', // 短篇小说
    4: 'narrative', // 叙事文
    5: 'descriptive', // 描写文
    6: 'business', // 商业报告
    7: 'technical', // 技术报告
    8: 'news', // 新闻报道
    9: 'editorial', // 社论
    10: 'blog', // 博客文章
    11: 'social_media' // 社交媒体文案
  }
  return typeMap[passageType] || 'general'
}

// 辅助函数：同步旧参数与新参数
const syncPassageNeeds = (passageNeeds: number) => {
  config.difficulty_level = mapPassageNeedsToNewFormat(passageNeeds)
}

const syncPassageType = (passageType: number) => {
  config.article_type = mapPassageTypeToNewFormat(passageType)
}

// 辅助函数：获取难度文本描述
const getPassageNeedsText = (passageNeeds: number): string => {
  const needsMap: Record<number, string> = {
    1: '考研难度',
    2: '六级难度',
    3: '易于记忆',
    4: '四级难度',
    5: '高中水平'
  }
  return needsMap[passageNeeds] || '未知难度'
}

// 辅助函数：获取文章类型文本描述
const getPassageTypeText = (passageType: number): string => {
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

// 添加动画控制
const isAppLoaded = ref(false)

// 在组件加载后显示动画
onMounted(() => {
  setTimeout(() => {
    isAppLoaded.value = true
  }, 300)
})

// 跳转到历史记录页面
const viewHistory = () => {
  router.push('/history');
}
</script>

<template>
  <div class="home-container" :class="{ 'app-loaded': isAppLoaded }">
    <el-container>
      <el-header height="auto" class="app-header">
        <div class="header-content">
          <div class="logo-area">
            <el-icon class="logo-icon"><Connection /></el-icon>
            <h1>词境</h1>
          </div>
          <div class="header-description">
            <p>每个单词都值得一个故事</p>
          </div>
          <div class="header-actions">
            <el-button type="primary" plain round @click="viewHistory">
              <el-icon><List /></el-icon>
              学习历史
            </el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="24" class="main-content">
          <!-- 左侧：单词输入和配置区域 -->
          <el-col :xs="24" :sm="24" :md="8" :lg="7" :xl="6" class="left-col">
            <div class="left-panel">
              <el-card class="word-input-card" shadow="hover">
                <template #header>
                  <div class="panel-header">
                    <el-icon><EditPen /></el-icon>
                    <span>单词输入</span>
                  </div>
                </template>
                
                <WordInput @words-updated="onWordsUpdated" />
                
                <div class="config-section">
                  <div class="section-divider">
                    <el-divider>
                      <div class="divider-content">
                        <el-icon><Setting /></el-icon>
                        <span>文章生成配置</span>
                      </div>
                    </el-divider>
                  </div>
                  
                  <el-form label-position="top" size="default" class="config-form">
                    <!-- 基础配置 -->
                    <el-form-item label="文章类型">
                      <el-select v-model="config.article_type" placeholder="选择类型" class="w-100">
                        <el-option
                          v-for="option in articleTypeOptions"
                          :key="option.value"
                          :label="option.label"
                          :value="option.value"
                        />
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="难度级别">
                      <el-select v-model="config.difficulty_level" placeholder="选择难度" class="w-100">
                        <el-option
                          v-for="option in difficultyLevelOptions"
                          :key="option.value"
                          :label="option.label"
                          :value="option.value"
                        />
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="文章长度">
                      <el-select v-model="config.article_length" placeholder="选择长度" class="w-100">
                        <el-option
                          v-for="option in articleLengthOptions"
                          :key="option.value"
                          :label="option.label"
                          :value="option.value"
                        />
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item v-if="showCustomWordCount" label="自定义字数">
                      <el-input-number 
                        v-model="config.custom_word_count" 
                        :min="50" 
                        :max="2000" 
                        :step="50"
                        class="w-100"
                      />
                    </el-form-item>
                    
                    <!-- 高级配置展开/折叠区域 -->
                    <el-divider content-position="center">
                      <el-button 
                        type="text" 
                        @click="showAdvancedSettings = !showAdvancedSettings"
                        class="toggle-advanced-btn"
                      >
                        {{ showAdvancedSettings ? '收起高级设置' : '展开高级设置' }}
                        <el-icon>
                          <component :is="showAdvancedSettings ? 'ArrowUp' : 'ArrowDown'" />
                        </el-icon>
                      </el-button>
                    </el-divider>
                    
                    <div v-show="showAdvancedSettings" class="advanced-settings">
                      <el-form-item label="语气风格">
                        <el-select v-model="config.tone_style" placeholder="选择风格" class="w-100">
                          <el-option
                            v-for="option in toneStyleOptions"
                            :key="option.value"
                            :label="option.label"
                            :value="option.value"
                          />
                        </el-select>
                      </el-form-item>
                      
                      <el-form-item label="主题领域">
                        <el-select v-model="config.topic" placeholder="选择主题" class="w-100">
                          <el-option
                            v-for="option in topicOptions"
                            :key="option.value"
                            :label="option.label"
                            :value="option.value"
                          />
                        </el-select>
                      </el-form-item>
                      
                      <el-form-item label="句子复杂度">
                        <el-slider 
                          v-model="config.sentence_complexity" 
                          :min="0" 
                          :max="1" 
                          :step="0.1"
                          :format-tooltip="(value: number) => `${Math.round(value * 100)}%`"
                          show-stops
                        />
                        <div class="slider-labels">
                          <span>简单</span>
                          <span>复杂</span>
                        </div>
                      </el-form-item>
                    </div>
                    
                    <el-form-item>
                      <el-button 
                        type="primary" 
                        @click="generateArticle" 
                        class="generate-btn"
                        :loading="isGenerating"
                        :disabled="wordList.length === 0 || isGenerating"
                      >
                        <el-icon v-if="!isGenerating"><MagicStick /></el-icon>
                        <span v-if="!isGenerating">生成英文文章</span>
                        <span v-else>{{ loadingText }}</span>
                      </el-button>
                    </el-form-item>
                  </el-form>
                </div>
              </el-card>
            </div>
          </el-col>
          
          <!-- 右侧：内容显示区域 -->
          <el-col :xs="24" :sm="24" :md="16" :lg="17" :xl="18" class="right-col">
            <div class="right-panel">
              <transition name="fade-scale">
                <el-card v-if="!articleGenerated" class="empty-state-card" shadow="hover">
                  <div class="empty-state">
                    <div class="empty-icon-wrapper">
                      <el-icon class="empty-icon"><DocumentAdd /></el-icon>
                    </div>
                    <h3>等待生成英文文章</h3>
                    <p>完成左侧的配置后点击"生成英文文章"按钮开始创建</p>
                    <div class="empty-steps">
                      <div class="step">
                        <div class="step-number">1</div>
                        <div class="step-text">输入单词</div>
                      </div>
                      <div class="step-arrow">
                        <el-icon><Right /></el-icon>
                      </div>
                      <div class="step">
                        <div class="step-number">2</div>
                        <div class="step-text">配置选项</div>
                      </div>
                      <div class="step-arrow">
                        <el-icon><Right /></el-icon>
                      </div>
                      <div class="step">
                        <div class="step-number">3</div>
                        <div class="step-text">生成文章</div>
                      </div>
                    </div>
                  </div>
                </el-card>
              </transition>
              
              <transition name="fade-scale">
                <div v-if="articleGenerated" class="content-tabs-container">
                  <el-tabs 
                    v-model="activeTab" 
                    type="border-card" 
                    class="content-tabs"
                    stretch
                    @tab-click="(tab: any) => {
                      if (tab.paneName === 'translation' && !translationData) getTranslation();
                      if (tab.paneName === 'questions' && !questionData) getQuestions();
                    }"
                  >
                    <el-tab-pane label="文章阅读" name="article">
                      <div class="tab-content-wrapper">
                        <ArticleDisplay :article-data="articleData" />
                      </div>
                    </el-tab-pane>
                    <el-tab-pane label="练习题" name="questions">
                      <div class="tab-content-wrapper">
                        <QuestionDisplay :question-data="questionData" />
                      </div>
                    </el-tab-pane> 
                    <el-tab-pane label="翻译和解释" name="translation">
                      <div class="tab-content-wrapper">
                        <TranslationDisplay :translation-data="translationData" />
                      </div>
                    </el-tab-pane>
                    
                    
                  </el-tabs>
                </div>
              </transition>
            </div>
          </el-col>
        </el-row>
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
.home-container {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.6s ease;
}

.app-loaded {
  opacity: 1;
  transform: translateY(0);
}

.app-header {
  padding: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  background: linear-gradient(90deg, #409EFF 0%, #53a8ff 100%);
  position: relative;
  overflow: hidden;
}

.app-header::before {
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
  text-align: center;
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-area {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 6px;
}

.logo-icon {
  font-size: 28px;
  color: #fff;
}

.app-header h1 {
  margin: 0;
  color: #fff;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: 1px;
}

.header-description p {
  margin: 10px 0 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
}

.header-actions {
  margin-top: 16px;
}

.el-main {
  padding: 32px 16px;
}

.main-content {
  margin: 0 auto;
}

.left-col, .right-col {
  margin-bottom: 20px;
}

.left-panel{
  height: 100%;
  width: 100%;
  transition: all 0.3s ease;
}
.right-panel {
  height: 100%;
  width: 100%;
  transition: all 0.3s ease;
}

.word-input-card {
  border-radius: 12px;
  background: #fff;
  transition: all 0.3s ease;
}

.word-input-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.panel-header .el-icon {
  color: #409EFF;
}

.config-section {
  margin-top: 24px;
}

.section-divider {
  margin-bottom: 20px;
}

.divider-content {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
}

.config-form {
  padding: 0 4px;
}

.generate-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  border-radius: 24px;
  margin-top: 8px;
  background: linear-gradient(90deg, #409EFF 0%, #53a8ff 100%);
  border: none;
  transition: all 0.3s ease;
  letter-spacing: 1px;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(64, 158, 255, 0.3);
}

.generate-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.empty-state-card {
  height: 100%;
  width: 100%;
  border-radius: 12px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
}

.empty-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon-wrapper {
  width: 80px;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f0f7ff, #e6f0ff);
  border-radius: 50%;
  margin-bottom: 24px;
  box-shadow: 0 8px 16px rgba(64, 158, 255, 0.15);
}

.empty-state .empty-icon {
  font-size: 40px;
  color: #409EFF;
}

.empty-state h3 {
  font-weight: 600;
  font-size: 20px;
  margin: 0 0 12px;
  color: #303133;
}

.empty-state p {
  color: #606266;
  max-width: 400px;
  margin: 0 0 32px;
  line-height: 1.6;
}

.empty-steps {
  display: flex;
  align-items: center;
  gap: 16px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.step:hover {
  transform: translateY(-4px);
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #409EFF;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 600;
  font-size: 18px;
  box-shadow: 0 4px 10px rgba(64, 158, 255, 0.3);
}

.step-text {
  color: #303133;
  font-size: 14px;
  font-weight: 500;
}

.step-arrow {
  color: #c0c4cc;
  font-size: 20px;
}

.content-tabs-container {
  height: 100%;
}

.content-tabs {
  border-radius: 12px;
  overflow: hidden;
  height: 100%;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  background-color: #fff;
}

.tab-content-wrapper {
  padding: 16px 0;
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

.w-100 {
  width: 100%;
}

/* 更优雅的过渡动画 */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(20px);
}

/* 响应式布局优化 */
@media (max-width: 992px) {
  .empty-state {
    padding: 40px 15px;
  }
  
  .empty-icon-wrapper {
    width: 70px;
    height: 70px;
  }
  
  .empty-state .empty-icon {
    font-size: 35px;
  }
  
  .generate-btn {
    height: 44px;
    font-size: 15px;
  }
}

@media (max-width: 768px) {
  .app-header h1 {
    font-size: 24px;
  }
  
  .logo-icon {
    font-size: 24px;
  }
  
  .header-content {
    padding: 16px;
  }
  
  .empty-steps {
    flex-direction: column;
    gap: 20px;
  }
  
  .step-arrow {
    transform: rotate(90deg);
  }
  
  .el-main {
    padding: 16px 12px;
  }
  
  .panel-header {
    font-size: 15px;
  }
  
  .word-input-card:hover {
    transform: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  }
  
  .generate-btn:hover:not(:disabled) {
    transform: none;
    box-shadow: none;
  }
  
  .tab-content-wrapper {
    padding: 8px 0;
  }
}

@media (max-width: 576px) {
  .app-header h1 {
    font-size: 20px;
  }
  
  .header-description p {
    font-size: 14px;
  }
  
  .empty-state h3 {
    font-size: 18px;
  }
  
  .empty-state p {
    font-size: 14px;
  }
  
  .step-number {
    width: 36px;
    height: 36px;
    font-size: 16px;
  }
  
  .step-text {
    font-size: 13px;
  }
  
  .footer-content p {
    font-size: 13px;
  }
  
  .divider-content {
    font-size: 13px;
  }
}

.toggle-advanced-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: #409EFF;
  font-size: 14px;
}

.advanced-settings {
  background-color: #f9f9f9;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  border: 1px solid #ebeef5;
  transition: all 0.3s;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  color: #909399;
  font-size: 12px;
}

/* 控制高级设置的动画 */
.advanced-settings-enter-active,
.advanced-settings-leave-active {
  transition: all 0.3s ease;
  max-height: 500px;
  overflow: hidden;
}

.advanced-settings-enter-from,
.advanced-settings-leave-to {
  max-height: 0;
  opacity: 0;
  margin: 0;
  padding-top: 0;
  padding-bottom: 0;
}
</style>
