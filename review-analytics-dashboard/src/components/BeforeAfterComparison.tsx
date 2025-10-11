import { motion } from 'framer-motion';
import { useState, useRef, useEffect } from 'react';
import { ArrowLeftRight } from 'lucide-react';

export default function BeforeAfterComparison() {
  const [sliderPosition, setSliderPosition] = useState(50);
  const [isDragging, setIsDragging] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMove = (clientX: number) => {
    if (!containerRef.current) return;
    
    const rect = containerRef.current.getBoundingClientRect();
    const x = clientX - rect.left;
    const percentage = (x / rect.width) * 100;
    
    setSliderPosition(Math.max(0, Math.min(100, percentage)));
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (isDragging) {
      handleMove(e.clientX);
    }
  };

  const handleTouchMove = (e: TouchEvent) => {
    if (isDragging && e.touches[0]) {
      handleMove(e.touches[0].clientX);
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  useEffect(() => {
    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
      window.addEventListener('touchmove', handleTouchMove);
      window.addEventListener('touchend', handleMouseUp);
      
      return () => {
        window.removeEventListener('mousemove', handleMouseMove);
        window.removeEventListener('mouseup', handleMouseUp);
        window.removeEventListener('touchmove', handleTouchMove);
        window.removeEventListener('touchend', handleMouseUp);
      };
    }
  }, [isDragging]);

  return (
    <div className="w-full max-w-6xl mx-auto mb-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="text-center mb-10"
      >
        <h2 className="text-4xl font-bold text-foreground mb-3 tracking-tight">
          Before & After
        </h2>
        <p className="text-foreground/60 text-lg font-light">
          Drag the slider to compare Love Park's transformation
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, delay: 0.2 }}
        ref={containerRef}
        className="relative w-full h-[500px] overflow-hidden border border-border select-none cursor-col-resize"
        onMouseDown={() => setIsDragging(true)}
        onTouchStart={() => setIsDragging(true)}
      >
        {/* Left Image (Pre-Construction) - Full width base layer */}
        <div className="absolute inset-0">
          <div 
            className="w-full h-full bg-cover bg-center"
            style={{
              backgroundImage: 'url(/images/love-park-before.jpg)',
            }}
          />
          <div 
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center pointer-events-none transition-opacity duration-300"
            style={{
              opacity: sliderPosition > 70 ? 0 : 1
            }}
          >
            <div className="bg-black/70 backdrop-blur-md px-8 py-6 border border-white/20 w-[340px]">
              <h3 className="text-2xl font-bold text-white mb-2">PRE-CONSTRUCTION</h3>
              <p className="text-white/80 text-lg mb-3">Before 2016</p>
              <div className="text-blue-400 text-xl font-medium h-[28px] flex items-center justify-center">
                Average Rating: 3.63 ⭐
              </div>
            </div>
          </div>
        </div>

        {/* Right Image (Post-Construction) - Reveals from right as slider moves right */}
        <div 
          className="absolute inset-0"
          style={{
            clipPath: `inset(0 0 0 ${sliderPosition}%)`
          }}
        >
          <div 
            className="w-full h-full bg-cover bg-center"
            style={{
              backgroundImage: 'url(/images/love-park-after.jpg.png)',
            }}
          />
          <div 
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center pointer-events-none transition-opacity duration-300"
            style={{
              opacity: sliderPosition < 30 ? 0 : 1
            }}
          >
            <div className="bg-black/70 backdrop-blur-md px-8 py-6 border border-white/20 w-[340px]">
              <h3 className="text-2xl font-bold text-white mb-2">POST-CONSTRUCTION</h3>
              <p className="text-white/80 text-lg mb-3">2018+</p>
              <div className="text-accent text-xl font-medium h-[28px] flex items-center justify-center">
                Average Rating: 3.90 ⭐
              </div>
            </div>
          </div>
        </div>

        {/* Slider */}
        <div 
          className="absolute top-0 bottom-0 w-1 bg-white cursor-col-resize"
          style={{ left: `${sliderPosition}%` }}
        >
          {/* Slider Handle */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
            <motion.div
              whileHover={{ scale: 1.1 }}
              className="w-12 h-12 bg-white border-2 border-primary rounded-full flex items-center justify-center shadow-lg"
            >
              <ArrowLeftRight size={20} className="text-primary" strokeWidth={2.5} />
            </motion.div>
          </div>
        </div>

        {/* Instruction hint (shows briefly) */}
        {sliderPosition === 50 && !isDragging && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute top-8 left-1/2 -translate-x-1/2 px-4 py-2 bg-black/80 backdrop-blur-sm border border-white/20 rounded-full"
          >
            <span className="text-white text-sm font-medium flex items-center gap-2">
              <ArrowLeftRight size={16} />
              Drag to compare
            </span>
          </motion.div>
        )}
      </motion.div>

      {/* Stats comparison */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="grid grid-cols-2 gap-4 mt-6"
      >
        <div className="bg-background border border-border p-4 text-center">
          <div className="text-blue-400 text-2xl font-bold mb-1">3.63</div>
          <div className="text-foreground/60 text-sm">Pre-Construction</div>
        </div>
        <div className="bg-background border border-border p-4 text-center">
          <div className="text-accent text-2xl font-bold mb-1">3.90</div>
          <div className="text-foreground/60 text-sm">Post-Construction</div>
        </div>
      </motion.div>
    </div>
  );
}
