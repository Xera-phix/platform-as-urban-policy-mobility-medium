/**
 * Service for fetching review data from Supabase database.
 * 
 * Provides aggregated statistics and time series data for dashboard components.
 * All queries respect RLS policies (public read-only access).
 */

import { supabase, Review } from './supabase'

/**
 * Period mapping for display labels.
 */
const PERIOD_LABELS: Record<string, string> = {
  pre_construction: 'Pre-Construction',
  during_construction: 'During Construction',
  post_construction: 'Post-Construction'
}

/**
 * Fetch average ratings by construction period.
 * 
 * @returns Array of period stats with average rating and review count
 */
export async function getRatingsByPeriod() {
  const periods = ['pre_construction', 'during_construction', 'post_construction']
  
  const results = await Promise.all(
    periods.map(async (period) => {
      const { data, error } = await supabase
        .from('reviews')
        .select('rating')
        .eq('period', period)
      
      if (error) throw error
      
      const ratings = data.map(r => r.rating)
      const avgRating = ratings.reduce((sum, r) => sum + r, 0) / ratings.length
      
      return {
        period: PERIOD_LABELS[period],
        avgRating: Math.round(avgRating * 100) / 100,
        reviews: ratings.length
      }
    })
  )
  
  return results
}

/**
 * Fetch time series data for rating trends.
 * Currently returns TripAdvisor data only.
 * 
 * @returns Array of quarterly data points with average rating
 */
export async function getRatingTimeline() {
  const { data, error } = await supabase
    .from('reviews')
    .select('date_of_experience, rating, period')
    .not('period', 'eq', 'missing_date')
    .order('date_of_experience')
  
  if (error) throw error
  
  // Group by quarter
  const quarterlyData: Record<string, { ratings: number[], count: number }> = {}
  
  data.forEach((review: any) => {
    if (!review.date_of_experience) return
    
    const date = new Date(review.date_of_experience)
    const year = date.getFullYear()
    const quarter = Math.floor(date.getMonth() / 3) + 1
    const key = `${year}Q${quarter}`
    
    if (!quarterlyData[key]) {
      quarterlyData[key] = { ratings: [], count: 0 }
    }
    
    quarterlyData[key].ratings.push(review.rating)
    quarterlyData[key].count++
  })
  
  // Calculate averages for each quarter
  return Object.entries(quarterlyData).map(([month, data]) => {
    const avgRating = data.ratings.reduce((sum, r) => sum + r, 0) / data.ratings.length
    
    return {
      month,
      tripadvisorRating: Math.round(avgRating * 100) / 100,
      googleRating: Math.round((avgRating + 0.3) * 100) / 100, // Synthetic Google data
      yelpRating: Math.round((avgRating - 0.2) * 100) / 100 // Synthetic Yelp data
    }
  })
}

/**
 * Fetch review volume by platform.
 * Currently returns actual TripAdvisor data with synthetic Google/Yelp data.
 * 
 * @returns Array of period counts by platform
 */
export async function getReviewVolumeByPlatform() {
  const periods = ['pre_construction', 'during_construction', 'post_construction']
  const labels = ['Pre', 'During', 'Post']
  
  const results = await Promise.all(
    periods.map(async (period, idx) => {
      const { count, error } = await supabase
        .from('reviews')
        .select('*', { count: 'exact', head: true })
        .eq('period', period)
      
      if (error) throw error
      
      return {
        period: labels[idx],
        tripadvisor: count || 0,
        google: Math.round((count || 0) * 1.2), // Synthetic: ~20% more reviews
        yelp: Math.round((count || 0) * 0.8) // Synthetic: ~20% fewer reviews
      }
    })
  )
  
  return results
}

/**
 * Fetch all dashboard data in one call for efficiency.
 * 
 * @returns Object with all dashboard data sections
 */
export async function getAllDashboardData() {
  try {
    const [ratingsByPeriod, multiPlatformTimeline, reviewVolumeByPlatform] = await Promise.all([
      getRatingsByPeriod(),
      getRatingTimeline(),
      getReviewVolumeByPlatform()
    ])
    
    return {
      ratingsByPeriod,
      multiPlatformTimeline,
      reviewVolumeByPlatform
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    throw error
  }
}

/**
 * Fetch recent reviews for display.
 * 
 * @param limit Number of reviews to fetch
 * @returns Array of recent reviews sorted by date
 */
export async function getRecentReviews(limit: number = 10) {
  const { data, error } = await supabase
    .from('reviews')
    .select('user_name, rating, title, text, date_of_experience, period')
    .order('date_of_experience', { ascending: false })
    .limit(limit)
  
  if (error) throw error
  return data
}

/**
 * Get total review count.
 */
export async function getTotalReviewCount() {
  const { count, error } = await supabase
    .from('reviews')
    .select('*', { count: 'exact', head: true })
  
  if (error) throw error
  return count || 0
}
