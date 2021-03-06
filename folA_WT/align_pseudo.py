with open("folA_WT.in",'r') as m:
    sequence=m.readline()

print('RNA='+sequence)

energy=open('summary_energy_pseudo.dat','w')
structure=open('summary_structure_pseudo.dat','w')


for i in range(1,len(sequence)+1):
    with open('segments_pseudo/sample_'+str(i)+'.in','w') as w:
        w.write(sequence[:i]+'\n')
    with open('segments_pseudo/sample_'+str(i)+'.mfe','r') as result:
        q=result.readlines()
        energy.write(q[14])
        structure.write(q[15])
energy.close()
structure.close()
