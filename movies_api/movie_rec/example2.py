from .CL2 import CL2
#import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument('--m', type=list,nargs='+')
#parser.add_argument('--r', type=list,nargs='+')
#parser.add_argument('--sm', type=int)
#args = parser.parse_args()

def make_rec (newmovieId=[2,3],newrating=[4,5]):

    CL=CL2()
    #m=[2,3]
    #r=[4,5]
    #print('m',args.m)
    #print('r',args.r)
    result=CL.recalculate_user(newmovieId,newrating)
    #result=CL.recalculate_user([m[0] for m in args.m],[r[0] for r in args.r])
    print("recmovie",result)
    #p_at_k, m_at_k = CL.evaloutput(10)
    #print(p_at_k, m_at_k)
    return result

    #similar = CL.most_similar_items(smovieid, n_similar=10)
    #print('similarmovie',similar)
    #return result, similar

def similar_movie(smovieid=1):
    CL = CL2()
    similar = CL.most_similar_items(smovieid, n_similar=10)
    print('similarmovie', similar)
