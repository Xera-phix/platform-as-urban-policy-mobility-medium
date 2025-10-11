import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

interface AnalyzeButtonProps {
  onClick: () => void;
  disabled: boolean;
}

export default function AnalyzeButton({ onClick, disabled }: AnalyzeButtonProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.4 }}
      className="flex justify-center"
    >
      <motion.button
        whileHover={{ scale: disabled ? 1 : 1.02 }}
        whileTap={{ scale: disabled ? 1 : 0.98 }}
        onClick={onClick}
        disabled={disabled}
        className={`
          group relative px-12 py-4 font-medium text-base tracking-tight
          transition-all duration-300 border
          ${disabled
            ? 'bg-muted/50 text-foreground/30 cursor-not-allowed border-border'
            : 'bg-primary text-white border-primary hover:bg-primary/90'
          }
        `}
      >
        <span className="flex items-center gap-3 uppercase text-sm tracking-wider">
          <Sparkles size={18} className={!disabled ? 'animate-pulse' : ''} strokeWidth={1.5} />
          Analyze Reviews
        </span>
        
        {!disabled && (
          <motion.div
            className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10"
            initial={false}
            transition={{ duration: 0.3 }}
          />
        )}
      </motion.button>
    </motion.div>
  );
}
