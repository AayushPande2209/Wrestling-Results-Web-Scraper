/**
 * TypeScript type definitions for the Wrestling Analytics Platform database schema - MVP Version
 * Simplified: wrestlers, tournaments, matches only
 */

export interface Wrestler {
  id: string;
  name: string;
  weight_class: number | null;
  created_at: string;
}

export interface Tournament {
  id: string;
  name: string;
  date: string | null;
  created_at: string;
}

export interface Match {
  id: string;
  tournament_id: string | null;
  wrestler1_id: string;
  wrestler2_id: string;
  winner_id: string | null;
  wrestler1_score: number;
  wrestler2_score: number;
  match_type: MatchType;
  round: string | null;
  created_at: string;
  
  // Relationships (populated by joins)
  tournament?: Tournament;
  wrestler1?: Wrestler;
  wrestler2?: Wrestler;
  winner?: Wrestler;
}

// Enums
export type MatchType = 
  | 'decision' 
  | 'major_decision' 
  | 'tech_fall' 
  | 'pin' 
  | 'forfeit' 
  | 'disqualification';

// Weight classes for wrestling
export const WEIGHT_CLASSES = [
  106, 113, 120, 126, 132, 138, 145, 152, 160, 170, 182, 195, 220, 285
] as const;

export type WeightClass = typeof WEIGHT_CLASSES[number];

// Database table names for Supabase queries
export const TABLE_NAMES = {
  WRESTLERS: 'wrestlers',
  TOURNAMENTS: 'tournaments',
  MATCHES: 'matches',
} as const;