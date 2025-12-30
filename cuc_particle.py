import streamlit.components.v1 as components

def cuc_particle_effect():
    """
    渲染自适应双模粒子特效 (Adaptive Dual-Mode)
    Dark: 赛博朋克发光青色
    Light: 工业设计深蓝墨点
    """
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
            let appState = 0;
            
            // 🎨 主题检测与配色配置
            let isLightMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
            
            // 监听系统主题变化
            window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', event => {
                isLightMode = event.matches;
                // 切换主题时重新初始化粒子颜色
                init("CUC", appState === 2 ? "DSIM" : "");
            });

            // 颜色配置函数
            function getThemeConfig() {
                if (isLightMode) {
                    return {
                        textBase: 'rgba(0, 0, 0, 1)', // 扫描文字：纯黑
                        particleHue: 215, // 工业蓝 (Hue 215)
                        saturation: '80%',
                        lightness: '40%', // 深色点
                        bgComposite: 'source-over', // 正常叠加
                        shadowBlur: 0 // 无光晕，实体感
                    };
                } else {
                    return {
                        textBase: 'white', // 扫描文字：白
                        particleHue: 180, // 赛博青 (Hue 180)
                        saturation: '100%',
                        lightness: '60%', // 亮色点
                        bgComposite: 'lighter', // 发光叠加
                        shadowBlur: 15 // 强光晕
                    };
                }
            }

            const mouse = { x: null, y: null, radius: 100 };
            window.addEventListener('mousemove', function(event){ mouse.x = event.x; mouse.y = event.y; });
            window.addEventListener('mouseout', function(){ mouse.x = canvas.width*0.8; mouse.y = canvas.height*0.5; });
            window.addEventListener('dblclick', function(){
                if (appState === 0) { appState = 1; init("CUC", ""); } 
                else if (appState === 1) { appState = 2; init("CUC", "DSIM"); } 
                else { appState = 1; init("CUC", ""); }
            });

            class Particle {
                constructor(x, y){
                    this.x = Math.random() * (canvas.width * 0.5) + (canvas.width * 0.5);
                    this.y = Math.random() * canvas.height;
                    this.vx = (Math.random() - 0.5) * 2;
                    this.vy = (Math.random() - 0.5) * 2;
                    this.targetX = x;
                    this.targetY = y;
                    this.size = Math.random() * 2 + 1.5; 
                    // 随机微调颜色
                    this.hueVariance = Math.random() * 20 - 10;
                    this.angle = Math.random() * Math.PI * 2;
                }
                
                draw(config){
                    // 动态获取颜色
                    const time = Date.now() * 0.002;
                    const opacity = 0.6 + Math.sin(time + this.x) * 0.4;
                    const finalHue = config.particleHue + this.hueVariance;
                    
                    ctx.fillStyle = `hsla(${finalHue}, ${config.saturation}, ${config.lightness}, ${opacity})`;
                    
                    // 光晕处理
                    ctx.shadowBlur = config.shadowBlur;
                    ctx.shadowColor = ctx.fillStyle;

                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.closePath();
                    ctx.fill();
                    
                    // 重置 shadow 避免影响性能
                    ctx.shadowBlur = 0;
                }
                
                update(){
                    if (appState === 0) {
                        let targetX = mouse.x || canvas.width * 0.8;
                        let targetY = mouse.y || canvas.height * 0.5;
                        let dx = targetX - this.x;
                        let dy = targetY - this.y;
                        let forceX = dx * 0.002; 
                        let forceY = dy * 0.002;
                        this.angle += 0.05;
                        this.vx += forceX + Math.cos(this.angle)*0.2;
                        this.vy += forceY + Math.sin(this.angle)*0.2;
                        this.vx *= 0.95; this.vy *= 0.95;
                        this.x += this.vx; this.y += this.vy;
                        return;
                    }
                    let dx = mouse.x - this.x;
                    let dy = mouse.y - this.y;
                    let distance = Math.sqrt(dx * dx + dy * dy);
                    let repulseRadius = 60;
                    if (distance < repulseRadius){
                        const force = (repulseRadius - distance) / repulseRadius;
                        this.vx -= (dx/distance) * force * 2; 
                        this.vy -= (dy/distance) * force * 2;
                    }
                    let floatX = Math.cos(Date.now()*0.001 + this.y*0.05) * 2;
                    let floatY = Math.sin(Date.now()*0.001 + this.x*0.05) * 2;
                    let homeDx = (this.targetX + floatX) - this.x;
                    let homeDy = (this.targetY + floatY) - this.y;
                    this.vx += homeDx * 0.05;
                    this.vy += homeDy * 0.05;
                    this.vx *= 0.80; this.vy *= 0.80;
                    this.x += this.vx; this.y += this.vy;
                }
                changeTarget(x, y) { this.targetX = x; this.targetY = y; }
            }

            function scanText(text1, text2, config) {
                ctx.clearRect(0,0, canvas.width, canvas.height);
                ctx.fillStyle = config.textBase; // 使用配置的文字颜色
                ctx.font = '900 200px Verdana'; 
                ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                ctx.fillText('CUC', canvas.width/2, canvas.height/2 - (text2 ? 80 : 0));
                if (text2) {
                    ctx.font = '900 100px Verdana';
                    ctx.fillText('DSIM', canvas.width/2, canvas.height/2 + 110);
                }
                const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
                ctx.clearRect(0,0, canvas.width, canvas.height); 
                let coordinates = [];
                const gap = 7; 
                for (let y = 0; y < canvas.height; y += gap){
                    for (let x = 0; x < canvas.width; x += gap){
                        if (data.data[(y * 4 * canvas.width) + (x * 4) + 3] > 128){
                            let jitter = (Math.random() - 0.5) * 2;
                            coordinates.push({x: x + jitter, y: y + jitter});
                        }
                    }
                }
                return coordinates;
            }

            function init(text1, text2){
                const config = getThemeConfig();
                const coords = scanText(text1, text2, config);
                if (particleArray.length < 800) {
                     for (let i = particleArray.length; i < 800; i++){
                        particleArray.push(new Particle(Math.random()*canvas.width, Math.random()*canvas.height));
                    }
                }
                let i = 0;
                for (; i < coords.length && i < particleArray.length; i++) {
                    particleArray[i].changeTarget(coords[i].x, coords[i].y);
                }
                for (; i < particleArray.length; i++) {
                    particleArray[i].changeTarget(Math.random()*canvas.width, Math.random()*canvas.height);
                }
                if (coords.length > particleArray.length) {
                    for (let j = particleArray.length; j < coords.length; j++) {
                        particleArray.push(new Particle(coords[j].x, coords[j].y));
                    }
                }
            }

            function animate(){
                // 拖尾清除逻辑：
                // 亮色模式：完全清除，保持干净
                // 暗色模式：轻微保留，增加光效
                const config = getThemeConfig();
                ctx.globalCompositeOperation = 'source-over'; // 重置混合模式
                
                if (isLightMode) {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                } else {
                    ctx.fillStyle = 'rgba(14, 17, 23, 0.3)'; // 模拟深色拖尾
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                }

                // 设置混合模式
                // 亮色用 normal，暗色用 lighter (叠加发光)
                // 注意：在 clearRect 后其实不需要 lighter，除非粒子互相重叠
                
                for (let i = 0; i < particleArray.length; i++){
                    particleArray[i].draw(config);
                    particleArray[i].update();
                }
                requestAnimationFrame(animate);
            }

            // 启动
            for(let i=0; i<800; i++) particleArray.push(new Particle(0,0));
            animate();
            
            window.addEventListener('resize', function(){ canvas.width = window.innerWidth; canvas.height = 600; });
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=600, scrolling=False)
