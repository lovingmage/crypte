def QueryParsing_GroupBy(Q):
    """
    Take query of the following form
    A1 - attribute to be grouped on
    A2,...,An - additional attributes to perform aggregation on
    + aggregation operation is sum
    | aggregation operation is count
    - aggregation operation is avg
    <> encodes prior filter condition
    t - threshold for count for A1
    in <rs_i,re_i> and parse it
    *,A1,t,0,e/:;ec;A2,+,e1;A4,k,e2/A3,v1,v2*
    y,A1,t,1,e/*/A2,v1,v2*
    *,A1,t,0,e/-;0;A2,$,e1/*
    :para Q: Query string of the form <attr_i
    :return Attr_GB - A1 as defined
    :return e - If A1 is counted 
    :return t - count threshold as defined (having clause)
    :return flag - 1 when I want a count of Attr_GB satisfying t
    :return flag2 - direction of threshold 
    :return count_sym - If I want to display noisy counts as well
    :return ec - to generate noisy counts for A1
    :return Attr_Aggr - list of attributes for aggregation A2,...,An
    :return Aggr - list of aggregation operators
    :return e_Aggr- list of epsilons for Aggr operations
    :return FilterQ - Where clause 
    """
    Attr_Aggr=[]
    Aggr=[]
    e_Aggr=[]
    count_sym='-'
    ec=1
    L=Q.split('/')
    l1=L[0].split(',')
    e=float(l1[4])
    Attr_GB=int(l1[1])
    t=int(l1[2])
    FilterQ=L[2]
    flag2=int(l1[3])
    if(l1[0]=='*'):
      flag=0
      l2=L[1].split('p')
      count_sym=l2[0]
      ec=float(l2[1])
      Attr_Aggr=[]
      Aggr=[]
      e_Aggr=[]
      for i in range(2,len(l2)):
         h=l2[i].split(',')
         Attr_Aggr.append(int(h[0]))
         Aggr.append(h[1])
         e_Aggr.append(float(h[2]))
    else:
       flag=1
        

    
    return Attr_GB,t,flag,flag2,e,count_sym,ec,Attr_Aggr,Aggr,e_Aggr,FilterQ




def QueryParsing(Q):
    """
    Take Conjunctive queries of the form A_i in <rs_i,re_i> and parse it
    :para Q: Query string of the form <attr_i,rs_i,re_i>
    :return Attr - list of attributes in conjunction in Q
    :return Rstart - list of range start for the attributes
    :return Rend - list of range end for the attributes
    """
    flag_range=0
    L=Q.split('*')
    Attr=[]
    Rstart=[]
    Rend=[]
    for i in range(len(L)):
        t=L[i].split(',')
        if(t==['']):
          print("")
        else:
            Attr.append(int(t[0]))
            Rstart.append(int(t[1]))
            Rend.append(int(t[2]))
    

    return Attr,Rstart,Rend   

