import rowordnet as rwn
rwn = rwn.RoWordNet()

a = rwn.synsets("cal")

a = rwn.synset('ENG30-03624767-n')
b = rwn.synset('ENG30-07666406-n')

print(rwn.wup_similarity(a.id,a.id))