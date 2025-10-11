import { motion, AnimatePresence } from 'framer-motion';
import { GitCompare, X, Wrench } from 'lucide-react';
import { useState } from 'react';

export default function ComparisonMode() {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-6xl mx-auto mb-16"
      >
        <div className="bg-gradient-to-br from-primary/5 to-accent/5 border border-primary/20 p-8 text-center">
          <motion.div
            initial={{ scale: 0 }}
            whileInView={{ scale: 1 }}
            viewport={{ once: true }}
            transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.2 }}
          >
            <GitCompare size={48} className="text-primary mx-auto mb-4" strokeWidth={1.5} />
          </motion.div>
          
          <h3 className="text-2xl font-bold text-foreground mb-3 tracking-tight">
            Compare Multiple Landmarks
          </h3>
          <p className="text-foreground/60 mb-6 max-w-2xl mx-auto font-light">
            Want to compare Love Park's construction impact with other Philadelphia landmarks? 
            This powerful feature is currently under development.
          </p>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowModal(true)}
            className="px-8 py-3 bg-primary text-white font-medium tracking-wide hover:bg-primary/90 transition-colors"
          >
            Preview Feature
          </motion.button>
        </div>
      </motion.div>

      {/* Modal */}
      <AnimatePresence>
        {showModal && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowModal(false)}
              className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50"
            />
            
            {/* Modal Content */}
            <div className="fixed inset-0 flex items-center justify-center z-50 p-4">
              <motion.div
                initial={{ opacity: 0, scale: 0.9, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.9, y: 20 }}
                className="bg-background border border-border max-w-2xl w-full p-8 relative"
              >
                {/* Close button */}
                <button
                  onClick={() => setShowModal(false)}
                  className="absolute top-4 right-4 text-foreground/60 hover:text-foreground transition-colors"
                >
                  <X size={24} strokeWidth={1.5} />
                </button>

                {/* Content */}
                <div className="text-center">
                  <motion.div
                    animate={{ rotate: [0, 5, -5, 0] }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                  >
                    <Wrench size={64} className="text-primary mx-auto mb-6" strokeWidth={1.5} />
                  </motion.div>
                  
                  <h2 className="text-3xl font-bold text-foreground mb-4 tracking-tight">
                    Feature In Development
                  </h2>
                  
                  <p className="text-foreground/70 mb-6 leading-relaxed">
                    The <span className="font-semibold text-primary">Comparison Mode</span> will allow you to:
                  </p>

                  <div className="space-y-3 text-left mb-8 bg-muted/30 p-6 border border-border">
                    <div className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                      <p className="text-foreground/80 text-sm">
                        <strong>Compare multiple landmarks</strong> side-by-side (e.g., Rittenhouse Square, Logan Circle, Independence Mall)
                      </p>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                      <p className="text-foreground/80 text-sm">
                        <strong>Analyze construction impacts</strong> across different Philadelphia locations
                      </p>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                      <p className="text-foreground/80 text-sm">
                        <strong>View synchronized timelines</strong> showing how different projects affected visitor sentiment
                      </p>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                      <p className="text-foreground/80 text-sm">
                        <strong>Generate comparative reports</strong> for urban planning insights
                      </p>
                    </div>
                  </div>

                  <div className="bg-accent/10 border border-accent/30 p-4 mb-6">
                    <p className="text-sm text-foreground/70 font-light">
                      <span className="font-semibold text-accent">Coming Soon!</span> This feature requires additional data collection and analysis across multiple Philadelphia landmarks.
                    </p>
                  </div>

                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowModal(false)}
                    className="px-8 py-3 bg-foreground text-background font-medium tracking-wide hover:bg-foreground/90 transition-colors"
                  >
                    Got It!
                  </motion.button>
                </div>
              </motion.div>
            </div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
