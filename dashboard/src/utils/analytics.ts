/**
 * Wrestling Analytics Functions - MVP Version
 * Simple stats only: Wins, Losses, Win %, Match type breakdown
 */

import { supabase } from './supabase';
import type { Wrestler, Match, MatchType } from '../types/database';

// Simplified wrestler statistics for MVP
export interface WrestlerStats {
  wrestler_id: string;
  name: string;
  weight_class: number | null;
  wins: number;
  losses: number;
  total_matches: number;
  win_percentage: number;
  pins: number;
  decisions: number;
  tech_falls: number;
  major_decisions: number;
}

/**
 * Calculate basic wrestler statistics - MVP version
 * Only: Wins, Losses, Win %, Pin/Dec/TF counts
 */
export async function calculateWrestlerStats(wrestlerId: string): Promise<WrestlerStats | null> {
  try {
    // Check if Supabase is configured
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
    if (supabaseUrl.includes('placeholder') || !supabaseUrl) {
      console.warn('Supabase not configured, returning null');
      return null;
    }

    // Get wrestler info
    const { data: wrestler, error: wrestlerError } = await supabase
      .from('wrestlers')
      .select('id, name, weight_class')
      .eq('id', wrestlerId)
      .single();

    if (wrestlerError || !wrestler) {
      console.error('Error fetching wrestler:', wrestlerError);
      return null;
    }

    // Get all matches for this wrestler
    const { data: matches, error: matchesError } = await supabase
      .from('matches')
      .select('*')
      .or(`wrestler1_id.eq.${wrestlerId},wrestler2_id.eq.${wrestlerId}`);

    if (matchesError) {
      console.error('Error fetching matches:', matchesError);
      return null;
    }

    if (!matches || matches.length === 0) {
      // Return empty stats for wrestler with no matches
      return {
        wrestler_id: wrestlerId,
        name: wrestler.name,
        weight_class: wrestler.weight_class,
        wins: 0,
        losses: 0,
        total_matches: 0,
        win_percentage: 0,
        pins: 0,
        decisions: 0,
        tech_falls: 0,
        major_decisions: 0
      };
    }

    // Calculate simple statistics
    let wins = 0;
    let losses = 0;
    let pins = 0;
    let decisions = 0;
    let tech_falls = 0;
    let major_decisions = 0;

    matches.forEach(match => {
      const isWinner = match.winner_id === wrestlerId;

      // Count wins/losses
      if (isWinner) {
        wins++;
        
        // Count match types (only for wins)
        switch (match.match_type) {
          case 'pin':
            pins++;
            break;
          case 'decision':
            decisions++;
            break;
          case 'tech_fall':
            tech_falls++;
            break;
          case 'major_decision':
            major_decisions++;
            break;
        }
      } else {
        losses++;
      }
    });

    const totalMatches = wins + losses;
    const winPercentage = totalMatches > 0 ? Math.round((wins / totalMatches) * 100) : 0;

    return {
      wrestler_id: wrestlerId,
      name: wrestler.name,
      weight_class: wrestler.weight_class,
      wins,
      losses,
      total_matches: totalMatches,
      win_percentage: winPercentage,
      pins,
      decisions,
      tech_falls,
      major_decisions
    };

  } catch (error) {
    console.error('Error calculating wrestler stats:', error);
    return null;
  }
}

/**
 * Get all wrestlers with basic stats for listing page
 * MVP: Just the wrestler list with simple stats
 */
export async function getAllWrestlersWithStats(): Promise<WrestlerStats[]> {
  try {
    // Check if Supabase is configured
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
    if (supabaseUrl.includes('placeholder') || !supabaseUrl) {
      console.warn('Supabase not configured, returning empty array');
      return [];
    }

    const { data: wrestlers, error } = await supabase
      .from('wrestlers')
      .select('id, name, weight_class')
      .order('name');

    if (error || !wrestlers) {
      console.error('Error fetching wrestlers:', error);
      return [];
    }

    // Calculate stats for each wrestler
    const wrestlerStats: WrestlerStats[] = [];
    
    for (const wrestler of wrestlers) {
      const stats = await calculateWrestlerStats(wrestler.id);
      if (stats) {
        wrestlerStats.push(stats);
      }
    }

    return wrestlerStats;

  } catch (error) {
    console.error('Error getting all wrestlers with stats:', error);
    return [];
  }
}

/**
 * Get wrestler matches for profile page
 * MVP: Simple match history
 */
export async function getWrestlerMatches(wrestlerId: string): Promise<Match[]> {
  try {
    // Check if Supabase is configured
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
    if (supabaseUrl.includes('placeholder') || !supabaseUrl) {
      console.warn('Supabase not configured, returning empty array');
      return [];
    }

    const { data: matches, error } = await supabase
      .from('matches')
      .select(`
        *,
        tournament:tournaments(name),
        wrestler1:wrestlers!wrestler1_id(name),
        wrestler2:wrestlers!wrestler2_id(name)
      `)
      .or(`wrestler1_id.eq.${wrestlerId},wrestler2_id.eq.${wrestlerId}`)
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching wrestler matches:', error);
      return [];
    }

    return matches || [];

  } catch (error) {
    console.error('Error getting wrestler matches:', error);
    return [];
  }
}