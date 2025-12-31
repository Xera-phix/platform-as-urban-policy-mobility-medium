/**
 * Supabase client configuration for Love Park review data.
 * 
 * Uses environment variables for secure credential management.
 * The anon/public key is safe for client-side use with RLS policies.
 */

import { createClient } from '@supabase/supabase-js'

// Environment variables defined in .env.local
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_KEY

if (!supabaseUrl || !supabaseKey) {
  throw new Error(
    'Missing Supabase credentials!\n' +
    'Create .env.local with VITE_SUPABASE_URL and VITE_SUPABASE_KEY'
  )
}

/**
 * Supabase client instance.
 * 
 * Configured with Row Level Security (RLS) policies:
 * - Public read access to reviews table
 * - No write access from client (data managed via Python scripts)
 */
export const supabase = createClient(supabaseUrl, supabaseKey)

/**
 * Database schema types (inferred from Supabase table).
 */
export interface Review {
  id: number
  review_id: string
  user_name: string | null
  rating: number
  text: string | null
  date_of_experience: string | null
  date_written: string | null
  title: string | null
  helpful_votes: number
  trip_type: string | null
  period: 'pre_construction' | 'during_construction' | 'post_construction' | 'border_feb2016' | 'border_may2018' | 'missing_date'
  created_at: string
}

/**
 * Aggregated stats by construction period.
 */
export interface PeriodStats {
  period: string
  count: number
  avgRating: number
}

/**
 * Time series data point.
 */
export interface TimeSeriesPoint {
  date: string
  avgRating: number
  count: number
}
