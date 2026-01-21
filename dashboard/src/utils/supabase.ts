/**
 * Supabase client configuration for the Wrestling Analytics Dashboard - MVP Version
 * Simplified for basic functionality
 */

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-key';

// Create Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  realtime: {
    params: {
      eventsPerSecond: 10,
    },
  },
});

// Helper function to check if Supabase is properly configured
export const checkSupabaseConnection = async (): Promise<boolean> => {
  try {
    // Don't attempt connection if using placeholder values
    if (supabaseUrl.includes('placeholder') || supabaseAnonKey.includes('placeholder')) {
      return false;
    }
    
    const { data, error } = await supabase.from('wrestlers').select('count').limit(1);
    return !error;
  } catch (error) {
    console.error('Supabase connection check failed:', error);
    return false;
  }
};