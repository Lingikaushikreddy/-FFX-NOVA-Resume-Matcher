import { useEffect, useRef } from 'react';

/**
 * AtmosphereParticles
 * 
 * A high-performance 2D Canvas particle system for cinematic backgrounds.
 * Features:
 * - Floating dust/data particles
 * - Mouse interaction (repulsion)
 * - Parallax depth simulation via varied speeds
 */
export function AtmosphereParticles() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const mouseRef = useRef({ x: 0, y: 0 });

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;
        let particles: Particle[] = [];

        // Configuration
        const PARTICLE_COUNT = 60;
        const CONNECTION_DISTANCE = 150;
        const MOUSE_RADIUS = 200;

        class Particle {
            x: number;
            y: number;
            vx: number;
            vy: number;
            size: number;
            color: string;
            baseX: number;
            baseY: number;

            constructor(w: number, h: number) {
                this.x = Math.random() * w;
                this.y = Math.random() * h;
                this.baseX = this.x;
                this.baseY = this.y;

                // Cinematic slow drift
                this.vx = (Math.random() - 0.5) * 0.3;
                this.vy = (Math.random() - 0.5) * 0.3;

                this.size = Math.random() * 2 + 0.5;

                // Brand colors: Primary (Blue) and Secondary (Purple)
                const isPrimary = Math.random() > 0.5;
                this.color = isPrimary
                    ? `rgba(59, 130, 246, ${Math.random() * 0.3 + 0.1})` // primary-500
                    : `rgba(124, 58, 237, ${Math.random() * 0.3 + 0.1})`; // secondary-600
            }

            update(w: number, h: number, mouseX: number, mouseY: number) {
                // Movement
                this.x += this.vx;
                this.y += this.vy;

                // Mouse interaction (gentle repulsion)
                const dx = mouseX - this.x;
                const dy = mouseY - this.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < MOUSE_RADIUS) {
                    const forceDirectionX = dx / distance;
                    const forceDirectionY = dy / distance;
                    const force = (MOUSE_RADIUS - distance) / MOUSE_RADIUS;
                    const directionX = forceDirectionX * force * 2; // Repulsion strength
                    const directionY = forceDirectionY * force * 2;

                    this.x -= directionX;
                    this.y -= directionY;
                }

                // Wrap around screen
                if (this.x < 0) this.x = w;
                if (this.x > w) this.x = 0;
                if (this.y < 0) this.y = h;
                if (this.y > h) this.y = 0;
            }

            draw(context: CanvasRenderingContext2D) {
                context.beginPath();
                context.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                context.fillStyle = this.color;
                context.fill();
            }
        }

        const init = () => {
            particles = [];
            for (let i = 0; i < PARTICLE_COUNT; i++) {
                particles.push(new Particle(canvas.width, canvas.height));
            }
        };

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            particles.forEach(particle => {
                particle.update(
                    canvas.width,
                    canvas.height,
                    mouseRef.current.x || -1000,
                    mouseRef.current.y || -1000
                );
                particle.draw(ctx);
            });

            // Draw subtle connections
            particles.forEach((a, index) => {
                for (let j = index + 1; j < particles.length; j++) {
                    const b = particles[j];
                    const dx = a.x - b.x;
                    const dy = a.y - b.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    if (distance < CONNECTION_DISTANCE) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(148, 163, 184, ${0.05 * (1 - distance / CONNECTION_DISTANCE)})`;
                        ctx.lineWidth = 1;
                        ctx.moveTo(a.x, a.y);
                        ctx.lineTo(b.x, b.y);
                        ctx.stroke();
                    }
                }
            });

            animationFrameId = requestAnimationFrame(animate);
        };

        // Resize handler
        const handleResize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            init();
        };

        // Mouse handler
        const handleMouseMove = (e: MouseEvent) => {
            // Get mouse pos relative to canvas if needed, but here window is fine for full screen
            const rect = canvas.getBoundingClientRect();
            mouseRef.current = {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            };
        };

        window.addEventListener('resize', handleResize);
        window.addEventListener('mousemove', handleMouseMove);

        handleResize(); // Initial setup
        animate();

        return () => {
            window.removeEventListener('resize', handleResize);
            window.removeEventListener('mousemove', handleMouseMove);
            cancelAnimationFrame(animationFrameId);
        };
    }, []);

    return (
        <canvas
            ref={canvasRef}
            className="absolute inset-0 w-full h-full pointer-events-none z-0"
        />
    );
}
