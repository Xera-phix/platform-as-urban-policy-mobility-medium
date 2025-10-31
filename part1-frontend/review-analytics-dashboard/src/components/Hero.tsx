import { motion, useScroll, useTransform } from 'framer-motion';
import AnimatedDataPoints from './AnimatedDataPoints';

export default function Hero() {
  const { scrollY } = useScroll();
  
  // Parallax effect - image moves slower than scroll
  const imageY = useTransform(scrollY, [0, 500], [0, 150]);
  const imageOpacity = useTransform(scrollY, [0, 300], [0.4, 0.1]);
  const overlayOpacity = useTransform(scrollY, [0, 300], [1, 0.5]);

  return (
    <div className="relative min-h-[70vh] flex items-center justify-center overflow-hidden bg-background">
      {/* Love Park background image with parallax */}
      <motion.div 
        className="absolute inset-0 bg-cover bg-center"
        style={{
          backgroundImage: 'url(/images/love-park.jpg.png)',
          y: imageY,
          opacity: imageOpacity,
          scale: 1.1, // Slightly larger to prevent white space during parallax
        }}
      />
      
      {/* Dark overlay with smooth gradient fade to background */}
      <motion.div 
        className="absolute inset-0 bg-gradient-to-b from-black/50 via-background/80 to-background"
        style={{ opacity: overlayOpacity }}
      />
      
      {/* Grid pattern overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:64px_64px] opacity-50" />
      
      {/* Animated data points */}
      <AnimatedDataPoints />
      
      {/* Subtle glow effect */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-primary/10 blur-[120px] rounded-full" />

      {/* Content */}
      <div className="relative z-10 text-center px-4 max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-block mb-4">
            <span className="text-xs font-medium tracking-widest text-primary uppercase border border-primary/30 px-4 py-1.5 bg-background/20 backdrop-blur-sm">
              Love Park • JFK Plaza
            </span>
          </div>
          
          <h1 className="text-6xl md:text-7xl font-bold text-white mb-6 tracking-tight drop-shadow-2xl leading-tight">
            Platform as Urban Policy<br/>Mobility Medium
          </h1>
          
          <p className="text-lg md:text-xl text-white/80 mb-12 max-w-2xl mx-auto font-light drop-shadow-lg">
            A case study on Love Park's 2016-2018 renovation impact
          </p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="flex gap-3 justify-center flex-wrap text-sm"
        >
          {['Google Maps', 'Yelp', 'TripAdvisor'].map((platform, index) => (
            <motion.div
              key={platform}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
              whileHover={{ y: -4, scale: 1.05 }}
              className="px-5 py-2.5 bg-black/40 border border-white/20 backdrop-blur-md rounded-sm hover:bg-black/50 hover:border-white/30 transition-all duration-300"
            >
              <span className="text-white/90 font-medium">{platform}</span>
            </motion.div>
          ))}
        </motion.div>
      </div>
      
      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 1 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
          className="flex flex-col items-center gap-2"
        >
          <span className="text-white/60 text-xs tracking-widest uppercase font-light">Scroll to explore</span>
          <div className="w-6 h-10 border border-white/30 rounded-full flex items-start justify-center p-2">
            <motion.div
              animate={{ y: [0, 12, 0] }}
              transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
              className="w-1.5 h-1.5 bg-white/60 rounded-full"
            />
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}
