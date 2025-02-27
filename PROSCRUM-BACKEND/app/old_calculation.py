
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
            elif new_hcp > -36:
                new_hcp -= 0.2
                
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