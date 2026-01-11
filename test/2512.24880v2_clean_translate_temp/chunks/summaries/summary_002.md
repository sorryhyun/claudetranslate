## Chunk 2 Summary

### Brief Summary
This section discusses macro-design approaches in neural networks, tracing the evolution from ResNet to recent width-expansion methods like Hyper-Connections (HC), then introduces the foundational HC formulation and its mathematical framework. The chunk identifies two critical limitations of HC—numerical instability in deep layers and excessive memory access overhead—which motivate the proposed manifold-constrained solution.

### Key Terms in This Section
- **Hyper-Connections (HC)**: An architecture design that expands the residual stream width by a factor n, introducing learnable mappings (H_l^pre, H_l^post, H_l^res) to manage feature interaction
- **Macro Design**: The global topology of neural network architecture, controlling features like connectivity and depth patterns
- **Residual Stream**: The expanded feature pathway in HC, represented as an n-stream matrix structure that broadens information capacity
- **Identity Mapping**: Fundamental property in residual networks ensuring stable signal flow; HC variants attempt to preserve this while enabling feature interaction
- **Numerical Instability**: Problem where composite residual mappings cause gradient explosion/vanishing, with Amax Gain Magnitude metrics showing peaks of 3000 instead of ideal value of 1
- **Doubly Stochastic Matrix**: A mathematical construct with non-negative entries where rows and columns sum to 1, proposed as the constraint manifold for stable residual mappings
- **Birkhoff Polytope**: The geometric space of doubly stochastic matrices, forming a convex hull of permutation matrices
- **Memory Wall**: Hardware bottleneck where memory access (I/O) costs dominate computation, often overlooked but decisive for runtime efficiency
- **RMSNorm**: Root Mean Square Normalization, applied in the HC mapping computation to normalize inputs

### Connections
- **Continues from**: Chunk 1 established the introduction and motivation for efficient neural network scaling; this chunk builds on that by examining existing approaches (ResNet, DenseNet, DLA) and their evolution toward width-expansion methods
- **Sets up**: The identified problems (numerical instability, memory overhead) directly motivate the proposed manifold-constrained HC approach (mHC) discussed in the following sections; the mathematical framework here underpins the solution methodology

### Translation Notes
- Mathematical notation and equations (5), (6) must remain unchanged; only surrounding explanatory text is translated
- The composite mapping notation [∏ from i=1 to L H_l^res] is critical for understanding instability analysis—preserve notation exactly
- "Memory wall" is a technical term; verify Korean IT terminology uses established convention (메모리 월)
- The progression from HC's problems to the proposed solution is central to comprehension; ensure causal language (consequence, result, therefore) is translated with appropriate Korean particles
- Table 1 and Table 2 show empirical results; numerical values and column headers must be preserved with only descriptive text translated
- Figure references (Fig. 2, Fig. 3) appear multiple times—maintain consistent Korean reference style (그림 2, 그림 3)
- The shift from discussing HC limitations (3.1-3.2) to introducing the manifold constraint solution marks a key rhetorical pivot that should be evident in translation
