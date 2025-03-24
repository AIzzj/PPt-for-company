"""
新增功能测试脚本
"""
import os
import requests
import logging
import json
from PIL import Image
from io import BytesIO

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API基础URL
BASE_URL = "http://localhost:8000"

def test_template_preview():
    """测试模板预览功能"""
    logger.info("测试模板预览功能...")
    
    # 使用系统中最新的模板ID
    template_id = "template_77ed597496da4c259659c7c517998d0d"
    logger.info(f"使用模板ID: {template_id}")
    
    # 只测试第一张幻灯片
    test_indices = [0]  # 只测试第一张幻灯片
    for slide_index in test_indices:
        preview_url = f"{BASE_URL}/templates/{template_id}/preview?slide_index={slide_index}"
        logger.info(f"请求预览URL: {preview_url}")
        
        response = requests.get(preview_url)
        
        if response.status_code == 200:
            # 验证返回的是图片
            try:
                img = Image.open(BytesIO(response.content))
                width, height = img.size
                logger.info(f"幻灯片 {slide_index} 预览成功，图片尺寸: {width}x{height}")
            except Exception as e:
                logger.error(f"无法解析返回的图片: {str(e)}")
                return False
        else:
            logger.error(f"获取预览失败，状态码: {response.status_code}")
            if response.headers.get('content-type') == 'application/json':
                try:
                    error_json = response.json()
                    logger.error(f"错误信息: {error_json}")
                except:
                    logger.error(f"无法解析错误JSON，响应内容: {response.text[:200]}")
            return False
    
    return True

def test_batch_content_generation():
    """测试批量内容生成"""
    logger.info("测试批量内容生成...")
    
    # 使用系统中最新的模板ID
    template_id = "template_77ed597496da4c259659c7c517998d0d"
    logger.info(f"使用模板ID: {template_id}")
    
    try:
        # 获取模板详情
        response = requests.get(f"{BASE_URL}/templates/{template_id}")
        response.raise_for_status()
        template_data = response.json()
        
        # 准备批量请求
        requests_data = []
        
        # 遍历所有幻灯片和元素
        for slide in template_data["slides"]:
            for element in slide["elements"]:
                if element.get("is_placeholder", False):
                    # 确定内容类型
                    content_type = "paragraph"
                    if "title" in element["id"] or len(element.get("content", "")) < 30:
                        content_type = "title"
                    elif "•" in element.get("content", "") or "・" in element.get("content", ""):
                        content_type = "bullets"
                    
                    # 添加请求
                    requests_data.append({
                        "slide_id": slide["id"],
                        "element_id": element["id"],
                        "content_type": content_type,
                        "user_input": f"生成一个关于AI的{content_type}",
                        "style_guide": {
                            "tone": "专业",
                            "length": "简短"
                        }
                    })
        
        if not requests_data:
            logger.error("模板中没有可编辑的元素")
            return False
        
        # 发送批量生成请求
        response = requests.post(
            f"{BASE_URL}/content/generate-batch",
            json={
                "template_id": template_id,
                "content_requests": requests_data
            }
        )
        
        if response.status_code == 200:
            results = response.json()
            logger.info(f"批量生成成功，共生成 {len(results)} 个内容")
            
            # 显示部分生成结果
            for i, result in enumerate(results[:3]):  # 只显示前3个
                logger.info(f"内容 {i+1}: {result['content'][:50]}...")
            
            if len(results) > 3:
                logger.info(f"... 还有 {len(results) - 3} 个内容")
            
            # 测试用生成的内容创建PPT
            ppt_request = {
                "template_id": template_id,
                "content_mappings": [{
                    "slide_id": result["metadata"].get("slide_id") or slide_id_from_element_id(result["metadata"]["element_id"]),
                    "element_id": result["metadata"]["element_id"],
                    "content": result["content"],
                    "content_type": result["content_type"]
                } for result in results]
            }
            
            response = requests.post(f"{BASE_URL}/ppt/generate", json=ppt_request)
            if response.status_code == 200:
                task_data = response.json()
                logger.info(f"PPT生成任务创建成功，任务ID: {task_data['task_id']}")
                return True
            else:
                logger.error(f"创建PPT生成任务失败: {response.status_code}")
                if response.headers.get('content-type') == 'application/json':
                    logger.error(f"错误信息: {response.json()}")
                return False
        else:
            logger.error(f"批量生成内容失败，状态码: {response.status_code}")
            if response.headers.get('content-type') == 'application/json':
                logger.error(f"错误信息: {response.json()}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"测试批量内容生成时出错: {str(e)}")
        return False

def slide_id_from_element_id(element_id):
    """从元素ID提取幻灯片ID"""
    parts = element_id.split('_')
    if len(parts) >= 2:
        return f"slide_{parts[1]}"
    return f"slide_1"  # 默认返回第一张幻灯片

def main():
    """运行所有测试"""
    success = True
    
    # 测试模板预览
    if not test_template_preview():
        logger.error("模板预览测试失败")
        success = False
    
    # 测试批量内容生成
    if not test_batch_content_generation():
        logger.error("批量内容生成测试失败")
        success = False
    
    if success:
        logger.info("所有测试完成，测试成功！")
    else:
        logger.error("测试过程中出现错误")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 