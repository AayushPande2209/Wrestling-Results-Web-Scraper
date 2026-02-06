/**
 * Supabase client configuration for the Wrestling Analytics Dashboard - MVP Version
 * Updated to use modern Supabase client without deprecated packages
 */

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-key';

// Create Supabase client with basic configuration
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: false, // Simplified for MVP - no user auth needed
  },
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
      console.log('Supabase not configured, using placeholder values');
      return false;
    }
    
    // Simple connection test
    const { data, error } = await supabase.from('wrestlers').select('count').limit(1);
    
    if (error) {
      console.error('Supabase connection error:', error);
      return false;
    }
    
    return true;
  } catch (error) {
    console.error('Supabase connection check failed:', error);
    return false;
  }
};