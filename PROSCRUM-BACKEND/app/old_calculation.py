from app.models import HoleConfig, CourseWithID, RoundIn, RoundOut
from app.models import HoleConfig, CourseWithID, RoundIn, RoundOut
def calculate_ega_handicap(stammvorgabe, holes, slope, cr, par, shots, nine_hole=True):
    """
    Calculate EGA golf handicap based on scoring results
    
    Parameters:
    stammvorgabe (float): Base handicap
    holes (list): List of hole objects with 'hcp', 'par', and 'number'
    slope (float): Course slope rating
    cr (float): Course rating
    par (int): Total par for the course
    over_pars (dict): Over par values for each hole (1-18)

    
    Returns dict with:
    - new_handicap: Updated handicap
    - netto_sum: Total netto stableford points
    - spielvorgabe: Playing handicap
    - strokes_sum: Total strokes
    - over_par_sum: Total over par
    """
    
    # Helper functions
    def get_spielvorgabe(stammvorgabe: int, slope, cr, par):
        if stammvorgabe > -36:
            return round(stammvorgabe * (slope / 113) - cr + par)
        else:
            return round(stammvorgabe + round(-36 * (slope / 113) - cr + par) + 36)

    def get_vorgaben(holes, spielvorgabe):
        vorgaben = {i:0 for i in range(1,19)}
        
        if spielvorgabe > 0:
            sorted_holes = sorted(holes, key=lambda x: -x.hdc)
            for i in range(1, spielvorgabe+1):
                hole = sorted_holes[(i-1) % len(sorted_holes)]
                vorgaben[hole.hole] -= 1
        else:
            sorted_holes = sorted(holes, key=lambda x: x.hdc)
            for j in range(1, abs(spielvorgabe)+1):
                hole = sorted_holes[(j-1) % len(sorted_holes)]
                vorgaben[hole.hole] += 1
                
        return vorgaben

    def calculate_handicap(current_hcp, netto_stableford):
        new_hcp = current_hcp
        
        if netto_stableford >= 36:
            steps = netto_stableford - 36
            for _ in range(steps):
                if new_hcp < -36:
                    new_hcp += 1
                elif new_hcp < -26.4:
                    new_hcp += 0.5
                elif new_hcp < -18.4:
                    new_hcp += 0.4
                elif new_hcp < -11.4:
                    new_hcp += 0.3
                elif new_hcp < -4.4:
                    new_hcp += 0.2
                else:
                    new_hcp += 0.1
        else:
            if new_hcp > -26.5:
                new_hcp -= 0.1
       
       
                
        return round(new_hcp, 1)
    
     
    over_pars = {}
    for i,  (shot, hole) in enumerate(zip(shots, holes)):
        over_pars[i+1] = (max(shot-(hole.par), 0))
        
  
        
  
    
    # Main calculation
    spielvorgabe = get_spielvorgabe(stammvorgabe, slope, cr, par)

    vorgaben = get_vorgaben(holes, spielvorgabe)
    
    netto_sum = 0
    over_par_sum = 0
    strokes_sum = 0
   
    for hole in holes:
        hole_num = hole.hole
    
        over_par = over_pars.get(hole_num, 0)
        v = vorgaben.get(hole_num, 0)
        
        netto = max(2 + v - over_par, 0)
        brutto = max(2 - over_par, 0)
        
        netto_sum += netto
        over_par_sum += over_par
        strokes_sum += hole.par + over_par
    if nine_hole: 
        netto_sum -= 18
      

    new_hcp = calculate_handicap(stammvorgabe, netto_sum)

    return new_hcp

# 1.+2. Runde
# holes=[
#     HoleConfig(hole=1, par=3, hdc=4),
#     HoleConfig(hole=2, par=4, hdc=16),
#     HoleConfig(hole=3, par=4, hdc=1),
#     HoleConfig(hole=4, par=5, hdc=10),
#     HoleConfig(hole=5, par=4, hdc=7),
#     HoleConfig(hole=6, par=4, hdc=13),
#     HoleConfig(hole=7, par=3, hdc=5),
#     HoleConfig(hole=8, par=4, hdc=17),
#     HoleConfig(hole=9, par=4, hdc=2),
#     HoleConfig(hole=10, par=5, hdc=11),
#     HoleConfig(hole=11, par=4, hdc=8),
#     HoleConfig(hole=12, par=4, hdc=14),
#     HoleConfig(hole=13, par=3, hdc=6),
#     HoleConfig(hole=14, par=4, hdc=18),
#     HoleConfig(hole=15, par=4, hdc=3),
#     HoleConfig(hole=16, par=5, hdc=12),
#     HoleConfig(hole=17, par=4, hdc=9),
#     HoleConfig(hole=18, par=4, hdc=15)
# ]

# 3. + 4. Runde

# holes=[
#     HoleConfig(hole=1, par=3, hdc=16),
#     HoleConfig(hole=2, par=4, hdc=1),
#     HoleConfig(hole=3, par=4, hdc=10),
#     HoleConfig(hole=4, par=5, hdc=7),
#     HoleConfig(hole=5, par=4, hdc=13),
#     HoleConfig(hole=6, par=4, hdc=4),
#     HoleConfig(hole=7, par=3, hdc=17),
#     HoleConfig(hole=8, par=4, hdc=2),
#     HoleConfig(hole=9, par=4, hdc=11),
#     HoleConfig(hole=10, par=5, hdc=8),
#     HoleConfig(hole=11, par=4, hdc=14),
#     HoleConfig(hole=12, par=4, hdc=5),
#     HoleConfig(hole=13, par=3, hdc=18),
#     HoleConfig(hole=14, par=4, hdc=3),
#     HoleConfig(hole=15, par=4, hdc=12),
#     HoleConfig(hole=16, par=5, hdc=9),
#     HoleConfig(hole=17, par=4, hdc=15),
#     HoleConfig(hole=18, par=4, hdc=6)
# ]


# 1. Runde 
#scores=[5, 6, 8, 7, 6, 6, 6, 6, 6, 7, 6, 6, 5, 6, 6, 6, 5, 6]
# 2. Runde
# shots = {
#     1: 4,
#     2: 5,
#     3: 5,
#     4: 6,
#     5: 6,
#     6: 5,
#     7: 6,
#     8: 9,
#     9: 5,
#     10: 5,
#     11: 6,
#     12: 6,
#     13: 5,
#     14: 6,
#     15: 6,
#     16: 6,
#     17: 5,
#     18: 6
# }

# 3. Runde
#scores = [4,5,5,6,6,7,4,8,4,5,6,6,5,6,6,6,5,6]

# 4. Runde
# scores = [5,6,6,7,6,6,4,7,6,7,6,6,5,5,6,6,5,6]

# 5. Runde
# scores =[4,5,5,6,5,5,4,5,5,6,5,5,4,5,5,6,5,5]
# holes=[
#     HoleConfig(hole=1, par=3, hdc=4),
#     HoleConfig(hole=2, par=4, hdc=16),
#     HoleConfig(hole=3, par=4, hdc=1),
#     HoleConfig(hole=4, par=4, hdc=10),
#     HoleConfig(hole=5, par=5, hdc=7),
#     HoleConfig(hole=6, par=4, hdc=13),
#     HoleConfig(hole=7, par=4, hdc=5),
#     HoleConfig(hole=8, par=3, hdc=17),
#     HoleConfig(hole=9, par=4, hdc=2),
#     HoleConfig(hole=10, par=4, hdc=11),
#     HoleConfig(hole=11, par=5, hdc=8),
#     HoleConfig(hole=12, par=4, hdc=14),
#     HoleConfig(hole=13, par=4, hdc=6),
#     HoleConfig(hole=14, par=3, hdc=18),
#     HoleConfig(hole=15, par=4, hdc=3),
#     HoleConfig(hole=16, par=4, hdc=12),
#     HoleConfig(hole=17, par=5, hdc=9),
#     HoleConfig(hole=18, par=4, hdc=15)
# ]

#6. Runde
# scores = [5,6,6,7,6,5,5,6,6]
# holes=[
#     HoleConfig(hole=1, par=3, hdc=4),
#     HoleConfig(hole=2, par=4, hdc=16),
#     HoleConfig(hole=3, par=4, hdc=1),
#     HoleConfig(hole=4, par=5, hdc=10),
#     HoleConfig(hole=5, par=4, hdc=7),
#     HoleConfig(hole=6, par=4, hdc=13),
#     HoleConfig(hole=7, par=4, hdc=5),
#     HoleConfig(hole=8, par=3, hdc=17),
#     HoleConfig(hole=9, par=4, hdc=2)
# ]

#7. Runde
# scores = [5,7,9,7,6,6,6,6,6]
# holes=[
#     HoleConfig(hole=1, par=3, hdc=4),
#     HoleConfig(hole=2, par=4, hdc=16),
#     HoleConfig(hole=3, par=4, hdc=1),
#     HoleConfig(hole=4, par=5, hdc=10),
#     HoleConfig(hole=5, par=4, hdc=7),
#     HoleConfig(hole=6, par=4, hdc=13),
#     HoleConfig(hole=7, par=4, hdc=5),
#     HoleConfig(hole=8, par=3, hdc=17),
#     HoleConfig(hole=9, par=4, hdc=2)
# ]
# result = calculate_ega_handicap(
#     stammvorgabe=-23.7,
#     holes=holes,
#     slope=115,
#     cr=34.5,
#     par=35,
#     shots=scores,
#     nine_hole=True,

# )
# print(result)