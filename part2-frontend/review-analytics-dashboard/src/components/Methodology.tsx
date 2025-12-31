import { motion } from 'framer-motion';
import { Database, BarChart3, Brain, FileCheck } from 'lucide-react';

export default function Methodology() {
  const steps = [
    {
      icon: <Database size={32} strokeWidth={1.5} />,
      title: 'Data Collection',
      description: '620+ reviews aggregated from Google Maps, Yelp, and TripAdvisor spanning 2011-2018',
      number: '01'
    },
    {
      icon: <Brain size={32} strokeWidth={1.5} />,
      title: 'Period Classification',
      description: 'Reviews categorized into Pre (before Feb 2016), During (Feb 2016-May 2018), and Post-Construction periods',
      number: '02'
    },
    {
      icon: <BarChart3 size={32} strokeWidth={1.5} />,
      title: 'Statistical Analysis',
      description: 'Calculated average ratings, trends, and percentage changes across platforms and time periods',
      number: '03'
    },
    {
      icon: <FileCheck size={32} strokeWidth={1.5} />,
      title: 'Visualization',
      description: 'Interactive charts reveal patterns, validate construction impact, and measure recovery success',
      number: '04'
    }
  ];

  return (
    <div className="w-full max-w-6xl mx-auto mb-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="text-center mb-12"
      >
        <h2 className="text-4xl font-bold text-foreground mb-3 tracking-tight">
          Research Methodology
        </h2>
        <p className="text-foreground/60 text-lg font-light">
          A data-driven approach to understanding construction impact
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-50px" }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            whileHover={{ y: -8 }}
            className="relative group"
          >
            {/* Connecting line */}
            {index < steps.length - 1 && (
              <div className="hidden lg:block absolute top-16 -right-3 w-6 h-0.5 bg-border group-hover:bg-primary/50 transition-colors" />
            )}
            
            <div className="relative bg-background border border-border p-6 h-full overflow-hidden">
              {/* Number background */}
              <div className="absolute top-4 right-4 text-6xl font-bold text-foreground/5 group-hover:text-foreground/10 transition-colors">
                {step.number}
              </div>
              
              {/* Icon */}
              <div className="relative z-10 inline-flex p-3 bg-primary/10 mb-4 group-hover:bg-primary/20 transition-colors">
                <div className="text-primary">
                  {step.icon}
                </div>
              </div>
              
              {/* Content */}
              <h3 className="relative z-10 text-lg font-bold text-foreground mb-2 tracking-tight">
                {step.title}
              </h3>
              <p className="relative z-10 text-foreground/60 text-sm leading-relaxed font-light">
                {step.description}
              </p>
              
              {/* Glow effect */}
              <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-primary/0 via-primary to-primary/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
