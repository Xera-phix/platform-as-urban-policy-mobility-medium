import { motion } from 'framer-motion';

export default function AnimatedDataPoints() {
  // Generate random positions for floating data points
  const dataPoints = Array.from({ length: 15 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    delay: Math.random() * 2,
    duration: 3 + Math.random() * 2,
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {dataPoints.map((point) => (
        <motion.div
          key={point.id}
          className="absolute w-1 h-1 bg-primary/20 rounded-full"
          style={{
            left: `${point.x}%`,
            top: `${point.y}%`,
          }}
          animate={{
            y: [0, -30, 0],
            opacity: [0, 1, 0],
            scale: [0.5, 1, 0.5],
          }}
          transition={{
            duration: point.duration,
            repeat: Infinity,
            delay: point.delay,
            ease: "easeInOut",
          }}
        />
      ))}
    </div>
  );
}
