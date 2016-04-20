tall_buildings = {'building': [{'ES': 381, 'TD': 123, 'BK': 828, 'ST': 442},
                               {'TD': 222, 'ES': 509, 'ST': 1000, 'BK': 450}]}

# print(max(tall_buildings))
# print(max(tall_buildings.values()))
# #
# #print(max(tall_buildings.values(), key=lambda b: b[0]))
# print(tall_buildings.get('A', 'BK'))
#
# for i,v in enumerate(tall_buildings):
#     print(i,v)
#
#
# for i,v in iteritems(tall_buildings):
#     print(i,v)

b = tall_buildings['building']
for a in b:
    es, st, bk, td = a.items()
    print(es)
    print(st)
    print(bk)

