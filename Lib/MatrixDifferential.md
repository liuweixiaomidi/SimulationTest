<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

## 神经网络中的矩阵计算

为了使得推导公式时，做到所写即所码，结合编程时的习惯，重新定义部分已有运算、以及提出新的运算符。

作者：向英杰
日期：2023年6月1日

[toc]

---

### 矩阵偏导的定义

> 1. $A,B$ 是两个矩阵，$\exists\; f(\cdot),\; A = f(B)$。
> 2. $\exists\; n,m\in\mathbb{Z}^+,\; \forall B\in\mathbb{R}^{n\times m},\; \frac{\partial A}{\partial B}\in\mathbb{R}^{n\times m}$。
> 3. $A_{i,j}$ 表示矩阵 $A$ 第 $i$ 行、第 $j$ 列的元素，$ \forall\; i,j,\; (\frac{\partial A}{\partial B})_{ij} = \sum_{a\in A}\frac{\partial a}{\partial B_{ij}}$

当同时满足上述三个条件时，我们认为 $  \frac{\partial A}{\partial B}$ 是矩阵偏导，有了偏导，剩下想怎么玩都行。:)

### 特殊符号与运算

> 1. 粗体的 $\mathbf{e}$ 是单位列向量，$\mathbf{e}^T$ 是单位行向量，维度自适应。
> 2. 符号 $\mathcal{I}(A)$ 表示一个元素全为 1 的矩阵，维度与矩阵 $A$ 相同，即 $\mathcal{I}(A) = \mathbf{e}\cdot\mathbf{e}^T $。
> 3. 符号 $\dot{\times}$ 表示矩阵左乘，即 $A\cdot B = B \dot{\times}A$。
> 4. 符号 $:$ 表示哈达玛乘积，即对应元素相乘。
> 5. 符号 $:n$ 表示哈达玛幂，即 $A^{:3} = A:A:A$。
> 6. 符号 $\mathfrak{T}$ 是全转置运算，即 $A \cdot B \cdot C \cdot \mathfrak{T} = (A \cdot B \cdot C)^T $。

可能此时此刻你还没法明白这些符号是在搞什么鬼，但是在编程时，也许它们会救你一命，先暂时记住即可。

### 严格推论与魔改

1. 根据先前对矩阵偏导的定义，非常显然地有以下结论，不做证明：
> $$  \frac{\partial A}{\partial A} = \mathcal{I}(A);\;\; \frac{\partial A}{\partial A^T} = \mathcal{I}(A)^T;\;\; \frac{\partial A^{:n}}{\partial A} = n\cdot A^{:n-1}; $$

2. 加减法：
> $$  \frac{\partial (f(A)\pm g(A))}{\partial A} = \frac{\partial f(A)}{\partial A} \pm \frac{\partial g(A)}{\partial A} $$

3. 哈达玛乘积：
> $$  \frac{\partial (f(A):g(A))}{\partial A} = \frac{\partial f(A)}{\partial A} : g(A) + \frac{\partial g(A)}{\partial A} : f(A) $$

4. 矩阵乘积：
> $$  \frac{\partial AB}{\partial A} = \mathcal{I}(AB)\cdot B^T;\;\; \frac{\partial AB}{\partial B} = \mathcal{I}(AB)\dot{\times} A^T;  $$

5. 现在，我们需要证明一个重要的法则，即偏导中的链式法则：

> 假设存在这样的关系 $A = f(B),\; B = g(C)$，根据矩阵偏导的定义有：$$ \Big(\frac{\partial A}{\partial C}\Big)_j = \sum_{a\in A}\frac{\partial a}{\partial C_j} = \sum_{a\in A}\sum_{b\in B}\frac{\partial a}{\partial b}\cdot\frac{\partial b}{\partial C_j} $$ 上述求和展开后，元素可以组合成一个矩阵，观察可知能够换序：$$  \Big(\frac{\partial A}{\partial C}\Big)_j = \sum_{b\in B}\sum_{a\in A}\frac{\partial a}{\partial b}\cdot\frac{\partial b}{\partial C_j} = \sum_{B_i\in B}\Big(\frac{\partial A}{\partial B}\Big)_i\cdot\frac{\partial B_i}{\partial C_j} $$ 根据先前的推论，假设存在与 $B$ 维度相同的独立矩阵 $D$，观察如下式子：$$  \Big(\frac{D:\partial B}{\partial C}\Big)_j = \Big(\frac{\partial(D:B)}{\partial C}\Big)_j = \sum_{B_i\in B}\frac{\partial(d_i\cdot B_i)}{\partial C_j} = \sum_{B_i\in B}d_i\cdot\frac{\partial B_i}{\partial C_j} $$ 不妨令矩阵 $D = \frac{\partial A}{\partial B}$，然后突然眼前一亮：$$  \Big(\frac{D:\partial(B)}{\partial C}\Big)_j = \sum_{B_i\in B}\Big[(\sum_{a\in A}\frac{\partial a}{\partial B_i})\cdot\frac{\partial B_i}{\partial C_j}\Big] = \sum_{B_i\in B}\Big(\frac{\partial A}{\partial B}\Big)_i\cdot\frac{\partial B_i}{\partial C_j} = \Big(\frac{\partial A}{\partial C}\Big)_j $$ 综上所述，我们运气非常好，得到了链式法则的表示方法：$$  \frac{\partial A}{\partial C} = \frac{\partial A}{\partial B} : \frac{\partial B}{\partial C} $$

6. $F$-范数，基于上述推论，可以轻松得到：
> $$  \frac{\partial||A||_F}{\partial A} = \frac{\partial{\sqrt{\mathbf{e}^TA^{:2}\,\mathbf{e}}}}{\partial A} = \frac{\mathbf{e}^T\dot{\times}\mathbf{e}:2A}{2\sqrt{\mathbf{e}^TA^{:2}\,\mathbf{e}}} = \frac{A}{||A||_F};\;\; \frac{\partial{\frac{1}{2}||A||_F^2}}{\partial A} = A; $$










