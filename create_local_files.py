import os
import json
import math

# ==========================================
# 🎨 基础配置
# ==========================================
COLOR_CYAN = [0, 0.949, 1, 1]  # #00F2FF
COLOR_GREEN = [0, 1, 0.533, 1] # #00FF88
SIZE = 512
CENTER = SIZE / 2
DURATION = 120

def create_base(name):
    return {"v": "5.7.4", "fr": 60, "ip": 0, "op": DURATION, "w": SIZE, "h": SIZE, "nm": name, "ddd": 0, "assets": [], "layers": []}

def get_rect_shape(w, h, color):
    return [{"ty": "rc", "d": 1, "s": {"a": 0, "k": [w, h]}, "p": {"a": 0, "k": [0, 0]}, "r": {"a": 0, "k": 0}, "nm": "Rect", "hd": False},
            {"ty": "fl", "c": {"a": 0, "k": color}, "o": {"a": 0, "k": 100}, "nm": "Fill", "hd": False}]

def get_circle_shape(s, color):
    return [{"ty": "el", "d": 1, "s": {"a": 0, "k": [s, s]}, "p": {"a": 0, "k": [0, 0]}, "nm": "Circle", "hd": False},
            {"ty": "fl", "c": {"a": 0, "k": color}, "o": {"a": 0, "k": 100}, "nm": "Fill", "hd": False}]

def create_layer(name, shapes, scale=100, pos=[CENTER, CENTER]):
    return {"ddd": 0, "ind": 1, "ty": 4, "nm": name, "sr": 1, "ks": {"o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0}, "p": {"a": 0, "k": [*pos, 0]}, "a": {"a": 0, "k": [0, 0, 0]}, "s": {"a": 0, "k": [scale, scale, 100]}}, "ao": 0, "shapes": shapes, "ip": 0, "op": DURATION, "st": 0, "bm": 0}

# ==========================================
# 🎬 不同的动画逻辑
# ==========================================

def anim_robot():
    """生成机器人：一个方形头部 + 闪烁眼睛"""
    lottie = create_base("Robot")
    # 头
    head = create_layer("Head", get_rect_shape(200, 180, COLOR_CYAN))
    # 眼睛 (左右移动)
    eye_shapes = get_circle_shape(40, COLOR_GREEN)
    eye = create_layer("Eye", eye_shapes)
    eye["ks"]["p"]["k"] = [{"t": 0, "s": [CENTER-50, CENTER, 0]}, {"t": 60, "s": [CENTER+50, CENTER, 0]}, {"t": 120, "s": [CENTER-50, CENTER, 0]}] # 左右扫视
    lottie["layers"] = [eye, head]
    return lottie

def anim_files():
    """生成文件：一个上下浮动的文档"""
    lottie = create_base("Files")
    doc = create_layer("Doc", get_rect_shape(180, 240, COLOR_GREEN))
    # 上下浮动
    doc["ks"]["p"]["k"] = [{"t": 0, "s": [CENTER, CENTER, 0]}, {"t": 60, "s": [CENTER, CENTER-30, 0]}, {"t": 120, "s": [CENTER, CENTER, 0]}]
    lottie["layers"] = [doc]
    return lottie

def anim_success():
    """生成成功：一个放大的圆"""
    lottie = create_base("Success")
    circle = create_layer("Check", get_circle_shape(200, COLOR_GREEN))
    circle["ks"]["s"]["k"] = [{"t": 0, "s": [0, 0, 100]}, {"t": 100, "s": [100, 100, 100]}] # 放大
    lottie["layers"] = [circle]
    return lottie

def anim_empty():
    """生成空状态：一个呼吸的线框"""
    lottie = create_base("Empty")
    box = create_layer("Box", get_rect_shape(200, 200, [0.5, 0.5, 0.5, 1]))
    box["ks"]["o"]["k"] = [{"t": 0, "s": [30]}, {"t": 60, "s": [80]}, {"t": 120, "s": [30]}]
    lottie["layers"] = [box]
    return lottie

# ==========================================
# 🚀 执行生成
# ==========================================
if not os.path.exists("assets"): os.makedirs("assets")

# 字典映射：文件名 -> 生成函数
tasks = {
    "robot.json": anim_robot,
    "files.json": anim_files,
    "success.json": anim_success,
    "empty.json": anim_empty,
    # welcome.json 不需要了，因为我们要用新的粒子特效替代它
    "welcome.json": anim_robot # 暂时用 robot 顶替，反正会被覆盖
}

print("🎨 正在生成多样的矢量动画...")
for filename, func in tasks.items():
    with open(f"assets/{filename}", "w") as f:
        json.dump(func(), f)
    print(f"✅ Generated: {filename}")

