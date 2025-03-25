// 定义学习记录的数据类型
export interface LearningRecord {
  id: string;
  timestamp: number;
  words: string[];
  article: {
    record_id: number;
    passage_needs: number;
    passage_type: number;
    word_count: number;
    article: string;
    alert?: string;
  };
  translation?: {
    translation: string;
    language_points: {
      word: string;
      explanation: string;
    }[];
  };
  questions?: any[];
}

// 本地存储的键名
const LEARNING_RECORDS_KEY = 'word2llm_learning_records';

/**
 * 保存学习记录到本地存储
 */
export function saveLearningRecord(record: LearningRecord): void {
  const records = getAllLearningRecords();
  
  // 检查是否已存在相同ID的记录，如果存在则更新
  const existingIndex = records.findIndex(r => r.id === record.id);
  if (existingIndex !== -1) {
    records[existingIndex] = record;
  } else {
    records.push(record);
  }
  
  // 按时间戳降序排序（最新的记录在前）
  records.sort((a, b) => b.timestamp - a.timestamp);
  
  // 最多保存50条记录
  const limitedRecords = records.slice(0, 50);
  
  localStorage.setItem(LEARNING_RECORDS_KEY, JSON.stringify(limitedRecords));
}

/**
 * 获取所有学习记录
 */
export function getAllLearningRecords(): LearningRecord[] {
  const recordsString = localStorage.getItem(LEARNING_RECORDS_KEY);
  if (!recordsString) {
    return [];
  }
  
  try {
    return JSON.parse(recordsString);
  } catch (error) {
    console.error('解析学习记录失败:', error);
    return [];
  }
}

/**
 * 获取单个学习记录
 */
export function getLearningRecord(id: string): LearningRecord | null {
  const records = getAllLearningRecords();
  return records.find(record => record.id === id) || null;
}

/**
 * 删除学习记录
 */
export function deleteLearningRecord(id: string): void {
  const records = getAllLearningRecords();
  const updatedRecords = records.filter(record => record.id !== id);
  localStorage.setItem(LEARNING_RECORDS_KEY, JSON.stringify(updatedRecords));
}

/**
 * 清空所有学习记录
 */
export function clearAllLearningRecords(): void {
  localStorage.removeItem(LEARNING_RECORDS_KEY);
}
