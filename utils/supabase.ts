/**
 * Supabase client configuration for the Wrestling Analytics Dashboard - MVP Version
 * Updated to use modern Supabase client without deprecated packages
 */

import { createClient, type SupabaseClient } from '@supabase/supabase-js';

function getSupabaseUrl(): string {
  return process.env.NEXT_PUBLIC_SUPABASE_URL ?? '';
}

function getSupabaseAnonKey(): string {
  return process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? '';
}

// Lazy check – reads env vars at call time, not module-load time
export function isSupabaseConfigured(): boolean {
  const url = getSupabaseUrl();
  const key = getSupabaseAnonKey();
  const configured =
    url.length > 0 &&
    key.length > 0 &&
    !url.includes('placeholder') &&
    !key.includes('placeholder');

  console.log('[v0] isSupabaseConfigured check:', {
    urlSet: url.length > 0,
    keySet: key.length > 0,
    urlStart: url.substring(0, 30),
    configured,
  });

  return configured;
}

// Lazy singleton – client is created on first use with the real env vars
let _supabase: SupabaseClient | null = null;

export function getSupabase(): SupabaseClient {
  if (!_supabase) {
    const url = getSupabaseUrl() || 'https://placeholder.supabase.co';
    const key = getSupabaseAnonKey() || 'placeholder-key';

    _supabase = createClient(url, key, {
      auth: {
        persistSession: false,
      },
      realtime: {
        params: {
          eventsPerSecond: 10,
        },
      },
    });
  }
  return _supabase;
}

// Keep a default export for backwards-compat with existing code
export const supabase = new Proxy({} as SupabaseClient, {
  get(_target, prop, receiver) {
    return Reflect.get(getSupabase(), prop, receiver);
  },
});

// Helper function to check if Supabase is properly configured
export const checkSupabaseConnection = async (): Promise<boolean> => {
  try {
    if (!isSupabaseConfigured()) {
      console.log('Supabase not configured – missing or placeholder env vars');
      return false;
    }

    const { error } = await getSupabase().from('wrestlers').select('count').limit(1);

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
