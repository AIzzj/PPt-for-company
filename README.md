# PPT JSON Transforms

一个强大的PPT模板解析和生成系统，可以动态生成PowerPoint演示文稿。

## 功能特点

- **模板上传**：上传PowerPoint模板文件
- **模板解析**：解析PPT模板，提取幻灯片、元素和样式信息
- **内容生成**：为幻灯片元素生成内容，如标题、副标题等
- **PPT生成**：使用模板和内容生成新的PPT文件
- **结果下载**：下载生成的PPT文件

## 系统架构

系统由以下模块组成：

- **模板解析器**：负责解析上传的PPT模板文件
- **PPT生成器**：负责将模板和内容组合成最终的PPT文件
- **内容生成器**：负责生成幻灯片内容
- **API服务**：提供REST API接口，供前端和其他应用调用

## 使用方法

### 1. 上传模板

```bash
# 上传一个PPT模板文件
curl -X POST -F "file=@template.pptx" http://127.0.0.1:8000/template/upload
```

响应示例：

```json
{
  "template_id": "42438a4fe845420bb98f5938eee4d8b9",
  "name": "42438a4fe845420bb98f5938eee4d8b9",
  "slide_count": 1,
  "slides": [
    {
      "slide_id": "slide_0",
      "slide_type": "title",
      "elements": [
        {
          "element_id": "shape_1",
          "element_type": "text",
          "properties": {
            "id": "shape_1",
            "type": "text",
            "position": {
              "x": 0.075,
              "y": 0.3106481481481482,
              "width": 0.85,
              "height": 0.21435185185185185
            },
            "style": {
              "text": {
                "paragraphs": [
                  {
                    "alignment": "None",
                    "runs": [
                      {
                        "text": "测试标题",
                        "style": {
                          "size": null,
                          "bold": null,
                          "italic": null,
                          "underline": null,
                          "font_name": null
                        }
                      }
                    ]
                  }
                ]
              }
            }
          },
          "content": "测试标题",
          "is_placeholder": true
        },
        {
          "element_id": "shape_2",
          "element_type": "text",
          "properties": {
            "id": "shape_2",
            "type": "text",
            "position": {
              "x": 0.075,
              "y": 0.5555555555555556,
              "width": 0.85,
              "height": 0.13425925925925927
            },
            "style": {
              "text": {
                "paragraphs": [
                  {
                    "alignment": "None",
                    "runs": [
                      {
                        "text": "测试副标题",
                        "style": {
                          "size": null,
                          "bold": null,
                          "italic": null,
                          "underline": null,
                          "font_name": null
                        }
                      }
                    ]
                  }
                ]
              }
            }
          },
          "content": "测试副标题",
          "is_placeholder": true
        }
      ]
    }
  ]
}
```

### 2. 生成PPT

```bash
# 使用模板生成PPT
curl -X POST -H "Content-Type: application/json" -d '{
  "template_id": "42438a4fe845420bb98f5938eee4d8b9",
  "content_mappings": [
    {
      "request_id": "48d6a2dd-f113-4ba7-91bf-407153277d1b",
      "slide_id": "slide_0",
      "element_id": "shape_1",
      "content": "这是自动生成的演示标题",
      "content_type": "title",
      "metadata": {
        "style": {
          "text": {
            "size": 32,
            "color": "#FF0000",
            "bold": true
          }
        }
      }
    },
    {
      "request_id": "de66107e-edfa-46ff-aa59-96cc6d0206f8",
      "slide_id": "slide_0",
      "element_id": "shape_2",
      "content": "这是自动生成的副标题文本",
      "content_type": "subtitle",
      "metadata": {
        "style": {
          "text": {
            "size": 24,
            "color": "#0000FF",
            "italic": true
          }
        }
      }
    }
  ]
}' http://127.0.0.1:8000/ppt/generate
```

响应示例：

```json
{
  "task_id": "ca3db434-9401-4a58-8421-0995099abaf5",
  "status": "pending",
  "output_path": null,
  "download_url": "/ppt/download/ca3db434-9401-4a58-8421-0995099abaf5"
}
```

### 3. 检查生成状态

```bash
# 检查PPT生成任务状态
curl -X GET http://127.0.0.1:8000/ppt/status/ca3db434-9401-4a58-8421-0995099abaf5
```

响应示例：

```json
{
  "task_id": "ca3db434-9401-4a58-8421-0995099abaf5",
  "status": "completed",
  "output_path": "outputs\\ca3db434-9401-4a58-8421-0995099abaf5.pptx",
  "download_url": "/ppt/download/ca3db434-9401-4a58-8421-0995099abaf5"
}
```

### 4. 下载生成的PPT

```bash
# 下载生成的PPT文件
curl -X GET -o generated.pptx http://127.0.0.1:8000/ppt/download/ca3db434-9401-4a58-8421-0995099abaf5
```

## 调试工具

系统提供了几个调试脚本：

- `debug_parser.py`: 测试模板解析功能
- `debug_upload.py`: 测试模板上传功能
- `debug_generate.py`: 测试PPT生成功能
- `debug_ppt_generator.py`: 直接测试PPT生成器

## 目录结构

- `/backend`: 后端代码
  - `/core`: 核心功能模块
    - `/template_parser`: 模板解析器
    - `/ppt_generator`: PPT生成器
    - `/ai_engine`: 内容生成器
    - `/models`: 数据模型
  - `/api`: API服务
- `/frontend`: 前端代码
- `/templates`: 模板文件目录
- `/uploads`: 上传的模板文件
- `/outputs`: 生成的PPT文件

## 依赖库

- Python 3.8+
- FastAPI
- python-pptx
- python-multipart
- PyMuPDF (fitz)
- Pillow
- uvicorn
- asyncio

## 启动服务

```bash
# 启动API服务
uvicorn backend.api.main:app --reload
```

## 常见问题

### 模板解析失败

可能的原因：
- PPT文件格式不兼容
- 文件损坏
- 文件路径错误

解决方案：
- 确保使用兼容的PowerPoint格式（.pptx）
- 检查文件是否完整
- 检查文件路径是否正确

### PPT生成超时

可能的原因：
- 模板文件过大
- 服务器资源不足
- 内容映射错误

解决方案：
- 使用更小的模板文件
- 增加服务器资源
- 检查内容映射是否正确

### 下载失败

可能的原因：
- 任务尚未完成
- 任务ID错误
- 文件已被删除

解决方案：
- 等待任务完成
- 检查任务ID是否正确
- 重新生成PPT 