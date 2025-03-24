import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def plot_region(c=0.05, k=10, n=200):
    """
    Plot the region in the unit square [0,1]x[0,1] where:
        1) L*S < c
        2) 1/k < S/L < k
    using a grid of size n x n.
    """
    # Create a grid of L, S values in [0,1] x [0,1]
    Lvals = np.linspace(0, 1, n)
    Svals = np.linspace(0, 1, n)
    L, S = np.meshgrid(Lvals, Svals)
    
    # 1) Condition: L*S < c
    region1 = (L * S < c)
    
    # 2) Condition: 1/k < S/L < k
    #    We'll handle L=0 carefully. If L=0 and S>0, ratio => ∞, which won't be < k unless k is huge.
    #    We can define ratio = 0 if L=0, S=0 => ratio is undefined, but that's just a single point.
    ratio = np.zeros_like(L)
    mask_nonzero = (L != 0)
    ratio[mask_nonzero] = S[mask_nonzero] / L[mask_nonzero]
    region2 = (ratio > 1/k) & (ratio < k)
    
    # Intersection of both conditions
    region = region1 & region2

    # Make a single figure
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_title(f"Region where L*S < {c} and 1/{k} < S/L < {k}")
    
    # Show the intersection region as a shaded mask
    ax.pcolormesh(L, S, region, shading='auto')
    
    # Plot boundary curves:
    # S = c/L (hyperbola), ignoring L=0 to avoid division by zero
    # S = k*L  and S = (1/k)*L (straight lines)
    l_line = np.linspace(1e-9, 1, 400)  # Avoid 0 for hyperbola
    s_hyp = c / l_line
    ax.plot(l_line, s_hyp, label="S = c/L")
    s_line_up = k * l_line
    s_line_dn = (1/k) * l_line
    ax.plot(l_line, s_line_up, label="S = k·L")
    ax.plot(l_line, s_line_dn, label="S = (1/k)·L")
    
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])
    ax.set_xlabel("L")
    ax.set_ylabel("S")
    ax.legend()
    
    return fig

def main():
    st.title("Visualizing L*S < c and 1/k < S/L < k in the Unit Square")

    # Create sliders / inputs for c, k, and n
    c = st.slider("c (threshold for L*S < c)", 
                  min_value=1e-8, max_value=0.2, value=1e-3, step=1e-8, format="%.8f")
    
    k = st.slider("k (ratio bound: 1/k < S/L < k)", 
                  min_value=1.0, max_value=1e6, value=10.0, step=100.0, format="%.2f")
    
    n = st.slider("Grid resolution n", 
                  min_value=50, max_value=500, value=200, step=50)
    
    fig = plot_region(c, k, n)
    st.pyplot(fig)

if __name__ == "__main__":
    main()