import React, { useEffect, useRef } from 'react';

export interface ConfettiProps {
  durationMs?: number;
  onComplete?: () => void;
}

export const Confetti: React.FC<ConfettiProps> = ({ durationMs = 3500, onComplete }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const colors = ['#0066FF', '#00D2FF', '#10B981', '#F59E0B', '#A855F7', '#EC4899'];
    const particleCount = 80;
    const particles = Array.from({ length: particleCount }).map(() => ({
      x: Math.random() * canvas.width,
      y: Math.random() * -canvas.height * 0.5,
      size: Math.random() * 6 + 4,
      color: colors[Math.floor(Math.random() * colors.length)]!,
      speedX: Math.random() * 4 - 2,
      speedY: Math.random() * 3 + 2,
      rotation: Math.random() * 360,
      rotationSpeed: Math.random() * 4 - 2,
      opacity: 1,
    }));

    let animationFrameId: number;
    const startTime = Date.now();

    const render = () => {
      const elapsed = Date.now() - startTime;
      if (elapsed > durationMs) {
        onComplete?.();
        return;
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach((p) => {
        p.x += p.speedX;
        p.y += p.speedY;
        p.rotation += p.rotationSpeed;
        p.opacity = Math.max(0, 1 - elapsed / durationMs);

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate((p.rotation * Math.PI) / 180);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.opacity;
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
        ctx.restore();
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [durationMs, onComplete]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-50 w-full h-full"
    />
  );
};
