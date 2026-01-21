/**
 * Unit tests for wrestling analytics functions - MVP version
 * Tests simple stats: Wins, Losses, Win %, Match type counts
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { 
  calculateWrestlerStats, 
  getAllWrestlersWithStats,
  getWrestlerMatches,
  type WrestlerStats
} from '../analytics';
import { supabase } from '../supabase';

// Mock the supabase client
vi.mock('../supabase', () => ({
  supabase: {
    from: vi.fn(() => ({
      select: vi.fn(() => ({
        eq: vi.fn(() => ({
          single: vi.fn(),
          order: vi.fn(() => ({
            limit: vi.fn()
          }))
        })),
        or: vi.fn(() => ({
          order: vi.fn()
        })),
        order: vi.fn()
      }))
    }))
  }
}));

const mockSupabase = supabase as any;

describe('Wrestling Analytics MVP', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('calculateWrestlerStats', () => {
    it('should calculate basic stats for wrestler with matches', async () => {
      // Mock wrestler data
      const mockWrestler = {
        id: 'wrestler-1',
        name: 'John Doe',
        weight_class: 160
      };

      // Mock matches data
      const mockMatches = [
        {
          id: 'match-1',
          wrestler1_id: 'wrestler-1',
          wrestler2_id: 'wrestler-2',
          winner_id: 'wrestler-1',
          wrestler1_score: 8,
          wrestler2_score: 3,
          match_type: 'decision'
        },
        {
          id: 'match-2',
          wrestler1_id: 'wrestler-3',
          wrestler2_id: 'wrestler-1',
          winner_id: 'wrestler-1',
          wrestler1_score: 2,
          wrestler2_score: 12,
          match_type: 'pin'
        },
        {
          id: 'match-3',
          wrestler1_id: 'wrestler-1',
          wrestler2_id: 'wrestler-4',
          winner_id: 'wrestler-4',
          wrestler1_score: 4,
          wrestler2_score: 7,
          match_type: 'decision'
        }
      ];

      // Setup mocks
      mockSupabase.from.mockReturnValueOnce({
        select: vi.fn().mockReturnValue({
          eq: vi.fn().mockReturnValue({
            single: vi.fn().mockResolvedValue({ data: mockWrestler, error: null })
          })
        })
      }).mockReturnValueOnce({
        select: vi.fn().mockReturnValue({
          or: vi.fn().mockResolvedValue({ data: mockMatches, error: null })
        })
      });

      const result = await calculateWrestlerStats('wrestler-1');

      expect(result).toEqual({
        wrestler_id: 'wrestler-1',
        name: 'John Doe',
        weight_class: 160,
        wins: 2,
        losses: 1,
        total_matches: 3,
        win_percentage: 67, // Rounded to whole number
        pins: 1,
        decisions: 1,
        tech_falls: 0,
        major_decisions: 0
      });
    });

    it('should return empty stats for wrestler with no matches', async () => {
      const mockWrestler = {
        id: 'wrestler-1',
        name: 'John Doe',
        weight_class: 160
      };

      mockSupabase.from.mockReturnValueOnce({
        select: vi.fn().mockReturnValue({
          eq: vi.fn().mockReturnValue({
            single: vi.fn().mockResolvedValue({ data: mockWrestler, error: null })
          })
        })
      }).mockReturnValueOnce({
        select: vi.fn().mockReturnValue({
          or: vi.fn().mockResolvedValue({ data: [], error: null })
        })
      });

      const result = await calculateWrestlerStats('wrestler-1');

      expect(result).toEqual({
        wrestler_id: 'wrestler-1',
        name: 'John Doe',
        weight_class: 160,
        wins: 0,
        losses: 0,
        total_matches: 0,
        win_percentage: 0,
        pins: 0,
        decisions: 0,
        tech_falls: 0,
        major_decisions: 0
      });
    });

    it('should return null for non-existent wrestler', async () => {
      mockSupabase.from.mockReturnValue({
        select: vi.fn().mockReturnValue({
          eq: vi.fn().mockReturnValue({
            single: vi.fn().mockResolvedValue({ data: null, error: { message: 'Not found' } })
          })
        })
      });

      const result = await calculateWrestlerStats('non-existent');
      expect(result).toBeNull();
    });
  });

  describe('getAllWrestlersWithStats', () => {
    it('should return empty array when no wrestlers found', async () => {
      mockSupabase.from.mockReturnValue({
        select: vi.fn().mockReturnValue({
          order: vi.fn().mockResolvedValue({ data: [], error: null })
        })
      });

      const result = await getAllWrestlersWithStats();
      expect(result).toEqual([]);
    });
  });
});