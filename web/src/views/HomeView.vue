<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import { useRouter } from 'vue-router'
import WordInput from '@/components/WordInput.vue'
import ArticleDisplay from '@/components/ArticleDisplay.vue'
import TranslationDisplay from '@/components/TranslationDisplay.vue'
import QuestionDisplay from '@/components/QuestionDisplay.vue'
import { saveLearningRecord } from '@/utils/localStorageUtils'

// 定义类型
interface GenerationConfig {
  passageNeeds: number // 难度类型，1-考研难度，2-六级难度，等
  passageType: number // 文章类型，1-议论文，2-说明文，等
  wordNum: string // 词数范围，如"150-200"
}

// 定义响应式状态
const wordList = ref<string[]>([])
const config = reactive<GenerationConfig>({
  passageNeeds: 2, // 默认六级难度
  passageType: 1, // 默认议论文
  wordNum: '150-200' // 默认词数范围
})

// 文章状态
const articleGenerated = ref(false)
const articleData = ref<any>(null)
const translationData = ref<any>(null)
const questionData = ref<any>(null)
const activeTab = ref('article')
const recordId = ref<number | null>(null)

// 获取路由器实例
const router = useRouter()

// 接收从子组件传来的单词列表
const onWordsUpdated = (words: string[]) => {
  wordList.value = words
}
//环境变量中的API基础路径
const baseApiUrl = import.meta.env.VITE_API_BASE_URL

// API基础路径
const apiUrl = baseApiUrl+'/api/learning';

// 生成文章
const generateArticle = async () => {
  if (wordList.value.length === 0) {
    ElMessage.warning('请先输入或上传单词')
    return
  }

  const loading = ElLoading.service({
    lock: true,
    text: '正在生成文章，请稍候...',
    background: 'rgba(255, 255, 255, 0.7)'
  })

  try {
    const response = await fetch(`${apiUrl}/word2passage`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        words: wordList.value,
        passage_needs: config.passageNeeds,
        passage_type: config.passageType,
        word_num: config.wordNum
      })
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

    // 生成文章后自动在后台获取翻译和问题数据
    getTranslation();
    getQuestions();

  } catch (error) {
    console.error('生成文章失败:', error);
    ElMessage.error('生成文章失败，请稍后再试');
  } finally {
    loading.close();
  }
}

// 获取翻译和解释
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
    const response = await fetch(`${apiUrl}/passage2explanation`, {
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

// 获取习题
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
    const response = await fetch(`${apiUrl}/passage2question`, {
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
            <h1>词境——每个单词都值得一个故事</h1>
          </div>
          <div class="header-description">
            <p>输入单词，AI智能生成记忆文章</p>
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
                    <el-form-item label="文章难度">
                      <el-select v-model="config.passageNeeds" placeholder="选择难度" class="w-100">
                        <el-option :value="1" label="考研难度" />
                        <el-option :value="2" label="六级难度" />
                        <el-option :value="3" label="易于记忆" />
                        <el-option :value="4" label="四级难度" />
                        <el-option :value="5" label="高中水平" />
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="文章类型">
                      <el-select v-model="config.passageType" placeholder="选择类型" class="w-100">
                        <el-option :value="1" label="议论文" />
                        <el-option :value="2" label="说明文" />
                        <el-option :value="3" label="短篇小说" />
                        <el-option :value="4" label="叙事文" />
                        <el-option :value="5" label="描写文" />
                        <el-option :value="6" label="商业报告" />
                        <el-option :value="7" label="技术报告" />
                        <el-option :value="8" label="新闻报道" />
                        <el-option :value="9" label="社论" />
                        <el-option :value="10" label="博客文章" />
                        <el-option :value="11" label="社交媒体文案" />
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="字数范围">
                      <el-input v-model="config.wordNum" placeholder="如：100-200">
                        <template #prefix>
                          <el-icon><Document /></el-icon>
                        </template>
                      </el-input>
                    </el-form-item>
                    
                    <el-form-item>
                      <el-button type="primary" @click="generateArticle" class="generate-btn">
                        <el-icon><MagicStick /></el-icon>
                        生成英文文章
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
              <transition name="fade">
                <el-card v-if="!articleGenerated" class="empty-state-card" shadow="hover">
                  <div class="empty-state">
                    <div class="empty-icon-wrapper">
                      <el-icon class="empty-icon"><DocumentAdd /></el-icon>
                    </div>
                    <h3>尚未生成英文文章</h3>
                    <p>请在左侧输入单词并配置文章生成选项，然后点击"生成英文文章"按钮</p>
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
                        <div class="step-text">生成英文文章</div>
                      </div>
                    </div>
                  </div>
                </el-card>
              </transition>
              
              <transition name="fade">
                <div v-if="articleGenerated" class="content-tabs-container">
                  <el-tabs 
                    v-model="activeTab" 
                    type="border-card" 
                    class="content-tabs"
                    @tab-click="(tab: any) => {
                      if (tab.paneName === 'translation' && !translationData) getTranslation();
                      if (tab.paneName === 'questions' && !questionData) getQuestions();
                    }"
                  >
                    <el-tab-pane label="文章阅读" name="article">
                      <ArticleDisplay :article-data="articleData" />
                    </el-tab-pane>
                    
                    <el-tab-pane label="翻译和解释" name="translation">
                      <TranslationDisplay :translation-data="translationData" />
                    </el-tab-pane>
                    
                    <el-tab-pane label="练习题" name="questions">
                      <QuestionDisplay :question-data="questionData" />
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
            Word2LLM - 使用AI增强英语学习体验
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
  padding: 24px;
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
  /* max-width: 1440px; */
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

.generate-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(64, 158, 255, 0.3);
}

.empty-state-card {
  height: 100%;
  width: 100%;
  border-radius: 12px;
  transition: all 0.3s ease;
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
  background: linear-gradient(145deg, #f0f2f5, #e6e9ec);
  border-radius: 50%;
  margin-bottom: 24px;
}

.empty-state .empty-icon {
  font-size: 40px;
  color: #409EFF;
}

.empty-state h3 {
  font-weight: 600;
  font-size: 18px;
  margin: 0 0 12px;
  color: #303133;
}

.empty-state p {
  color: #909399;
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
}

.step-number {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #409EFF;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
}

.step-text {
  color: #606266;
  font-size: 14px;
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

.w-100 {
  width: 100%;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 响应式布局调整 */
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
    gap: 12px;
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
    font-size: 16px;
  }
  
  .empty-state p {
    font-size: 14px;
  }
  
  .step-number {
    width: 30px;
    height: 30px;
    font-size: 14px;
  }
  
  .step-text {
    font-size: 12px;
  }
  
  .footer-content p {
    font-size: 13px;
  }
}
</style>
