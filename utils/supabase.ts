/**
 * Supabase client configuration for the Wrestling Analytics Dashboard - MVP Version
 * Updated to use modern Supabase client without deprecated packages
 */

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? '';

// Determine if Supabase is configured once at module load
export const isSupabaseConfigured =
  supabaseUrl.length > 0 &&
  supabaseAnonKey.length > 0 &&
  !supabaseUrl.includes('placeholder') &&
  !supabaseAnonKey.includes('placeholder');

// Create Supabase client – if not configured we still create a client with
// dummy values so imports never crash, but every query will fail gracefully.
export const supabase = createClient(
  supabaseUrl || 'https://placeholder.supabase.co',
  supabaseAnonKey || 'placeholder-key',
  {
    auth: {
      persistSession: false, // Simplified for MVP - no user auth needed
    },
    realtime: {
      params: {
        eventsPerSecond: 10,
      },
    },
  },
);

// Helper function to check if Supabase is properly configured
export const checkSupabaseConnection = async (): Promise<boolean> => {
  try {
    if (!isSupabaseConfigured) {
      console.log('Supabase not configured – missing or placeholder env vars');
      return false;
    }

    // Simple connection test
    const { error } = await supabase.from('wrestlers').select('count').limit(1);

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
