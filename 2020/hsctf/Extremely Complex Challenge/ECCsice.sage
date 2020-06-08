F = GF(404993569381)
x, y = G = (391109997465, 167359562362)
b = 54575449882
a = ((y^2 - x^3 - b) * inverse_mod(x, F.order())) % F.order()

E = EllipticCurve(F, [a, b])
G = E(G)
P = E((209038982304, 168517698208))
print(G.discrete_log(P))