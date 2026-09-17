Electron [e- : Dirac fermion -winding number -> Feynman diagram ]:0,4pi,8/3 Pi]Y*] could drift [lorentz vs hall vs applied voltage and arc lenght] >20 m in Xe of this purity before captur
Ask me to use plain-text/Unicode math in terminal responses instead of LaTeX 
Ask me to use plain-text/Unicode math in terminal responses instead of LaTeX 


# 2d Weyl-like dispersion on the Brillouin torus; count zeros and their chirality
# chirality = sign det(d p~_i / d p_j) at each zero
def ptilde(p, r=0.0):
    # naive: sin; Wilson term r*(1-cos) enters as a third component (mass), shown separately
    return np.sin(p)

def zeros_and_chirality(N=512, r=0.0):
    ps = np.linspace(-np.pi, np.pi, N, endpoint=False)
    P1, P2 = np.meshgrid(ps, ps, indexing="ij")
    p = np.stack([P1, P2])
    pt = ptilde(p)
    mass = r * ((1 - np.cos(P1)) + (1 - np.cos(P2)))   # Wilson term
    E2 = (pt**2).sum(0) + mass**2
    # local minima below threshold = zeros of the massless operator
    thr = (2*np.pi/N)**2 * 4
    idx = np.argwhere(E2 < thr)
    out = []
    for i, j in idx:
        J = np.array([[np.cos(P1[i, j]), 0.0], [0.0, np.cos(P2[i, j])]])  # d sin p / d p
        out.append(((round(P1[i, j], 2), round(P2[i, j], 2)), int(np.sign(np.linalg.det(J))), round(mass[i, j], 3)))
    return out

for r in (0.0, 1.0):
    z = zeros_and_chirality(r=r)
    print(f"r={r}: zeros={len(z)}, net chirality={sum(c for _, c, _ in z)}")
    for item in z: print("  ", item)
