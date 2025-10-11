import { motion } from 'framer-motion';
import { Check, MapPin, Utensils, Plane } from 'lucide-react';

interface DataSource {
  id: string;
  name: string;
  description: string;
  icon: React.ElementType;
}

const dataSources: DataSource[] = [
  { id: 'google', name: 'Google Maps', description: 'Local business reviews', icon: MapPin },
  { id: 'yelp', name: 'Yelp', description: 'Restaurant & service reviews', icon: Utensils },
  { id: 'tripadvisor', name: 'TripAdvisor', description: 'Travel & hospitality reviews', icon: Plane },
];

interface DataSourceSelectorProps {
  selected: string;
  onSelect: (id: string) => void;
}

export default function DataSourceSelector({ selected, onSelect }: DataSourceSelectorProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="w-full max-w-3xl mx-auto"
    >
      <h3 className="text-xl font-medium text-foreground mb-6 tracking-tight">
        Select Data Source
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {dataSources.map((source) => (
          <motion.button
            key={source.id}
            onClick={() => onSelect(source.id)}
            whileHover={{ y: -4 }}
            whileTap={{ scale: 0.98 }}
            className={`
              relative p-6 border transition-all duration-300
              ${selected === source.id
                ? 'border-primary bg-primary/5'
                : 'border-border bg-muted/30 hover:border-primary/50'
              }
            `}
          >
            <div className="flex items-center justify-between mb-3">
              <source.icon 
                size={28} 
                className={selected === source.id ? 'text-primary' : 'text-foreground/40'} 
                strokeWidth={1.5}
              />
              {selected === source.id && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                >
                  <Check size={20} className="text-primary" strokeWidth={2} />
                </motion.div>
              )}
            </div>
            
            <h4 className={`text-base font-medium mb-1 tracking-tight ${
              selected === source.id ? 'text-foreground' : 'text-foreground/70'
            }`}>
              {source.name}
            </h4>
            <p className="text-xs text-foreground/40 font-light">
              {source.description}
            </p>
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
}
