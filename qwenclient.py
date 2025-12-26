from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import dashscope
from dashscope import ImageSynthesis
import os
import tempfile

# 确保使用北京节点的 URL
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def generate_image_sync(api_key: str, prompt: str, size: str = "1328*1328") -> dict:
    """
    同步调用通义万相生成图片
    安全说明：API Key 由外部传入，本文件不存储密钥
    """
    # 1. 检查 Key 是否存在 (防止空值传入报错)
    if not api_key:
        return {"success": False, "message": "Qwen API Key 未配置，请检查 Secrets 设置"}
        
    # 2. 设置本次调用的 Key
    dashscope.api_key = api_key
    
    print(f'---- [Qwen] 正在请求生图: {prompt[:20]}... (Size: {size}) ----')
    
    try:
        # 3. 发起调用
        rsp = ImageSynthesis.call(
            model="qwen-image-plus",
            prompt=prompt,
            n=1,
            size=size,
            prompt_extend=True,
            watermark=False
        )
        
        # 4. 处理结果
        if rsp.status_code == HTTPStatus.OK:
            # 双重检查返回结果的完整性
            if not hasattr(rsp, 'output') or not rsp.output or \
               not hasattr(rsp.output, 'results') or not rsp.output.results:
                   fail_msg = getattr(rsp.output, 'message', '未知错误')
                   print(f"⚠️ 生成失败: {fail_msg}")
                   return {"success": False, "message": f"生成失败: {fail_msg}"}

            paths = []
            for result in rsp.output.results:
                # 解析文件名
                file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                # 保存到系统临时目录 (适合 Streamlit Cloud)
                save_path = os.path.join(tempfile.gettempdir(), file_name)
                
                with open(save_path, 'wb+') as f:
                    f.write(requests.get(result.url).content)
                
                paths.append(save_path)
                print(f'---- [Qwen] 图片已保存: {save_path} ----')
            
            return {"success": True, "paths": paths}
        else:
            error_msg = f'API Error: {rsp.code} - {rsp.message}'
            print(error_msg)
            return {"success": False, "message": error_msg}

    except Exception as e:
        error_msg = f"Qwen Client Exception: {str(e)}"
        print(error_msg)
        return {"success": False, "message": error_msg}

if __name__ == "__main__":
    # 这里的测试代码不包含 Key，提示用户去主程序运行
    print("请在 web_app.py 中运行以测试完整功能")