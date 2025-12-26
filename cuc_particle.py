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
            
            canvas.width = window.innerWidth;
            canvas.height = 600; 

            let particleArray = [];
            let appState = 0; // 0:游弋, 1:CUC, 2:CUC+DSIM
            
            // 鼠标配置
            const mouse = { x: null, y: null, radius: 100 };

            window.addEventListener('mousemove', function(event){
                mouse.x = event.x;
                mouse.y = event.y;
            });
            // 鼠标移出时，给一个默认位置（右侧中心），让鱼群不至于停滞
            window.addEventListener('mouseout', function(){
                mouse.x = canvas.width * 0.8;
                mouse.y = canvas.height * 0.5;
            });

            // 双击切换
            window.addEventListener('dblclick', function(){
                if (appState === 0) {
                    appState = 1;
                    init("CUC", "");
                } else if (appState === 1) {
                    appState = 2;
                    init("CUC", "DSIM");
                } else {
                    appState = 1;
                    init("CUC", "");
                }
            });

            class Particle {
                constructor(x, y){
                    // 初始位置限制在右侧海域
                    this.x = Math.random() * (canvas.width * 0.5) + (canvas.width * 0.5);
                    this.y = Math.random() * canvas.height;
                    
                    // 物理属性
                    this.vx = (Math.random() - 0.5) * 2;
                    this.vy = (Math.random() - 0.5) * 2;
                    this.friction = 0.9; // 游弋时的低阻力
                    
                    // 目标点
                    this.targetX = x;
                    this.targetY = y;
                    
                    // 外观：松散的大点
                    this.size = Math.random() * 2 + 1.5; 
                    this.baseHue = Math.random() * 30 + 170; // 青色系
                    
                    // 随机参数
                    this.angle = Math.random() * Math.PI * 2;
                }
                
                draw(){
                    // 呼吸闪烁
                    const opacity = 0.4 + Math.sin(Date.now()*0.002 + this.x) * 0.4;
                    ctx.fillStyle = `hsla(${this.baseHue}, 80%, 60%, ${opacity})`;
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.closePath();
                    ctx.fill();
                }
                
                update(){
                    // ==========================================
                    // 🌊 状态 0: 鱼群集结 (Attraction Mode)
                    // ==========================================
                    if (appState === 0) {
                        // 1. 寻找目标：鼠标位置 或 默认右侧中心
                        let targetX = mouse.x || canvas.width * 0.8;
                        let targetY = mouse.y || canvas.height * 0.5;
                        
                        let dx = targetX - this.x;
                        let dy = targetY - this.y;
                        let distance = Math.sqrt(dx*dx + dy*dy);
                        
                        // 2. 引力计算 (距离越远引力越大，但有上限)
                        // 这是一个柔和的牵引力
                        let forceX = dx * 0.002; 
                        let forceY = dy * 0.002;
                        
                        // 3. 随机游动噪音 (Perlin Noise模拟)
                        this.angle += 0.05;
                        let noiseX = Math.cos(this.angle) * 0.2;
                        let noiseY = Math.sin(this.angle) * 0.2;

                        this.vx += forceX + noiseX;
                        this.vy += forceY + noiseY;
                        
                        // 4. 速度限制 (防止飞太快)
                        this.vx *= 0.95; // 水阻力
                        this.vy *= 0.95;
                        
                        this.x += this.vx;
                        this.y += this.vy;
                        return;
                    }

                    // ==========================================
                    // 🧊 状态 1 & 2: 文字结晶 (Repulsion + Viscosity)
                    // ==========================================
                    
                    // 1. 鼠标排斥 (此时鼠标是干扰源)
                    let dx = mouse.x - this.x;
                    let dy = mouse.y - this.y;
                    let distance = Math.sqrt(dx * dx + dy * dy);
                    let repulseRadius = 60; // 较小的排斥范围
                    
                    if (distance < repulseRadius){
                        const forceDirectionX = dx / distance;
                        const forceDirectionY = dy / distance;
                        const force = (repulseRadius - distance) / repulseRadius;
                        
                        // 强推力
                        this.vx -= forceDirectionX * force * 2; 
                        this.vy -= forceDirectionY * force * 2;
                    }

                    // 2. 回归目标的弹力 (Spring Force)
                    // 引入微动：目标点本身在轻微浮动，增加液体感
                    let floatX = Math.cos(Date.now() * 0.001 + this.y * 0.05) * 2;
                    let floatY = Math.sin(Date.now() * 0.001 + this.x * 0.05) * 2;
                    
                    let homeDx = (this.targetX + floatX) - this.x;
                    let homeDy = (this.targetY + floatY) - this.y;
                    
                    // 强回弹，高记忆感
                    this.vx += homeDx * 0.05;
                    this.vy += homeDy * 0.05;

                    // 3. 高粘滞阻尼 (High Viscosity)
                    // 0.8 的摩擦力让运动非常迟滞，像在胶水中
                    this.vx *= 0.80; 
                    this.vy *= 0.80;

                    this.x += this.vx;
                    this.y += this.vy;
                }
                
                changeTarget(x, y) {
                    this.targetX = x;
                    this.targetY = y;
                }
            }

            function scanText(text1, text2) {
                ctx.clearRect(0,0, canvas.width, canvas.height);
                ctx.fillStyle = 'white';
                // 字体稍微减小一点点，留出呼吸空间
                ctx.font = '900 200px Verdana'; 
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                
                // 绘制文字
                ctx.fillText('CUC', canvas.width/2, canvas.height/2 - (text2 ? 80 : 0));
                if (text2) {
                    ctx.font = '900 100px Verdana';
                    ctx.fillText('DSIM', canvas.width/2, canvas.height/2 + 110);
                }
                
                const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
                ctx.clearRect(0,0, canvas.width, canvas.height); 
                
                let coordinates = [];
                // 🔵 关键修改：采样间距 Gap
                // Gap = 6~7 可以实现“松散的点”效果，不必完全填充
                // 既能看清字，又有空隙感
                const gap = 7; 
                
                for (let y = 0; y < canvas.height; y += gap){
                    for (let x = 0; x < canvas.width; x += gap){
                        // 阈值 128
                        if (data.data[(y * 4 * canvas.width) + (x * 4) + 3] > 128){
                            // 加入一点随机偏移，让文字边缘不那么死板
                            let jitter = (Math.random() - 0.5) * 2;
                            coordinates.push({x: x + jitter, y: y + jitter});
                        }
                    }
                }
                return coordinates;
            }

            function init(text1, text2){
                const coords = scanText(text1, text2);
                
                // 初始状态粒子数：控制在 1000 左右，保持稀疏感
                if (particleArray.length < 800) {
                     for (let i = particleArray.length; i < 800; i++){
                        particleArray.push(new Particle(Math.random()*canvas.width, Math.random()*canvas.height));
                    }
                }

                let i = 0;
                // 分配目标
                for (; i < coords.length && i < particleArray.length; i++) {
                    particleArray[i].changeTarget(coords[i].x, coords[i].y);
                }
                
                // 多余粒子处理：让它们在文字周围继续像鱼一样游动，而不是消失
                // 这能增加氛围感
                for (; i < particleArray.length; i++) {
                    // 目标设为随机位置
                    particleArray[i].changeTarget(
                        Math.random() * canvas.width, 
                        Math.random() * canvas.height
                    );
                }
                
                // 如果文字需要的粒子比当前多，补充粒子
                if (coords.length > particleArray.length) {
                    for (let j = particleArray.length; j < coords.length; j++) {
                        particleArray.push(new Particle(coords[j].x, coords[j].y));
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

            // 启动：先生成一批“游鱼”
            for(let i=0; i<800; i++){
                particleArray.push(new Particle(0,0));
            }
            animate();
            
            window.addEventListener('resize', function(){
                canvas.width = window.innerWidth;
                canvas.height = 600;
            });
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=600, scrolling=False)