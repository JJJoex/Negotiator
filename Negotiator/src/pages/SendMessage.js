
import axios from 'axios';

/**
 * 通用函数，用于发送 JSON 数据到后端。
 * @param {number} CODE - 一个正整数，用于表示操作代码。
 * @param {object} obj - 一个 JSON 对象，包含需要传递的数据。
 * @returns {Promise} 返回一个 Promise，解析为后端返回的数据。
 */
export async function sendJson(CODE, obj) {
  if (!Number.isInteger(CODE) || CODE <= 0) {
    throw new Error('CODE 必须是一个正整数');
  }
  if (typeof obj !== 'object' || obj === null) {
    throw new Error('obj 必须是一个有效的 JSON 对象');
  }

  const payload = { signal:CODE, data: obj }; // 整合 CODE 和 JSON 对象

  try {
    // const response = await axios.post('http://localhost:5000/api/negotiation', payload);
    const response = await axios.post('http://127.0.0.1:5000/api/negotiation', payload);
    // console.log("ffffffffff",response);
    return response.data; // 返回后端响应数据
  } catch (error) {
    console.error('请求失败:', error);
    throw error; // 抛出错误以供调用方处理
  }
}
