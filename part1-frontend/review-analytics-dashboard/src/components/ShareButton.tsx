import { motion, AnimatePresence } from 'framer-motion';
import { Share2, Twitter, Linkedin, Facebook, Link, Check } from 'lucide-react';
import { useState } from 'react';

export default function ShareButton() {
  const [isOpen, setIsOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  const shareData = {
    title: 'Love Park Construction Impact Analysis',
    text: 'Discover how the 2016-2018 Love Park renovation affected visitor sentiment. Ratings dropped 2.5% during construction but surged 10.2% post-renovation! 📊',
    url: window.location.href
  };

  const handleCopyLink = async () => {
    try {
      await navigator.clipboard.writeText(shareData.url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleTwitterShare = () => {
    const text = encodeURIComponent(shareData.text);
    const url = encodeURIComponent(shareData.url);
    window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`, '_blank');
  };

  const handleLinkedInShare = () => {
    const url = encodeURIComponent(shareData.url);
    window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank');
  };

  const handleFacebookShare = () => {
    const url = encodeURIComponent(shareData.url);
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank');
  };

  return (
    <div className="fixed bottom-8 right-8 z-50">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="absolute bottom-16 right-0 bg-background border border-border p-2 shadow-2xl min-w-[200px]"
          >
            <div className="space-y-1">
              <motion.button
                whileHover={{ x: 4 }}
                onClick={handleTwitterShare}
                className="w-full flex items-center gap-3 px-4 py-2.5 text-foreground/80 hover:text-foreground hover:bg-muted/50 transition-colors text-left"
              >
                <Twitter size={18} strokeWidth={1.5} />
                <span className="text-sm font-medium">Share on Twitter</span>
              </motion.button>

              <motion.button
                whileHover={{ x: 4 }}
                onClick={handleLinkedInShare}
                className="w-full flex items-center gap-3 px-4 py-2.5 text-foreground/80 hover:text-foreground hover:bg-muted/50 transition-colors text-left"
              >
                <Linkedin size={18} strokeWidth={1.5} />
                <span className="text-sm font-medium">Share on LinkedIn</span>
              </motion.button>

              <motion.button
                whileHover={{ x: 4 }}
                onClick={handleFacebookShare}
                className="w-full flex items-center gap-3 px-4 py-2.5 text-foreground/80 hover:text-foreground hover:bg-muted/50 transition-colors text-left"
              >
                <Facebook size={18} strokeWidth={1.5} />
                <span className="text-sm font-medium">Share on Facebook</span>
              </motion.button>

              <div className="border-t border-border my-1" />

              <motion.button
                whileHover={{ x: 4 }}
                onClick={handleCopyLink}
                className="w-full flex items-center gap-3 px-4 py-2.5 text-foreground/80 hover:text-foreground hover:bg-muted/50 transition-colors text-left"
              >
                {copied ? (
                  <>
                    <Check size={18} strokeWidth={1.5} className="text-accent" />
                    <span className="text-sm font-medium text-accent">Link Copied!</span>
                  </>
                ) : (
                  <>
                    <Link size={18} strokeWidth={1.5} />
                    <span className="text-sm font-medium">Copy Link</span>
                  </>
                )}
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(!isOpen)}
        className={`
          flex items-center gap-2 px-5 py-3 border transition-all
          ${isOpen 
            ? 'bg-primary border-primary text-white' 
            : 'bg-background border-border text-foreground hover:border-primary/50'
          }
        `}
      >
        <Share2 size={20} strokeWidth={1.5} />
        <span className="text-sm font-medium tracking-wide">
          {isOpen ? 'Close' : 'Share'}
        </span>
      </motion.button>
    </div>
  );
}
