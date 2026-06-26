from model.modello import Model

mm = Model()
mm.buildGraph(1999, "CO")
print(len(mm._sighting))
n,a = mm.getGraphDetails()
print(n,a)
dim,largest = mm.getInfoConnessa()
print(f"num comp connesse = {dim}")
print("componente connessa più grande:")
for n in largest:
    print(f"{n.id}-{n.city}-{n.datetime}")