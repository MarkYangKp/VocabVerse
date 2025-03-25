<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { getAllLearningRecords } from '@/utils/localStorageUtils'

const props = defineProps({
  maxWords: {
    type: Number,
    default: 50
  }
})

const emit = defineEmits(['words-updated'])

const manualInput = ref('')
const wordList = ref<string[]>([])
const activeTab = ref('manual')
const isUploadingImage = ref(false)
const uploadProgress = ref(0)

const editingWord = ref('')  // 当前正在编辑的单词
const editingWordValue = ref('')  // 编辑框中的值
const editInput = ref<HTMLInputElement | null>(null)  // 编辑输入框的引用

// 添加单词
const addWords = () => {
  if (!manualInput.value) {
    ElMessage.warning('请输入单词')
    return
  }
  
  // 解析输入的单词（按逗号、空格或换行分隔）
  const words = manualInput.value
    .split(/[,，\s\n]+/)
    .filter(word => word.trim() !== '')
    .map(word => word.trim().toLowerCase())
  
  // 去重并添加到单词列表
  const uniqueWords = [...new Set([...wordList.value, ...words])]
  
  // 如果超过最大数量，截取并提示
  if (uniqueWords.length > props.maxWords) {
    wordList.value = uniqueWords.slice(0, props.maxWords)
    ElMessage.warning(`单词数量已达上限 (${props.maxWords})`)
  } else {
    wordList.value = uniqueWords
  }
  
  // 清空输入框
  manualInput.value = ''
}
// .env文件加载BASERUL
const baseApiUrl = import.meta.env.VITE_BASE_API_URL

// API基础路径
const apiUrl = baseApiUrl + '/api/learning';

// 上传图片并识别单词
const uploadImage = (file: File) => {
  // 检查文件类型
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('请上传图片文件')
    return false
  }
  
  // 开始上传
  isUploadingImage.value = true
  uploadProgress.value = 0
  
  // 创建上传进度处理函数
  const updateProgress = () => {
    const timer = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10
      } else {
        clearInterval(timer)
      }
    }, 200)
    
    return timer
  }
  
  const progressTimer = updateProgress()
  
  // 创建FormData对象
  const formData = new FormData()
  formData.append('image', file)
  
  // 发送API请求
  fetch(`${apiUrl}/upload_image`, {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`API响应错误: ${response.status}`)
    }
    return response.json()
  })
  .then(data => {
    uploadProgress.value = 100
    
    // 处理识别的单词
    const recognizedWords = data.words || []
    
    // 添加识别的单词
    const uniqueWords = [...new Set([...wordList.value, ...recognizedWords])]
    
    if (uniqueWords.length > props.maxWords) {
      wordList.value = uniqueWords.slice(0, props.maxWords)
      ElMessage.warning(`单词数量已达上限 (${props.maxWords})`)
    } else {
      wordList.value = uniqueWords
    }
    
    ElMessage.success(`成功从图片中识别出 ${recognizedWords.length} 个单词`)
  })
  .catch(error => {
    console.error('上传图片失败:', error)
    ElMessage.error('上传图片失败，请稍后再试')
  })
  .finally(() => {
    clearInterval(progressTimer)
    setTimeout(() => {
      isUploadingImage.value = false
    }, 500)
  })
  
  return false // 阻止默认的上传行为
}

// 清空所有单词
const clearAllWords = () => {
  if (wordList.value.length === 0) return
  
  wordList.value = []
  ElMessage.success('已清空所有单词')
}

// 移除单个单词
const removeWord = (word: string) => {
  wordList.value = wordList.value.filter(w => w !== word)
}

// 开始编辑单词
const startEditing = (word: string) => {
  editingWord.value = word
  editingWordValue.value = word
  
  // 在下一个渲染周期聚焦输入框
  nextTick(() => {
    if (editInput.value) {
      editInput.value?.focus()
    }
  })
}

// 保存编辑后的单词
const saveEditedWord = () => {
  if (!editingWordValue.value.trim()) {
    ElMessage.warning('单词不能为空')
    return
  }
  
  // 获取编辑前单词的索引
  const index = wordList.value.indexOf(editingWord.value)
  if (index !== -1) {
    // 检查新单词是否已存在（避免重复）
    const newWord = editingWordValue.value.trim().toLowerCase()
    if (newWord !== editingWord.value && wordList.value.includes(newWord)) {
      ElMessage.warning('该单词已存在')
    } else {
      // 更新单词
      wordList.value = wordList.value.map(w => 
        w === editingWord.value ? newWord : w
      )
      ElMessage.success('已成功修改单词')
    }
  }
  
  // 完成编辑
  cancelEditing()
}

// 取消编辑
const cancelEditing = () => {
  editingWord.value = ''
  editingWordValue.value = ''
}

// 监听单词列表变化，向父组件发送更新
watch(wordList, (newWords) => {
  emit('words-updated', newWords)
}, { deep: true })

// 历史单词记录列表
const historyWordsDialogVisible = ref(false)
const historySets = ref<{id: string, timestamp: number, words: string[]}[]>([])

// 打开历史单词选择对话框
const openHistoryDialog = () => {
  // 获取历史单词记录
  const records = getAllLearningRecords()
  historySets.value = records.map(record => ({
    id: record.id,
    timestamp: record.timestamp,
    words: record.words
  }))
  
  historyWordsDialogVisible.value = true
}

// 从历史记录中导入单词
const importWordsFromHistory = (words: string[]) => {
  if (!words || words.length === 0) {
    return
  }
  
  // 去重并添加到单词列表
  const uniqueWords = [...new Set([...wordList.value, ...words])]
  
  // 如果超过最大数量，截取并提示
  if (uniqueWords.length > props.maxWords) {
    wordList.value = uniqueWords.slice(0, props.maxWords)
    ElMessage.warning(`单词数量已达上限 (${props.maxWords})`)
  } else {
    wordList.value = uniqueWords
  }
  
  historyWordsDialogVisible.value = false
  ElMessage.success(`已导入 ${words.length} 个单词`)
}

// 格式化日期
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
</script>

<template>
  <div class="word-input-container">
    <el-tabs v-model="activeTab" type="border-card" class="input-tabs">
      <el-tab-pane label="手动输入" name="manual">
        <div class="tab-content">
          <el-form>
            <el-form-item>
              <el-input
                v-model="manualInput"
                type="textarea"
                :rows="4"
                placeholder="输入单词，多个单词可用逗号、空格或换行分隔"
                @keyup.ctrl.enter="addWords"
                class="word-textarea"
              />
            </el-form-item>
            <el-form-item>
              <div class="input-actions">
                <el-button type="primary" @click="addWords" class="add-button">
                  <el-icon><Plus /></el-icon>
                  添加单词
                </el-button>
                <el-tooltip content="按Ctrl+Enter快速添加" placement="top" effect="light">
                  <span class="keyboard-shortcut">
                    <el-icon><Key /></el-icon>
                    Ctrl+Enter
                  </span>
                </el-tooltip>
              </div>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="图片识别" name="image">
        <div class="tab-content">
          <div class="image-upload-area">
            <el-upload
              class="image-uploader"
              action="#"
              :http-request="() => {}"
              :before-upload="uploadImage"
              :show-file-list="false"
              drag
              accept="image/*"
              :disabled="isUploadingImage"
            >
              <div v-if="!isUploadingImage" class="upload-content">
                <el-icon class="upload-icon"><Picture /></el-icon>
                <div class="upload-text">拖拽图片到此处或 <em>点击上传</em></div>
                <div class="upload-tip">支持jpg、png、jpeg等常见图片格式</div>
              </div>
              <div v-else class="upload-progress">
                <el-progress 
                  :percentage="uploadProgress" 
                  :stroke-width="8" 
                  status="success"
                />
                <p>正在处理图片和识别单词...</p>
              </div>
            </el-upload>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="历史导入" name="history">
        <div class="tab-content">
          <div class="history-import-area">
            <div class="import-description">
              <el-icon><Clock /></el-icon>
              <p>从历史学习记录中导入已使用过的单词</p>
            </div>
            <el-button type="primary" @click="openHistoryDialog" class="import-button">
              <el-icon><Files /></el-icon>
              浏览历史单词集
            </el-button>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
    
    <div class="word-list-section">
      <div class="word-list-header">
        <div class="word-count">
          <el-icon><Collection /></el-icon>
          <span>已添加单词 <strong>{{ wordList.length }}/{{ props.maxWords }}</strong></span>
        </div>
        <el-button 
          v-if="wordList.length > 0" 
          type="danger" 
          size="small"
          @click="clearAllWords"
          class="clear-btn"
        >
          <el-icon><Delete /></el-icon>
          清空
        </el-button>
      </div>
      
      <transition-group name="list" tag="div" class="word-tag-container">
        <div v-if="wordList.length === 0" key="empty" class="empty-word-list">
          <el-empty description="还没有添加单词" :image-size="60">
            <template #image>
              <el-icon class="empty-icon"><Edit /></el-icon>
            </template>
          </el-empty>
        </div>
        
        <div v-else key="tags" class="word-tag-list">
          <div v-for="word in wordList" :key="word" class="word-tag-wrapper">
            <template v-if="editingWord === word">
              <div class="editing-tag">
                <el-input 
                  v-model="editingWordValue" 
                  size="small" 
                  @keyup.enter="saveEditedWord"
                  @keyup.esc="cancelEditing"
                  ref="editInput"
                  class="word-edit-input"
                />
                <div class="editing-actions">
                  <el-button 
                    type="primary" 
                    size="small" 
                    circle 
                    @click="saveEditedWord"
                    class="edit-action-btn"
                  >
                    <el-icon><Check /></el-icon>
                  </el-button>
                  <el-button 
                    type="info" 
                    size="small" 
                    circle 
                    @click="cancelEditing"
                    class="edit-action-btn"
                  >
                    <el-icon><Close /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>
            <el-tag
              v-else
              closable
              :disable-transitions="false"
              @close="removeWord(word)"
              class="word-tag"
              effect="light"
            >
              {{ word }}
              <el-icon class="edit-icon" @click.stop="startEditing(word)"><Edit /></el-icon>
            </el-tag>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- 历史单词选择对话框 -->
    <el-dialog
      v-model="historyWordsDialogVisible"
      title="选择历史单词集"
      width="70%"
    >
      <div v-if="historySets.length === 0" class="empty-history-sets">
        <el-empty description="没有可用的历史单词记录" />
      </div>
      <div v-else class="history-sets-list">
        <el-card 
          v-for="item in historySets"
          :key="item.id"
          class="history-set-card"
          shadow="hover"
          @click="importWordsFromHistory(item.words)"
        >
          <div class="history-set-header">
            <div class="history-date">{{ formatDate(item.timestamp) }}</div>
            <el-tag size="small" type="info" effect="plain">{{ item.words.length }}个单词</el-tag>
          </div>
          
          <div class="history-set-words">
            <el-tag 
              v-for="(word, index) in item.words.slice(0, 10)" 
              :key="word+index"
              size="small"
              class="word-history-tag"
            >
              {{ word }}
            </el-tag>
            <el-tag v-if="item.words.length > 10" size="small" type="info">
              +{{ item.words.length - 10 }} 个单词
            </el-tag>
          </div>
          
          <div class="click-hint">
            <el-icon><Right /></el-icon>
            点击导入这组单词
          </div>
        </el-card>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.word-input-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-tabs {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.tab-content {
  padding: 20px 12px 12px;
}

.word-textarea {
  border-radius: 8px;
  transition: all 0.3s;
}

.word-textarea:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.input-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.add-button {
  border-radius: 8px;
  transition: all 0.2s;
}

.add-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.keyboard-shortcut {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #909399;
  background-color: #f2f6fc;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.image-upload-area {
  margin-bottom: 10px;
}

.image-uploader {
  border-radius: 8px;
  overflow: hidden;
}

.upload-content {
  padding: 20px;
  text-align: center;
}

.upload-icon {
  font-size: 38px;
  color: #409EFF;
  margin-bottom: 12px;
  opacity: 0.8;
}

.upload-text {
  color: #606266;
  font-size: 16px;
  margin-bottom: 6px;
}

.upload-text em {
  color: #409EFF;
  font-style: normal;
  font-weight: 500;
}

.upload-tip {
  color: #909399;
  font-size: 12px;
}

.upload-progress {
  padding: 24px;
  text-align: center;
}

.upload-progress p {
  margin-top: 12px;
  color: #409EFF;
}

.word-list-section {
  background: linear-gradient(145deg, #f8f9fa, #eef2f8);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.word-list-section:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.word-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.word-count {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #606266;
}

.word-count .el-icon {
  color: #409EFF;
}

.word-count strong {
  color: #409EFF;
  font-weight: 600;
}

.clear-btn {
  transition: all 0.2s;
  border-radius: 8px;
}

.clear-btn:hover {
  transform: translateY(-2px);
}

.word-tag-container {
  min-height: 50px;
}

.empty-word-list {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100px;
}

.empty-icon {
  font-size: 32px;
  color: #c0c4cc;
}

.word-tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.word-tag-wrapper {
  position: relative;
  display: inline-flex;
}

.word-tag {
  display: flex;
  align-items: center;
  gap: 5px;
}

.edit-icon {
  font-size: 12px;
  margin-left: 5px;
  color: #909399;
  cursor: pointer;
  opacity: 0.7;
  transition: all 0.2s;
}

.edit-icon:hover {
  opacity: 1;
  color: #409EFF;
  transform: scale(1.2);
}

.editing-tag {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #fff;
  padding: 4px 8px;
  border-radius: 16px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}

.word-edit-input {
  width: 120px;
}

.editing-actions {
  display: flex;
  gap: 5px;
}

.edit-action-btn {
  padding: 4px;
  transform: scale(0.85);
}

/* 列表动画 */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.history-import-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  padding: 20px 0;
}

.import-description {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}

.import-description .el-icon {
  font-size: 36px;
  color: #409EFF;
  opacity: 0.8;
}

.import-description p {
  color: #606266;
  margin: 0;
}

.import-button {
  padding: 12px 24px;
  border-radius: 8px;
}

.history-sets-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 60vh;
  overflow-y: auto;
}

.history-set-card {
  cursor: pointer;
  transition: all 0.3s;
}

.history-set-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.history-set-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.history-date {
  color: #606266;
  font-size: 14px;
}

.history-set-words {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.word-history-tag {
  margin: 0;
}

.click-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #409EFF;
  font-size: 13px;
}

.empty-history-sets {
  padding: 20px;
  display: flex;
  justify-content: center;
}

/* 增强响应式布局 */
@media (max-width: 991px) {
  .tab-content {
    padding: 16px 10px 10px;
  }
  
  .upload-content {
    padding: 16px;
  }
  
  .upload-icon {
    font-size: 32px;
    margin-bottom: 10px;
  }
  
  .word-list-section {
    padding: 14px;
  }
}

@media (max-width: 768px) {
  .word-input-container {
    gap: 16px;
  }
  
  .input-actions {
    flex-wrap: wrap;
  }
  
  .keyboard-shortcut {
    margin-top: 8px;
  }
  
  .add-button:hover {
    transform: none;
  }
  
  .upload-text {
    font-size: 15px;
  }
  
  .upload-tip {
    font-size: 11px;
  }
  
  .word-list-section:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    transform: none;
  }
  
  .word-tag-list {
    gap: 8px;
  }
  
  .word-edit-input {
    width: 90px;
  }
}

@media (max-width: 576px) {
  .tab-content {
    padding: 14px 8px 8px;
  }
  
  .upload-icon {
    font-size: 28px;
    margin-bottom: 8px;
  }
  
  .word-list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .clear-btn {
    align-self: flex-end;
  }
  
  .empty-icon {
    font-size: 28px;
  }
  
  .import-description .el-icon {
    font-size: 30px;
  }
  
  .import-button {
    padding: 10px 20px;
    font-size: 14px;
  }
  
  .history-set-card:hover {
    transform: none;
  }
  
  .history-set-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
