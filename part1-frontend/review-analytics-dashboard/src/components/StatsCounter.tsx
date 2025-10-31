import { motion, useMotionValue, useTransform, animate } from 'framer-motion';
import { useEffect, useRef } from 'react';
import { TrendingUp, TrendingDown, ThumbsUp, AlertTriangle } from 'lucide-react';

interface StatProps {
  end: number;
  duration?: number;
  suffix?: string;
  prefix?: string;
  decimals?: number;
  label: string;
  icon: React.ReactNode;
  trend?: 'up' | 'down';
  trendValue?: string;
}

function AnimatedCounter({ end, duration = 2, suffix = '', prefix = '', decimals = 0, label, icon, trend, trendValue }: StatProps) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => {
    return prefix + latest.toFixed(decimals) + suffix;
  });
  const nodeRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    const controls = animate(count, end, { duration });
    return controls.stop;
  }, [count, end, duration]);

  useEffect(() => {
    const unsubscribe = rounded.on('change', (latest) => {
      if (nodeRef.current) {
        nodeRef.current.textContent = latest;
      }
    });
    return () => unsubscribe();
  }, [rounded]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -8, scale: 1.02 }}
      className="relative group"
    >
      <div className="bg-gradient-to-br from-background via-muted/50 to-background border border-border p-6 overflow-hidden hover:border-primary/50 transition-all duration-300">
        {/* Glow effect on hover */}
        <div className="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-3">
            <div className="text-primary/70 group-hover:text-primary transition-colors">
              {icon}
            </div>
            {trend && trendValue && (
              <div className={`flex items-center gap-1 text-xs font-medium ${
                trend === 'up' ? 'text-accent' : 'text-red-400'
              }`}>
                {trend === 'up' ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
                {trendValue}
              </div>
            )}
          </div>
          
          <div className="text-4xl font-bold text-foreground mb-2 tracking-tight">
            <span ref={nodeRef}>0</span>
          </div>
          
          <div className="text-sm text-foreground/50 font-light tracking-wide uppercase">
            {label}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default function StatsCounter() {
  const stats = [
    {
      end: 3.63,
      decimals: 2,
      label: 'Pre-Construction Rating',
      icon: <ThumbsUp size={24} strokeWidth={1.5} />,
      trend: 'up' as const,
      trendValue: 'Baseline'
    },
    {
      end: 3.54,
      decimals: 2,
      label: 'During Construction',
      icon: <AlertTriangle size={24} strokeWidth={1.5} />,
      trend: 'down' as const,
      trendValue: '-2.5%'
    },
    {
      end: 3.90,
      decimals: 2,
      label: 'Post-Construction',
      icon: <TrendingUp size={24} strokeWidth={1.5} />,
      trend: 'up' as const,
      trendValue: '+10.2%'
    },
    {
      end: 7.4,
      decimals: 1,
      suffix: '%',
      label: 'Overall Improvement',
      icon: <TrendingUp size={24} strokeWidth={1.5} />,
      trend: 'up' as const,
      trendValue: 'vs. Construction'
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
      className="w-full max-w-6xl mx-auto mb-16"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <AnimatedCounter {...stat} />
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
