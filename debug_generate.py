import requests
import json
import logging
import os
import uuid
import time
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_ppt(template_id, elements_data):
    """
    使用API生成PPT
    """
    url = "http://127.0.0.1:8000/ppt/generate"
    
    # 准备content_mappings (根据API要求的格式)
    content_mappings = []
    
    # ContentType映射
    content_type_map = {
        "shape_1": "title",  # 假设shape_1是标题
        "shape_2": "subtitle"  # 假设shape_2是副标题
    }
    
    for slide_id, elements in elements_data.items():
        for element_id, element_data in elements.items():
            # 根据element_id决定content_type
            content_type = content_type_map.get(element_id, "body")  # 默认为body
            
            mapping = {
                "request_id": str(uuid.uuid4()),
                "slide_id": slide_id,
                "element_id": element_id,
                "content": element_data.get("content"),
                "content_type": content_type,
                "metadata": {
                    "style": element_data.get("style", {})
                }
            }
            content_mappings.append(mapping)
    
    # 准备请求数据
    data = {
        "template_id": template_id,
        "content_mappings": content_mappings
    }
    
    # 发送POST请求
    logger.info(f"发送生成PPT请求，模板ID: {template_id}")
    logger.info(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应头: {response.headers}")
        
        if response.status_code == 200:
            # 成功创建生成任务
            response_data = response.json()
            logger.info(f"任务创建成功: {response_data}")
            
            # 获取任务ID
            task_id = response_data.get("task_id")
            if task_id:
                logger.info(f"任务ID: {task_id}")
                
                # 轮询任务状态
                status_url = f"http://127.0.0.1:8000/ppt/status/{task_id}"
                max_attempts = 30  # 增加到30次尝试，相当于30秒
                for attempt in range(max_attempts):
                    logger.info(f"检查任务状态... (尝试 {attempt+1}/{max_attempts})")
                    status_response = requests.get(status_url)
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        logger.info(f"任务状态: {status_data}")
                        
                        if status_data.get("status") == "completed":
                            # 下载生成的PPT
                            download_url = f"http://127.0.0.1:8000/ppt/download/{task_id}"
                            logger.info(f"开始下载PPT: {download_url}")
                            
                            download_response = requests.get(download_url)
                            if download_response.status_code == 200:
                                # 保存生成的PPT
                                output_file = f"generated_ppt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
                                with open(output_file, "wb") as f:
                                    f.write(download_response.content)
                                logger.info(f"已保存生成的PPT: {output_file}")
                                return True
                            else:
                                logger.error(f"下载PPT失败: {download_response.text}")
                                return False
                    elif status_response.status_code != 200:
                        logger.error(f"检查任务状态时出错: {status_response.status_code} - {status_response.text}")
                    
                    # 等待1秒后再次检查
                    time.sleep(1)
                
                # 尝试直接下载一次
                logger.info("尝试直接下载PPT...")
                download_url = f"http://127.0.0.1:8000/ppt/download/{task_id}"
                try:
                    download_response = requests.get(download_url)
                    if download_response.status_code == 200:
                        output_file = f"generated_ppt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
                        with open(output_file, "wb") as f:
                            f.write(download_response.content)
                        logger.info(f"已保存生成的PPT: {output_file}")
                        return True
                    else:
                        logger.error(f"直接下载PPT失败: {download_response.status_code} - {download_response.text}")
                except Exception as e:
                    logger.error(f"直接下载PPT时出错: {e}")
                
                logger.error("PPT生成超时")
                return False
            else:
                logger.error(f"无法获取任务ID: {response_data}")
                return False
        else:
            try:
                logger.error(f"生成PPT失败: {response.text}")
                try:
                    json_response = response.json()
                    logger.error(f"错误详情: {json.dumps(json_response, ensure_ascii=False, indent=2)}")
                except:
                    pass
            except:
                logger.error(f"生成PPT失败，无法解析响应: {response.text[:200]}")
            return False
    except Exception as e:
        logger.error(f"发送请求时出错: {e}")
        return False

def main():
    # 获取最近上传的模板ID
    try:
        # 从临时文件中获取最近上传的模板ID
        if os.path.exists("last_template_id.txt"):
            with open("last_template_id.txt", "r") as f:
                template_id = f.read().strip()
            logger.info(f"使用最近上传的模板ID: {template_id}")
        else:
            # 使用默认模板ID
            template_id = "42438a4fe845420bb98f5938eee4d8b9"  # 从上次运行的输出中获取
            logger.info(f"未找到最近上传的模板ID，使用默认ID: {template_id}")
    except Exception as e:
        template_id = "42438a4fe845420bb98f5938eee4d8b9"  # 从上次运行的输出中获取
        logger.error(f"读取模板ID时出错: {e}，使用默认ID: {template_id}")

    # 示例数据，根据模板中的元素ID设置
    elements_data = {
        "slide_0": {  # 假设是第一个幻灯片
            "shape_1": {  # 标题文本框
                "content": "这是自动生成的演示标题",
                "style": {
                    "text": {
                        "size": 32,
                        "color": "#FF0000",  # 红色
                        "bold": True
                    }
                }
            },
            "shape_2": {  # 副标题文本框
                "content": "这是自动生成的副标题文本",
                "style": {
                    "text": {
                        "size": 24,
                        "color": "#0000FF",  # 蓝色
                        "italic": True
                    }
                }
            }
        }
    }
    
    # 保存当前使用的模板ID
    with open("last_template_id.txt", "w") as f:
        f.write(template_id)
    
    # 生成PPT
    success = generate_ppt(template_id, elements_data)
    
    if success:
        logger.info("PPT生成成功!")
    else:
        logger.error("PPT生成失败!")

if __name__ == "__main__":
    main() 