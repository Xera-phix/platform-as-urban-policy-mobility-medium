import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Hero from './components/Hero';
import InteractiveGraphs from './components/InteractiveGraphs';
import DataSourceSelector from './components/DataSourceSelector';
import AnalyzeButton from './components/AnalyzeButton';
import DarkModeToggle from './components/DarkModeToggle';
import StatsCounter from './components/StatsCounter';
import KeyInsights from './components/KeyInsights';
import Methodology from './components/Methodology';
import ShareButton from './components/ShareButton';
import BeforeAfterComparison from './components/BeforeAfterComparison';
import ComparisonMode from './components/ComparisonMode';

export default function App() {
  const [dataSource, setDataSource] = useState<string>('google');
  const [showAnalysis, setShowAnalysis] = useState(false);

  const handleAnalyze = () => {
    setShowAnalysis(true);
  };

  return (
    <div className="min-h-screen bg-background transition-colors duration-300">
      <DarkModeToggle />
      <ShareButton />
      
      <Hero />
      
      <div className="container mx-auto px-6 py-20 space-y-16">
        <StatsCounter />
        
        <InteractiveGraphs />
        
        <KeyInsights />
        
        <BeforeAfterComparison />
        
        <DataSourceSelector 
          selected={dataSource} 
          onSelect={setDataSource} 
        />
        
        <ComparisonMode />
        
        <Methodology />
        
        <AnalyzeButton 
          onClick={handleAnalyze} 
          disabled={false}
        />

        <AnimatePresence>
          {showAnalysis && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="bg-background border border-border p-8 text-center"
            >
              <p className="text-xl text-foreground tracking-tight">
                Analysis complete for {dataSource === 'google' ? 'Google Maps' : dataSource === 'yelp' ? 'Yelp' : 'TripAdvisor'}
              </p>
              <p className="text-sm text-foreground/40 mt-2 font-light">
                Interactive visualizations displayed above
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      
      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="text-center py-12 text-foreground/30 text-sm tracking-wide"
      >
        <div className="mb-6">
          <p className="text-foreground/60 text-base mb-2 font-medium">Built by Luke Pan</p>
          <p className="text-foreground/40 text-sm mb-1">Under the direct supervision of Khalil Martin</p>
          <p className="text-foreground/30 text-sm">Research conducted under Dr. Daniel Silver</p>
        </div>
        <p className="font-light">BUILT WITH REACT • TYPESCRIPT • FRAMER MOTION</p>
      </motion.footer>
    </div>
  );
}
