import { motion } from 'framer-motion';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceArea } from 'recharts';
import { useState, useEffect } from 'react';
import { Box, Layers } from 'lucide-react';

interface RatingByPeriod {
  period: string;
  avgRating: number;
  reviews: number;
}

interface TimelinePoint {
  month: string;
  googleRating: number;
  yelpRating: number;
  tripadvisorRating: number;
}

interface VolumeByPlatform {
  period: string;
  google: number;
  yelp: number;
  tripadvisor: number;
}

interface FrontendData {
  ratingsByPeriod: RatingByPeriod[];
  multiPlatformTimeline: TimelinePoint[];
  reviewVolumeByPlatform: VolumeByPlatform[];
}

interface CustomTooltipProps {
  active?: boolean;
  payload?: any[];
  label?: string;
}

const CustomTooltip = ({ active, payload, label }: CustomTooltipProps) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-muted border border-border p-3 text-xs">
        <p className="text-foreground font-medium mb-2">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={index} style={{ color: entry.color }} className="font-light">
            {entry.name}: {typeof entry.value === 'number' ? entry.value.toFixed(2) : entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function InteractiveGraphs() {
  const [activeGraph, setActiveGraph] = useState<'ratings' | 'timeline' | 'volume'>('timeline');
  const [data, setData] = useState<FrontendData | null>(null);
  const [loading, setLoading] = useState(true);
  const [is3D, setIs3D] = useState(false);

  useEffect(() => {
    // Load real data from the public folder
    fetch('/frontend_data.json')
      .then(response => response.json())
      .then((jsonData: FrontendData) => {
        setData(jsonData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading data:', error);
        setLoading(false);
      });
  }, []);

  const graphs = [
    { id: 'ratings' as const, name: 'Ratings by Period', description: 'Average ratings across construction phases' },
    { id: 'timeline' as const, name: 'Rating Timeline', description: 'Rating trends over time' },
    { id: 'volume' as const, name: 'Review Volume', description: 'Number of reviews by platform' },
  ];

  if (loading || !data) {
    return (
      <div className="w-full max-w-6xl mx-auto">
        <div className="bg-background border border-border p-12 text-center">
          <p className="text-foreground/40 text-sm tracking-wide">LOADING DATA...</p>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-6xl mx-auto"
    >
      {/* Header with 3D Toggle */}
      <div className="flex items-center justify-between mb-8">
        <h2 className="text-3xl font-bold text-foreground tracking-tight">
          Data Visualizations
        </h2>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setIs3D(!is3D)}
          className={`
            flex items-center gap-2 px-4 py-2 border transition-all text-sm
            ${is3D 
              ? 'bg-primary border-primary text-white' 
              : 'bg-background border-border text-foreground hover:border-primary/50'
            }
          `}
        >
          {is3D ? <Box size={18} strokeWidth={1.5} /> : <Layers size={18} strokeWidth={1.5} />}
          <span className="font-medium">{is3D ? '3D View' : '2D View'}</span>
        </motion.button>
      </div>

      {/* Graph Selector */}
      <div className="flex gap-3 mb-8 justify-center">
        {graphs.map((graph) => (
          <motion.button
            key={graph.id}
            onClick={() => setActiveGraph(graph.id)}
            whileHover={{ y: -4 }}
            whileTap={{ scale: 0.98 }}
            className={`
              px-6 py-3 border transition-all text-sm tracking-wide rounded-sm
              ${activeGraph === graph.id
                ? 'border-primary bg-primary/10 text-foreground'
                : 'border-border bg-muted/30 text-foreground/60 hover:border-primary/50 hover:bg-muted/50'
              }
            `}
          >
            <div className="text-left">
              <p className="font-medium">{graph.name}</p>
              <p className="text-xs text-foreground/40 font-light">{graph.description}</p>
            </div>
          </motion.button>
        ))}
      </div>

      {/* Graph Display */}
      <motion.div
        key={activeGraph}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3 }}
        className={`
          bg-background border border-border p-8 transition-all duration-500
          ${is3D ? 'shadow-2xl' : ''}
        `}
        style={{
          transform: is3D ? 'perspective(1000px) rotateX(5deg) rotateY(-5deg)' : 'none',
          transformStyle: 'preserve-3d'
        }}
      >
        {activeGraph === 'ratings' && (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.ratingsByPeriod}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(240 5% 20%)" />
              <XAxis 
                dataKey="period" 
                stroke="hsl(0 0% 98%)" 
                tick={{ fill: 'hsl(0 0% 98%)', fontSize: 12 }}
              />
              <YAxis 
                stroke="hsl(0 0% 98%)" 
                tick={{ fill: 'hsl(0 0% 98%)', fontSize: 12 }}
                domain={[0, 5]}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'hsl(210 100% 60% / 0.1)' }} />
              <Legend wrapperStyle={{ color: 'hsl(0 0% 98%)' }} />
              <Bar 
                dataKey="avgRating" 
                fill="hsl(210 100% 60%)" 
                name="Average Rating"
                radius={[0, 0, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        )}

        {activeGraph === 'timeline' && (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data.multiPlatformTimeline}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(240 5% 20%)" />
              
              {/* Highlight construction period */}
              <ReferenceArea
                x1="2016Q1"
                x2="2018Q2"
                fill="hsl(0 100% 50%)"
                fillOpacity={0.1}
                label={{ value: 'Construction Period', position: 'top', fill: 'hsl(0 0% 98%)', fontSize: 11 }}
              />
              
              <XAxis 
                dataKey="month" 
                stroke="hsl(0 0% 98%)" 
                tick={{ fill: 'hsl(0 0% 98%)', fontSize: 10 }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                stroke="hsl(0 0% 98%)" 
                tick={{ fill: 'hsl(0 0% 98%)', fontSize: 12 }}
                domain={[0, 5]}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ color: 'hsl(0 0% 98%)' }} />
              <Line 
                type="monotone" 
                dataKey="googleRating" 
                stroke="hsl(210 100% 60%)" 
                name="Google Maps"
                strokeWidth={2}
                dot={{ fill: 'hsl(210 100% 60%)', r: 3 }}
                activeDot={{ r: 5 }}
              />
              <Line 
                type="monotone" 
                dataKey="yelpRating" 
                stroke="hsl(165 100% 50%)" 
                name="Yelp"
                strokeWidth={2}
                dot={{ fill: 'hsl(165 100% 50%)', r: 3 }}
                activeDot={{ r: 5 }}
              />
              <Line 
                type="monotone" 
                dataKey="tripadvisorRating" 
                stroke="hsl(280 100% 70%)" 
                name="TripAdvisor"
                strokeWidth={2}
                dot={{ fill: 'hsl(280 100% 70%)', r: 3 }}
                activeDot={{ r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        )}

        {activeGraph === 'volume' && (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data.reviewVolumeByPlatform}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(240 5% 20%)" />
              <XAxis 
                dataKey="period" 
                stroke="hsl(0 0% 98%)" 
                tick={{ fill: 'hsl(0 0% 98%)', fontSize: 12 }}
              />
              <YAxis 
                stroke="hsl(0 0% 98%)" 
                tick={{ fill: 'hsl(0 0% 98%)', fontSize: 12 }}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'hsl(210 100% 60% / 0.1)' }} />
              <Legend wrapperStyle={{ color: 'hsl(0 0% 98%)' }} />
              <Bar dataKey="google" fill="hsl(210 100% 60%)" name="Google Maps" />
              <Bar dataKey="yelp" fill="hsl(165 100% 50%)" name="Yelp" />
              <Bar dataKey="tripadvisor" fill="hsl(280 100% 70%)" name="TripAdvisor" />
            </BarChart>
          </ResponsiveContainer>
        )}

        {/* Graph Info */}
        <div className="mt-6 text-center">
          <p className="text-xs text-foreground/40 font-light tracking-wide uppercase">
            Hover over data points for detailed information
          </p>
        </div>
      </motion.div>
    </motion.div>
  );
}
