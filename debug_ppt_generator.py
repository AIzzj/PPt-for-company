import os
import logging
import uuid
from datetime import datetime
from backend.core.template_parser import TemplateParser
from backend.core.ppt_generator import PPTGenerator, PPTGenerationTask, PPTContentMapping
from backend.core.ai_engine import ContentResponse
from backend.core.ai_engine.content_generator import ContentType

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_ppt_generator():
    """测试PPT生成器"""
    # 创建测试PPT文件
    test_file = "test_template.pptx"
    parser = TemplateParser(test_file)
    template = parser.parse()
    
    if not template:
        logger.error(f"无法解析模板文件: {test_file}")
        return
    
    logger.info(f"成功解析模板，模板ID: {template.template_id}, 幻灯片数量: {len(template.slides)}")
    
    # 创建PPT生成器
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    ppt_generator = PPTGenerator(output_dir)
    
    # 创建内容映射
    content_mappings = []
    
    if len(template.slides) > 0:
        slide = template.slides[0]
        logger.info(f"第一张幻灯片ID: {slide.slide_id}, 类型: {slide.slide_type}, 元素数量: {len(slide.elements)}")
        
        if len(slide.elements) > 0:
            for idx, element in enumerate(slide.elements):
                logger.info(f"元素 {idx}: ID={element.element_id}, 类型={element.element_type}")
                
                # 根据元素类型确定内容类型
                content_type = ContentType.TITLE if idx == 0 else ContentType.SUBTITLE
                content = "测试标题" if idx == 0 else "测试副标题"
                
                # 创建内容响应
                content_response = ContentResponse(
                    request_id=str(uuid.uuid4()),
                    content=content,
                    content_type=content_type,
                    metadata={}
                )
                
                # 创建内容映射
                content_mapping = PPTContentMapping(
                    template_id=template.template_id,
                    slide_id=slide.slide_id,
                    element_id=element.element_id,
                    content_response=content_response
                )
                
                content_mappings.append(content_mapping)
    
    if not content_mappings:
        logger.error("没有内容映射")
        return
    
    # 创建生成任务
    task_id = str(uuid.uuid4())
    logger.info(f"创建生成任务，任务ID: {task_id}")
    
    task = ppt_generator.create_task(
        template=template,
        content_mappings=content_mappings,
        task_id=task_id
    )
    
    # 生成PPT
    try:
        output_path = ppt_generator.generate(task)
        logger.info(f"PPT生成成功，路径: {output_path}")
        
        # 检查生成的文件是否存在
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"生成的PPT文件大小: {file_size} 字节")
        else:
            logger.error(f"未找到生成的文件: {output_path}")
    except Exception as e:
        logger.error(f"生成PPT时出错: {e}", exc_info=True)

if __name__ == "__main__":
    test_ppt_generator() 