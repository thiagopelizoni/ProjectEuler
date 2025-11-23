import sys
from collections import defaultdict
import numpy as np
from tqdm import tqdm

def main():
    # Problem parameters
    N = 40
    
    # The state is represented by (boundary_gaps, internal_gaps)
    # boundary_gaps: tuple of sorted gap sizes adjacent to the boundaries (Wall).
    # internal_gaps: tuple of sorted gap sizes between segments.
    # Value: numpy array representing the probability distribution of the Max Segments (M).
    # index i stores P(M = i).
    
    # Max segments can't exceed N/2 + 1 (approx 21 for N=40). Size 42 is plenty safe.
    dist_size = N + 2
    
    # Dictionary to store current states and their probability distributions
    # key: (boundary_tuple, internal_tuple)
    # value: np.array of shape (dist_size,)
    current_states = defaultdict(lambda: np.zeros(dist_size, dtype=float))
    
    # --- Initialization (Step 1: 1 piece placed) ---
    # There are N positions to place the first piece.
    # Each position p (1-based) leaves gaps of size p-1 and N-p.
    # Both gaps are boundary gaps initially.
    # Current segments = 1. Max M = 1.
    init_prob = 1.0 / N
    for p in range(1, N + 1):
        b_gaps = []
        if p - 1 > 0:
            b_gaps.append(p - 1)
        if N - p > 0:
            b_gaps.append(N - p)
        b_gaps.sort()
        
        state = (tuple(b_gaps), ())
        current_states[state][1] += init_prob

    # --- Dynamic Programming (Steps 2 to N) ---
    # We iterate through the number of pieces placed.
    # Loop runs for k=1 to N-1 (transitions to k+1 pieces).
    for _ in tqdm(range(1, N), desc="Processing", file=sys.stderr):
        next_states = defaultdict(lambda: np.zeros(dist_size, dtype=float))
        
        for (b_gaps, i_gaps), dist in current_states.items():
            # Total empty slots (R)
            R = sum(b_gaps) + sum(i_gaps)
            if R == 0:
                continue
                
            # Helper to process a transition
            # new_b, new_i: lists of gap sizes
            # prob_weight: probability of this specific transition occurring
            def add_transition(new_b, new_i, prob_weight):
                # Canonicalize state
                t_new_b = tuple(sorted([x for x in new_b if x > 0]))
                t_new_i = tuple(sorted([x for x in new_i if x > 0]))
                
                # Calculate new segment count
                # Segments = Internal Gaps + 1
                new_seg_count = len(t_new_i) + 1
                
                # Calculate contribution to the next state's distribution
                # We take the current distribution 'dist' and scale it by 'prob_weight'.
                # Then, we apply the logic M_new = max(M_old, new_seg_count).
                
                contrib = dist * prob_weight
                
                # Shift probability mass where max_segments < new_seg_count
                # All probability mass for M < new_seg_count moves to M = new_seg_count
                mass_to_move = np.sum(contrib[:new_seg_count])
                
                target = next_states[(t_new_b, t_new_i)]
                
                # Add mass that was already >= new_seg_count
                target[new_seg_count:] += contrib[new_seg_count:]
                
                # Add moved mass
                target[new_seg_count] += mass_to_move

            # Group gaps by size for efficiency
            b_counts = {}
            for g in b_gaps: b_counts[g] = b_counts.get(g, 0) + 1
            
            i_counts = {}
            for g in i_gaps: i_counts[g] = i_counts.get(g, 0) + 1
            
            # 1. Transitions from BOUNDARY Gaps
            for g, count in b_counts.items():
                # A boundary gap of size g has g slots.
                # Slot g is adjacent to an existing segment (Extension).
                # Slots 1 to g-1 are not adjacent (New Segment).
                
                # Case A: Extension (1 slot per gap)
                # Prob = (count * 1) / R
                prob_ext = count / R
                
                nb = list(b_gaps)
                nb.remove(g)
                if g - 1 > 0:
                    nb.append(g - 1)
                add_transition(nb, list(i_gaps), prob_ext)
                
                # Case B: New Segment (g-1 slots per gap)
                # Only possible if g > 1
                if g > 1:
                    # Prob of picking a specific slot x (distance from wall) in ANY of these gaps
                    # is count / R.
                    # We iterate x from 1 to g-1.
                    base_prob = count / R
                    
                    for x in range(1, g):
                        # Slot x filled.
                        # Gap 'left' (Wall side) is x-1 (Boundary).
                        # Gap 'right' (Segment side) is g-x (Internal).
                        
                        nb = list(b_gaps)
                        nb.remove(g)
                        if x - 1 > 0:
                            nb.append(x - 1)
                            
                        ni = list(i_gaps)
                        if g - x > 0:
                            ni.append(g - x)
                            
                        add_transition(nb, ni, base_prob)

            # 2. Transitions from INTERNAL Gaps
            for g, count in i_counts.items():
                # An internal gap of size g has g slots.
                # Slots 1 and g are adjacent to segments.
                # If g=1, the single slot is adjacent to BOTH (Merge).
                # If g>1, slots 1 and g are extensions. Slots 2..g-1 are New Segments.
                
                if g == 1:
                    # Merge (1 slot per gap)
                    prob_merge = count / R
                    
                    ni = list(i_gaps)
                    ni.remove(g)
                    add_transition(list(b_gaps), ni, prob_merge)
                    
                else:
                    # Case A: Extension (2 slots per gap)
                    prob_ext = (2.0 * count) / R
                    
                    ni = list(i_gaps)
                    ni.remove(g)
                    ni.append(g - 1)
                    add_transition(list(b_gaps), ni, prob_ext)
                    
                    # Case B: New Segment (g-2 slots per gap)
                    # Slots 2 to g-1
                    if g > 2:
                        base_prob = count / R
                        for x in range(2, g):
                            # Slot x filled.
                            # Splits g into x-1 and g-x (both Internal)
                            ni = list(i_gaps)
                            ni.remove(g)
                            ni.append(x - 1)
                            ni.append(g - x)
                            
                            add_transition(list(b_gaps), ni, base_prob)
                            
        current_states = next_states

    # --- Final Calculation ---
    # Aggregate distributions from all final states
    final_distribution = np.zeros(dist_size, dtype=float)
    for dist in current_states.values():
        final_distribution += dist
        
    # Calculate Expected Value
    expected_max_segments = 0.0
    for m, prob in enumerate(final_distribution):
        expected_max_segments += m * prob
        
    print(f"{expected_max_segments:.6f}")

if __name__ == "__main__":
    main()