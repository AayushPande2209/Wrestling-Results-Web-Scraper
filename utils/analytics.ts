/**
 * Wrestling Analytics Functions - MVP Version
 * Simple stats only: Wins, Losses, Win %, Match type breakdown
 */

import { supabase, isSupabaseConfigured } from './supabase';
import type { Wrestler, Match, MatchType, Tournament } from '../types/database';

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
    if (!isSupabaseConfigured()) {
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
    if (!isSupabaseConfigured()) {
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
    if (!isSupabaseConfigured()) {
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

/**
 * Get performance data over time for charts
 * Aggregates matches by date for performance visualization
 */
export interface PerformanceDataPoint {
  date: string;
  wins: number;
  matches: number;
  pins: number;
}

export async function getPerformanceOverTime(wrestlerId?: string): Promise<PerformanceDataPoint[]> {
  try {
    if (!isSupabaseConfigured()) {
      console.warn('Supabase not configured, returning empty array');
      return [];
    }

    let query = supabase
      .from('matches')
      .select(`
        created_at,
        winner_id,
        wrestler1_id,
        wrestler2_id,
        match_type,
        tournaments!inner(date)
      `)
      .order('created_at', { ascending: true });

    // Filter by wrestler if provided
    if (wrestlerId) {
      query = query.or(`wrestler1_id.eq.${wrestlerId},wrestler2_id.eq.${wrestlerId}`);
    }

    const { data: matches, error } = await query;

    if (error) {
      console.error('Error fetching performance data:', error);
      return [];
    }

    if (!matches || matches.length === 0) {
      return [];
    }

    // Group matches by date
    const dateGroups: { [key: string]: { wins: number; matches: number; pins: number } } = {};

    matches.forEach(match => {
      // Use tournament date if available, otherwise use created_at
      const tournamentData = (match as any).tournaments;
      const matchDate = tournamentData?.date || match.created_at.split('T')[0];
      
      if (!dateGroups[matchDate]) {
        dateGroups[matchDate] = { wins: 0, matches: 0, pins: 0 };
      }

      dateGroups[matchDate].matches++;

      // Check if this wrestler won (only if filtering by wrestler)
      if (wrestlerId && match.winner_id === wrestlerId) {
        dateGroups[matchDate].wins++;
        
        // Count pins
        if (match.match_type === 'pin') {
          dateGroups[matchDate].pins++;
        }
      } else if (!wrestlerId) {
        // For overall stats, count all wins
        if (match.winner_id) {
          dateGroups[matchDate].wins++;
        }
        
        // Count all pins
        if (match.match_type === 'pin') {
          dateGroups[matchDate].pins++;
        }
      }
    });

    // Convert to array and sort by date
    return Object.entries(dateGroups)
      .map(([date, data]) => ({
        date,
        wins: data.wins,
        matches: data.matches,
        pins: data.pins
      }))
      .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  } catch (error) {
    console.error('Error getting performance over time:', error);
    return [];
  }
}

/**
 * Team statistics interface
 */
export interface TeamStats {
  team_name: string;
  wrestler_count: number;
  total_wins: number;
  total_losses: number;
  total_matches: number;
  win_percentage: number;
  pins: number;
  top_wrestler: string;
}

/**
 * Extract team name from wrestler name (simple heuristic)
 * This is a temporary solution until proper team data is available
 */
function extractTeamFromWrestlerName(wrestlerName: string): string {
  // Simple heuristic: assume team name is in parentheses or after a dash
  // Examples: "John Smith (Eagles)", "Mike Johnson - Tigers", "Dave Wilson"
  
  // Check for parentheses pattern
  const parenMatch = wrestlerName.match(/\(([^)]+)\)$/);
  if (parenMatch) {
    return parenMatch[1].trim();
  }
  
  // Check for dash pattern
  const dashMatch = wrestlerName.match(/\s-\s(.+)$/);
  if (dashMatch) {
    return dashMatch[1].trim();
  }
  
  // If no pattern found, use a generic team name based on first letter
  const firstLetter = wrestlerName.charAt(0).toUpperCase();
  return `Team ${firstLetter}`;
}

/**
 * Get all teams with statistics
 */
export async function getAllTeamsWithStats(): Promise<TeamStats[]> {
  try {
    if (!isSupabaseConfigured()) {
      console.warn('Supabase not configured, returning empty array');
      return [];
    }

    // Get all wrestlers with their match data
    const wrestlers = await getAllWrestlersWithStats();
    
    if (wrestlers.length === 0) {
      return [];
    }

    // Group wrestlers by team
    const teamGroups: { [teamName: string]: WrestlerStats[] } = {};
    
    wrestlers.forEach(wrestler => {
      const teamName = extractTeamFromWrestlerName(wrestler.name);
      if (!teamGroups[teamName]) {
        teamGroups[teamName] = [];
      }
      teamGroups[teamName].push(wrestler);
    });

    // Calculate team statistics
    const teamStats: TeamStats[] = [];
    
    Object.entries(teamGroups).forEach(([teamName, teamWrestlers]) => {
      const totalWins = teamWrestlers.reduce((sum, w) => sum + w.wins, 0);
      const totalLosses = teamWrestlers.reduce((sum, w) => sum + w.losses, 0);
      const totalMatches = totalWins + totalLosses;
      const winPercentage = totalMatches > 0 ? Math.round((totalWins / totalMatches) * 100) : 0;
      const pins = teamWrestlers.reduce((sum, w) => sum + w.pins, 0);
      
      // Find top wrestler (highest win percentage with at least 3 matches)
      const topWrestler = teamWrestlers
        .filter(w => w.total_matches >= 3)
        .sort((a, b) => b.win_percentage - a.win_percentage)[0];
      
      teamStats.push({
        team_name: teamName,
        wrestler_count: teamWrestlers.length,
        total_wins: totalWins,
        total_losses: totalLosses,
        total_matches: totalMatches,
        win_percentage: winPercentage,
        pins: pins,
        top_wrestler: topWrestler ? topWrestler.name : teamWrestlers[0]?.name || 'N/A'
      });
    });

    // Sort by win percentage, then by total wins
    return teamStats.sort((a, b) => {
      if (b.win_percentage !== a.win_percentage) {
        return b.win_percentage - a.win_percentage;
      }
      return b.total_wins - a.total_wins;
    });

  } catch (error) {
    console.error('Error getting teams with stats:', error);
    return [];
  }
}

/**
 * Get team comparison data for charts
 */
export interface TeamComparisonData {
  team_name: string;
  wins: number;
  matches: number;
  win_percentage: number;
}

export async function getTeamComparisonData(): Promise<TeamComparisonData[]> {
  try {
    const teams = await getAllTeamsWithStats();
    
    return teams.map(team => ({
      team_name: team.team_name,
      wins: team.total_wins,
      matches: team.total_matches,
      win_percentage: team.win_percentage
    }));

  } catch (error) {
    console.error('Error getting team comparison data:', error);
    return [];
  }
}

/**
 * Get win types data for charts
 */
export interface WinTypeData {
  type: string;
  count: number;
}

/**
 * Tournament statistics interface
 */
export interface TournamentStats {
  tournament_id: string;
  name: string;
  date: string | null;
  total_matches: number;
  total_wins: number;
  participating_teams: number;
  match_types: {
    pins: number;
    decisions: number;
    tech_falls: number;
    major_decisions: number;
  };
}

/**
 * Get all tournaments with statistics
 */
export async function getAllTournamentsWithStats(): Promise<TournamentStats[]> {
  try {
    if (!isSupabaseConfigured()) {
      console.warn('Supabase not configured, returning empty array');
      return [];
    }

    // Get all tournaments
    const { data: tournaments, error: tournamentsError } = await supabase
      .from('tournaments')
      .select('id, name, date')
      .order('date', { ascending: false });

    if (tournamentsError || !tournaments) {
      console.error('Error fetching tournaments:', tournamentsError);
      return [];
    }

    // Get statistics for each tournament
    const tournamentStats: TournamentStats[] = [];

    for (const tournament of tournaments) {
      // Get all matches for this tournament
      const { data: matches, error: matchesError } = await supabase
        .from('matches')
        .select(`
          *,
          wrestler1:wrestlers!wrestler1_id(name),
          wrestler2:wrestlers!wrestler2_id(name)
        `)
        .eq('tournament_id', tournament.id);

      if (matchesError) {
        console.error('Error fetching matches for tournament:', matchesError);
        continue;
      }

      const totalMatches = matches?.length || 0;
      const totalWins = matches?.filter(m => m.winner_id).length || 0;

      // Count match types
      const matchTypes = {
        pins: matches?.filter(m => m.match_type === 'pin').length || 0,
        decisions: matches?.filter(m => m.match_type === 'decision').length || 0,
        tech_falls: matches?.filter(m => m.match_type === 'tech_fall').length || 0,
        major_decisions: matches?.filter(m => m.match_type === 'major_decision').length || 0
      };

      // Count participating teams (unique teams from wrestlers)
      const uniqueTeams = new Set<string>();
      matches?.forEach(match => {
        if (match.wrestler1) {
          uniqueTeams.add(extractTeamFromWrestlerName((match.wrestler1 as any).name));
        }
        if (match.wrestler2) {
          uniqueTeams.add(extractTeamFromWrestlerName((match.wrestler2 as any).name));
        }
      });

      tournamentStats.push({
        tournament_id: tournament.id,
        name: tournament.name,
        date: tournament.date,
        total_matches: totalMatches,
        total_wins: totalWins,
        participating_teams: uniqueTeams.size,
        match_types: matchTypes
      });
    }

    return tournamentStats;

  } catch (error) {
    console.error('Error getting tournaments with stats:', error);
    return [];
  }
}

/**
 * Get tournament details with match list
 */
export interface TournamentDetails extends TournamentStats {
  matches: Array<{
    id: string;
    wrestler1_name: string;
    wrestler2_name: string;
    winner_name: string | null;
    wrestler1_score: number;
    wrestler2_score: number;
    match_type: string;
    round: string;
  }>;
}

export async function getTournamentDetails(tournamentId: string): Promise<TournamentDetails | null> {
  try {
    if (!isSupabaseConfigured()) {
      console.warn('Supabase not configured, returning null');
      return null;
    }

    // Get tournament info
    const { data: tournament, error: tournamentError } = await supabase
      .from('tournaments')
      .select('id, name, date')
      .eq('id', tournamentId)
      .single();

    if (tournamentError || !tournament) {
      console.error('Error fetching tournament:', tournamentError);
      return null;
    }

    // Get all matches for this tournament with wrestler details
    const { data: matches, error: matchesError } = await supabase
      .from('matches')
      .select(`
        *,
        wrestler1:wrestlers!wrestler1_id(name),
        wrestler2:wrestlers!wrestler2_id(name),
        winner:wrestlers!winner_id(name)
      `)
      .eq('tournament_id', tournamentId)
      .order('created_at', { ascending: true });

    if (matchesError) {
      console.error('Error fetching matches for tournament:', matchesError);
      return null;
    }

    const totalMatches = matches?.length || 0;
    const totalWins = matches?.filter(m => m.winner_id).length || 0;

    // Count match types
    const matchTypes = {
      pins: matches?.filter(m => m.match_type === 'pin').length || 0,
      decisions: matches?.filter(m => m.match_type === 'decision').length || 0,
      tech_falls: matches?.filter(m => m.match_type === 'tech_fall').length || 0,
      major_decisions: matches?.filter(m => m.match_type === 'major_decision').length || 0
    };

    // Count participating teams
    const uniqueTeams = new Set<string>();
    matches?.forEach(match => {
      if (match.wrestler1) {
        uniqueTeams.add(extractTeamFromWrestlerName((match.wrestler1 as any).name));
      }
      if (match.wrestler2) {
        uniqueTeams.add(extractTeamFromWrestlerName((match.wrestler2 as any).name));
      }
    });

    // Format matches for display
    const formattedMatches = matches?.map(match => ({
      id: match.id,
      wrestler1_name: (match.wrestler1 as any)?.name || 'Unknown',
      wrestler2_name: (match.wrestler2 as any)?.name || 'Unknown',
      winner_name: (match.winner as any)?.name || null,
      wrestler1_score: match.wrestler1_score,
      wrestler2_score: match.wrestler2_score,
      match_type: match.match_type,
      round: match.round
    })) || [];

    return {
      tournament_id: tournament.id,
      name: tournament.name,
      date: tournament.date,
      total_matches: totalMatches,
      total_wins: totalWins,
      participating_teams: uniqueTeams.size,
      match_types: matchTypes,
      matches: formattedMatches
    };

  } catch (error) {
    console.error('Error getting tournament details:', error);
    return null;
  }
}

/**
 * Get unique teams for filtering
 */
export async function getUniqueTeams(): Promise<string[]> {
  try {
    const wrestlers = await getAllWrestlersWithStats();
    const teams = new Set<string>();
    
    wrestlers.forEach(wrestler => {
      teams.add(extractTeamFromWrestlerName(wrestler.name));
    });
    
    return Array.from(teams).sort();
  } catch (error) {
    console.error('Error getting unique teams:', error);
    return [];
  }
}

/**
 * Get unique weight classes for filtering
 */
export async function getUniqueWeightClasses(): Promise<number[]> {
  try {
    if (!isSupabaseConfigured()) {
      console.warn('Supabase not configured, returning empty array');
      return [];
    }

    const { data: wrestlers, error } = await supabase
      .from('wrestlers')
      .select('weight_class')
      .not('weight_class', 'is', null);

    if (error) {
      console.error('Error fetching weight classes:', error);
      return [];
    }

    const weightClasses = new Set<number>();
    wrestlers?.forEach(wrestler => {
      if (wrestler.weight_class) {
        weightClasses.add(wrestler.weight_class);
      }
    });

    return Array.from(weightClasses).sort((a, b) => a - b);
  } catch (error) {
    console.error('Error getting unique weight classes:', error);
    return [];
  }
}

/**
 * Get unique tournaments for filtering
 */
export async function getUniqueTournaments(): Promise<Array<{id: string, name: string}>> {
  try {
    if (!isSupabaseConfigured()) {
      console.warn('Supabase not configured, returning empty array');
      return [];
    }

    const { data: tournaments, error } = await supabase
      .from('tournaments')
      .select('id, name')
      .order('name');

    if (error) {
      console.error('Error fetching tournaments:', error);
      return [];
    }

    return tournaments || [];
  } catch (error) {
    console.error('Error getting unique tournaments:', error);
    return [];
  }
}

export async function getWinTypesData(wrestlerId?: string): Promise<WinTypeData[]> {
  try {
    if (!isSupabaseConfigured()) {
      console.warn('Supabase not configured, returning empty array');
      return [];
    }

    let query = supabase
      .from('matches')
      .select('match_type, winner_id, wrestler1_id, wrestler2_id')
      .not('winner_id', 'is', null);

    // Filter by wrestler if provided
    if (wrestlerId) {
      query = query
        .or(`wrestler1_id.eq.${wrestlerId},wrestler2_id.eq.${wrestlerId}`)
        .eq('winner_id', wrestlerId);
    }

    const { data: matches, error } = await query;

    if (error) {
      console.error('Error fetching win types data:', error);
      return [];
    }

    if (!matches || matches.length === 0) {
      return [];
    }

    // Count match types
    const typeCounts: { [key: string]: number } = {
      'Pin': 0,
      'Tech Fall': 0,
      'Major': 0,
      'Decision': 0
    };

    matches.forEach(match => {
      switch (match.match_type) {
        case 'pin':
          typeCounts['Pin']++;
          break;
        case 'tech_fall':
          typeCounts['Tech Fall']++;
          break;
        case 'major_decision':
          typeCounts['Major']++;
          break;
        case 'decision':
          typeCounts['Decision']++;
          break;
      }
    });

    return Object.entries(typeCounts).map(([type, count]) => ({
      type,
      count
    }));

  } catch (error) {
    console.error('Error getting win types data:', error);
    return [];
  }
}
