
nanpa_sitelen=133
k = 12
# sitelen 0... (k-1)*(k-1)-1 li lon leko
# sitelen (k-1)*(k-1)... (k-1)*(k-1)+(k-1)-1 li lon ma suli
  # sitelen (k-1)*(k-1)+j li tawa linja pi ante j
# sitelen (k-1)*(k-1)+k-1 li tawa linja supa

assert(k*(k-1)+1 == nanpa_sitelen)

lipu= []

# nanpa wan la, linja supa
for i in range(k-1):
  lipu.append([(k-1)*(k-1)+k-1]+[i*(k-1)+l for l in range(k-1)])

# nanpa tu la, linja pi supa ala
for j in range(k-1):
  for i in range(k-1):
    lipu.append([(k-1)*(k-1)+j]+[(l*(k-1))+(i+j*l)%(k-1) for l in range(k-1)])

lipu.append([(k-1)*(k-1)+l for l in range(k)])
  
assert(all(len(l)==k for l in lipu))

for i1 in range(len(lipu)):
  for i2 in range(i1+1, len(lipu)):
    l1= lipu[i1]; l2= lipu[i2]
    
    if len(set(l1).intersection(set(l2)))!=1:
      print(l1,l2)
      print(set(l1).intersection(set(l2)))
      assert(False)

ale= set()
for l in lipu:
  ale= ale.union(set(l))
assert(len(ale)== nanpa_sitelen)

import sitelen

for i in range(nanpa_sitelen):
  sitelen.o_sitelen_e_lipu(lipu[i], i)