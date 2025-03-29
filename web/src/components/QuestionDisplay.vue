<script setup lang="ts">
import { ref } from 'vue'
import { Check, Refresh, CircleCheckFilled, CircleCloseFilled, InfoFilled } from '@element-plus/icons-vue'

// 定义问题数据接口
interface Question {
  question: string;
  option: Record<string, string>;
  answer: string;
  explanation: {
    chinese_exp: string;
    english_exp: string;
  };
}

const props = defineProps<{
  questionData: Question[]
}>()

// 用户选择的答案
const userAnswers = ref<Record<string, string>>({})

// 是否显示答案和解释
const showAnswers = ref(false)

// 选择答案
const selectAnswer = (questionIndex: number, option: string) => {
  if (showAnswers.value) return // 如果已经显示答案，不允许更改
  userAnswers.value[questionIndex.toString()] = option
}

// 提交答案并查看解释
const submitAnswers = () => {
  showAnswers.value = true
}

// 重置测验
const resetQuiz = () => {
  userAnswers.value = {}
  showAnswers.value = false
}

// 计算选项样式
const getOptionClass = (questionIndex: number, option: string) => {
  if (!showAnswers.value) {
    return {
      'selected': userAnswers.value[questionIndex.toString()] === option,
      'disabled': false
    }
  }
  
  const isUserSelected = userAnswers.value[questionIndex.toString()] === option
  const isCorrect = props.questionData[questionIndex].answer === option
  
  return {
    'selected': isUserSelected,
    'correct': isCorrect,
    'incorrect': isUserSelected && !isCorrect,
    'disabled': true
  }
}
</script>

<template>
  <div v-if="questionData && questionData.length > 0" class="question-display">
    <!-- 所有问题列表 -->
    <div class="questions-list">
      <div v-for="(question, index) in questionData" :key="index" class="question-card">
        <div class="question-header">
          <div class="question-number">问题 {{ index + 1 }}</div>
          <div class="question-text">{{ question.question }}</div>
        </div>
        
        <div class="options-list">
          <div 
            v-for="(text, key) in question.option" 
            :key="key"
            class="option-card"
            :class="getOptionClass(index, key)"
            @click="selectAnswer(index, key)"
          >
            <div class="option-content">
              <div class="option-label">{{ key }}</div>
              <div class="option-text">{{ text }}</div>
            </div>
            <div class="option-indicator">
              <el-icon v-if="showAnswers && question.answer === key"><CircleCheckFilled /></el-icon>
              <el-icon v-else-if="showAnswers && userAnswers[index] === key"><CircleCloseFilled /></el-icon>
            </div>
          </div>
        </div>
        
        <!-- 答案解释 -->
        <transition name="fade">
          <div v-if="showAnswers" class="answer-explanation">
            <el-divider>
              <div class="divider-content">
                <el-icon><InfoFilled /></el-icon>
                <span>答案解释</span>
              </div>
            </el-divider>
            
            <div v-if="userAnswers[index] === question.answer" class="result-card correct">
              <el-icon><CircleCheckFilled /></el-icon>
              <span>回答正确!</span>
            </div>
            <div v-else-if="userAnswers[index]" class="result-card incorrect">
              <el-icon><CircleCloseFilled /></el-icon>
              <span>
                回答错误! 正确答案是: 
                <strong>{{ question.answer }}</strong>
              </span>
            </div>
            
            <div class="explanation-box">
              <el-tabs tab-position="top" type="border-card">
                <el-tab-pane label="中文解析">
                  <div class="explanation-content">{{ question.explanation.chinese_exp }}</div>
                </el-tab-pane>
                <el-tab-pane label="英文解析">
                  <div class="explanation-content">{{ question.explanation.english_exp }}</div>
                </el-tab-pane>
              </el-tabs>
            </div>
          </div>
        </transition>
      </div>
    </div>
    
    <!-- 底部按钮 -->
    <div class="question-actions">
      <el-button 
        v-if="!showAnswers" 
        type="primary" 
        @click="submitAnswers"
        :disabled="Object.keys(userAnswers).length < questionData.length"
        size="large"
        class="action-button"
      >
        <el-icon><Check /></el-icon>
        提交答案
      </el-button>
      
      <el-button 
        v-else 
        type="warning" 
        @click="resetQuiz"
        size="large"
        class="action-button"
      >
        <el-icon><Refresh /></el-icon>
        重新开始
      </el-button>
    </div>
  </div>
  
  <div v-else class="loading-questions">
    <div class="loading-card">
      <el-skeleton :rows="8" animated />
    </div>
  </div>
</template>

<style scoped>
.question-display {
  padding: 10px;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 32px;
  max-width: 800px;
  margin: 0 auto;
  padding-bottom: 32px;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.question-number {
  font-size: 16px;
  font-weight: 600;
  width: auto;
  color: #409EFF;
  background-color: rgba(64, 158, 255, 0.1);
  padding: 6px 12px;
  border-radius: 20px;
}

.question-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.question-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.question-text {
  font-size: 18px;
  font-weight: 600;
  max-width: 600px;
  margin-bottom: 24px;
  line-height: 1.6;
  color: #303133;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.option-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-radius: 10px;
  border: 1px solid #ebeef5;
  background-color: #f9fafc;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-card:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #f5f7fa;
}

.option-card.selected {
  border-color: #409EFF;
  background-color: rgba(64, 158, 255, 0.1);
}

.option-card.correct {
  border-color: #67C23A;
  background-color: rgba(103, 194, 58, 0.1);
}

.option-card.incorrect {
  border-color: #F56C6C;
  background-color: rgba(245, 108, 108, 0.1);
}

.option-card.disabled {
  cursor: default;
}

.option-content {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.option-label {
  font-weight: 600;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  background-color: #ebeef5;
  color: #606266;
}

.selected .option-label {
  background-color: #409EFF;
  color: #fff;
}

.correct .option-label {
  background-color: #67C23A;
  color: #fff;
}

.incorrect .option-label {
  background-color: #F56C6C;
  color: #fff;
}

.option-text {
  flex: 1;
  font-size: 15px;
  color: #303133;
}

.option-indicator {
  color: inherit;
  font-size: 18px;
}

.correct .option-indicator {
  color: #67C23A;
}

.incorrect .option-indicator {
  color: #F56C6C;
}

.divider-content {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.answer-explanation {
  margin-top: 32px;
}

.result-card {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding: 16px;
  border-radius: 10px;
}

.result-card.correct {
  background-color: rgba(103, 194, 58, 0.1);
  color: #67C23A;
}

.result-card.incorrect {
  background-color: rgba(245, 108, 108, 0.1);
  color: #F56C6C;
}

.explanation-box {
  margin-top: 20px;
}

.explanation-content {
  padding: 16px;
  line-height: 1.8;
  white-space: pre-wrap;
  color: #303133;
  font-size: 15px;
}

.question-actions {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

.action-button {
  min-width: 160px;
  height: 48px;
  font-size: 16px;
  transition: all 0.3s;
  border-radius: 24px;
}

.action-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.loading-questions {
  padding: 20px;
}

.loading-card {
  padding: 24px;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

/* 增强响应式布局 */
@media (max-width: 991px) {
  .question-card {
    padding: 20px;
  }
  
  .option-card {
    padding: 14px;
  }
  
  .explanation-content {
    padding: 14px;
  }
}

@media (max-width: 768px) {
  .question-display {
    padding: 5px;
  }
  
  .progress-card {
    flex-direction: column;
    gap: 16px;
    align-items: center;
    padding: 16px;
  }
  
  .question-text {
    font-size: 16px;
    padding-bottom: 12px;
    margin-bottom: 16px;
  }
  
  .option-content {
    gap: 8px;
  }
  
  .option-label {
    width: 28px;
    height: 28px;
    font-size: 13px;
  }
  
  .option-text {
    font-size: 14px;
  }
  
  .action-button {
    min-width: 140px;
    height: 42px;
    font-size: 15px;
  }
  
  .result-card {
    padding: 12px;
  }
  
  .explanation-content {
    font-size: 14px;
    padding: 12px;
    line-height: 1.6;
  }
}

@media (max-width: 576px) {
  .progress-info {
    gap: 10px;
  }
  
  .progress-count {
    font-size: 16px;
  }
  
  .progress-label {
    font-size: 12px;
  }
  
  .nav-buttons {
    gap: 8px;
  }
  
  .question-card {
    padding: 16px;
  }
  
  .option-card {
    padding: 12px;
  }
  
  .option-label {
    width: 24px;
    height: 24px;
    font-size: 12px;
  }
  
  .action-button {
    min-width: 120px;
    height: 38px;
    font-size: 14px;
  }
}
</style>
