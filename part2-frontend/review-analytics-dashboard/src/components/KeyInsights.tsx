import { motion } from 'framer-motion';
import { Lightbulb, TrendingDown, TrendingUp, Award } from 'lucide-react';

export default function KeyInsights() {
  const insights = [
    {
      icon: <TrendingDown size={20} strokeWidth={1.5} />,
      title: 'Construction Impact',
      highlight: '-2.5%',
      delay: 0.1
    },
    {
      icon: <TrendingUp size={20} strokeWidth={1.5} />,
      title: 'Post-Renovation',
      highlight: '+10.2%',
      delay: 0.2
    },
    {
      icon: <Award size={20} strokeWidth={1.5} />,
      title: 'Overall Gain',
      highlight: '7.4%',
      delay: 0.3
    },
    {
      icon: <Lightbulb size={20} strokeWidth={1.5} />,
      title: 'Reviews Analyzed',
      highlight: '620+',
      delay: 0.4
    }
  ];

  return (
    <div className="w-full max-w-6xl mx-auto mb-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="text-center mb-8"
      >
        <h2 className="text-3xl font-bold text-foreground tracking-tight">
          Key Findings
        </h2>
      </motion.div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {insights.map((insight, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.5, delay: insight.delay }}
            whileHover={{ y: -4 }}
            className="group text-center p-6 bg-background border border-border hover:border-primary/30 transition-all"
          >
            <div className="inline-flex p-2 bg-primary/5 mb-3 group-hover:bg-primary/10 transition-colors">
              <div className="text-primary">
                {insight.icon}
              </div>
            </div>
            
            <div className="text-3xl font-bold text-foreground mb-1 tracking-tight">
              {insight.highlight}
            </div>
            
            <div className="text-xs text-foreground/50 font-light tracking-wide uppercase">
              {insight.title}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
