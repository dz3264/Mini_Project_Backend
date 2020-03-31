from .CL_norating import CL2

def make_norating_rec (newmovieId=[2,3],newrating=[4,5]):

    CL = CL2()
    result = CL.recalculate_user(newmovieId, newrating)
    print("recmovie", result)
    return result
    #p_at_k, m_at_k = CL.evaloutput(10)
    #print(p_at_k, m_at_k)
