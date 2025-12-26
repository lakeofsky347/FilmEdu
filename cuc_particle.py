import streamlit.components.v1 as components

def cuc_particle_effect():
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body { margin: 0; overflow: hidden; background-color: transparent; }
            canvas { display: block; }
        </style>
    </head>
    <body>
        <canvas id="canvas1"></canvas>
        <script>
            const canvas = document.getElementById('canvas1');
            const ctx = canvas.getContext('2d');
            
            // 适配 Streamlit 容器宽度，高度增加以容纳更多内容
            canvas.width = window.innerWidth;
            canvas.height = 600; 

            let particleArray = [];
            let currentText = "CUC"; // 当前状态
            
            // 鼠标配置
            const mouse = { x: null, y: null, radius: 30 }; // 斥力范围稍微调大一点点以配合大字体

            window.addEventListener('mousemove', function(event){
                mouse.x = event.x;
                mouse.y = event.y;
            });
            window.addEventListener('mouseout', function(){
                mouse.x = undefined;
                mouse.y = undefined;
            });

            // 双击切换状态
            window.addEventListener('dblclick', function(){
                if (currentText === "CUC") {
                    currentText = "DSIM";
                    // 重新扫描并重新分配目标点
                    init("CUC", "DSIM"); 
                } else {
                    currentText = "CUC";
                    init("CUC", "");
                }
            });

            class Particle {
                constructor(x, y){
                    this.x = Math.random() * canvas.width; // 初始随机位置，产生聚拢效果
                    this.y = Math.random() * canvas.height;
                    this.size = 2.2; // 粒子稍大，更有质感
                    
                    // 目标位置 (Target Position)
                    this.targetX = x;
                    this.targetY = y;
                    
                    this.density = (Math.random() * 20) + 1; 
                    
                    // 核心颜色：青色区间 (170-190)
                    this.baseHue = Math.random() * 20 + 170;
                    
                    // 微动参数 (Swarm Noise)
                    this.angle = Math.random() * Math.PI * 2;
                    this.velocity = Math.random() * 0.5 + 0.2;
                }
                
                draw(){
                    // 呼吸变色
                    const time = Date.now() * 0.001;
                    const opacity = 0.6 + Math.sin(time + this.density) * 0.4;
                    ctx.fillStyle = `hsla(${this.baseHue}, 80%, 60%, ${opacity})`;
                    
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.closePath();
                    ctx.fill();
                }
                
                update(){
                    // 1. 计算鼠标斥力
                    let dx = mouse.x - this.x;
                    let dy = mouse.y - this.y;
                    let distance = Math.sqrt(dx * dx + dy * dy);
                    let forceDirectionX = dx / distance;
                    let forceDirectionY = dy / distance;
                    
                    let maxDistance = mouse.radius;
                    let force = (maxDistance - distance) / maxDistance;
                    let directionX = forceDirectionX * force * this.density;
                    let directionY = forceDirectionY * force * this.density;

                    // 2. 计算回归目标的力 (Home Force)
                    // 引入微动：目标点不是固定的，是在原定目标点周围做微小的圆周运动
                    this.angle += 0.02; // 角速度
                    let swarmX = this.targetX + Math.cos(this.angle + this.density) * 3; // 3px 的微动范围
                    let swarmY = this.targetY + Math.sin(this.angle + this.density) * 3;

                    let homeDx = this.x - swarmX;
                    let homeDy = this.y - swarmY;

                    if (distance < mouse.radius){
                        // 受到斥力：推开
                        this.x -= directionX * 2; 
                        this.y -= directionY * 2;
                    } else {
                        // 3. 高粘滞流体模拟 (Fluid Simulation)
                        // 不直接设置位置，而是通过极小的比例逼近目标 (Zeno's Paradox)
                        // 分母越大，液体越稠，运动越迟滞优雅
                        if (this.x !== swarmX){
                            this.x -= homeDx / 35; // 阻尼系数 35，非常粘稠
                        }
                        if (this.y !== swarmY){
                            this.y -= homeDy / 35;
                        }
                    }
                }
                
                // 更新目标点 (用于变形)
                changeTarget(x, y) {
                    this.targetX = x;
                    this.targetY = y;
                }
            }

            // 核心逻辑：获取文字坐标数据
            function scanText(text1, text2) {
                ctx.clearRect(0,0, canvas.width, canvas.height);
                
                ctx.fillStyle = 'white';
                ctx.font = '900 220px Verdana'; // 巨型字体
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                
                // 绘制第一行 CUC
                ctx.fillText('CUC', canvas.width/2, canvas.height/2 - (text2 ? 80 : 0));
                
                // 如果有第二行 DSIM
                if (text2) {
                    ctx.font = '900 120px Verdana';
                    ctx.fillText('DSIM', canvas.width/2, canvas.height/2 + 100);
                }
                
                const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
                ctx.clearRect(0,0, canvas.width, canvas.height); // 扫完清空，留给粒子画
                
                let coordinates = [];
                const gap = 4; // 采样密度
                
                for (let y = 0; y < canvas.height; y += gap){
                    for (let x = 0; x < canvas.width; x += gap){
                        if (data.data[(y * 4 * canvas.width) + (x * 4) + 3] > 128){
                            coordinates.push({x: x, y: y});
                        }
                    }
                }
                return coordinates;
            }

            function init(text1, text2){
                const coords = scanText(text1, text2);
                
                // 智能分配策略：
                // 如果现有粒子不够，创建新的；如果多了，删除多余的（或者隐藏）
                // 这里为了变形平滑，我们尽量复用现有粒子
                
                if (particleArray.length === 0) {
                    // 第一次初始化
                    for (let i = 0; i < coords.length; i++){
                        particleArray.push(new Particle(coords[i].x, coords[i].y));
                    }
                } else {
                    // 变形逻辑 (Morphing)
                    // 1. 调整现有粒子目标
                    let i = 0;
                    for (; i < coords.length && i < particleArray.length; i++) {
                        particleArray[i].changeTarget(coords[i].x, coords[i].y);
                    }
                    
                    // 2. 如果新文字粒子更多，补充粒子
                    if (coords.length > particleArray.length) {
                        for (; i < coords.length; i++) {
                            particleArray.push(new Particle(coords[i].x, coords[i].y));
                        }
                    } 
                    // 3. 如果新文字粒子更少，多余的粒子让它飞走或透明 (这里简化为飞出屏幕)
                    else if (coords.length < particleArray.length) {
                        for (; i < particleArray.length; i++) {
                            particleArray[i].changeTarget(Math.random() * canvas.width, Math.random() * canvas.height); // 散开
                        }
                        // 截断数组以优化性能
                        particleArray.splice(coords.length);
                    }
                }
            }

            function animate(){
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let i = 0; i < particleArray.length; i++){
                    particleArray[i].draw();
                    particleArray[i].update();
                }
                requestAnimationFrame(animate);
            }

            // 启动
            init("CUC", ""); 
            animate();
            
            window.addEventListener('resize', function(){
                canvas.width = window.innerWidth;
                canvas.height = 600;
                // 重置当前状态
                if(currentText === "CUC") init("CUC", "");
                else init("CUC", "DSIM");
            });
        </script>
    </body>
    </html>
    """
    # 增加高度以适应双行文字
    components.html(html_code, height=600, scrolling=False)