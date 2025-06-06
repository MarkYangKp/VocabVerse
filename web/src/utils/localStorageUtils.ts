// 定义学习记录的数据类型
export interface LearningRecord {
  id: string;
  timestamp: number;
  words: string[];
  article: {
    record_id?: number;
    passage_needs?: number;
    passage_type?: number;
    // 新API字段
    article_type?: string;
    difficulty_level?: string;
    tone_style?: string; 
    topic?: string;
    sentence_complexity?: number;
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
  
  // 首先检查是否已存在相同内容的记录（基于文章内容和单词列表）
  const existingContentIndex = records.findIndex(r => 
    r.article.article === record.article.article && 
    JSON.stringify(r.words.sort()) === JSON.stringify([...record.words].sort())
  );
  
  if (existingContentIndex !== -1) {
    // 如果存在相同内容的记录，则更新该记录，保留原ID
    const existingRecord = records[existingContentIndex];
    
    // 合并新记录的数据到已存在的记录中
    records[existingContentIndex] = {
      ...existingRecord,
      timestamp: record.timestamp, // 更新时间戳为最新
      // 保留已有的翻译和问题，除非新记录提供了这些内容
      translation: record.translation || existingRecord.translation,
      questions: record.questions || existingRecord.questions
    };
  } else {
    // 如果不存在相同内容的记录，则检查ID是否重复
    const existingIdIndex = records.findIndex(r => r.id === record.id);
    if (existingIdIndex !== -1) {
      records[existingIdIndex] = record;
    } else {
      records.push(record);
    }
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
