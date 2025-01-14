# Active-Space Coupled-Cluster Code Generator

This repository contains code to automatically generate the numerous tensor
contractions arising from active-space coupled-cluster (CC) models, 
such as those of the CCSDt and CCSDtq types. The resulting expressions
are spin-integrated. The expressions for the 
active-space theory of interest are formed by first taking a set of 
factorized spin-integrated diagrams corresponding to the parent CC 
theory (e.g., CCSDT or CCSDTQ), and subsequently applying all possible 
combinations of  active/inactive partitioning to the external and contracted
lines. In doing so, special attention must be paid to account for all
weight and phase factors as well as the additional diagrams that arise from
permuting non-equivalent indices belonging to different sectors (active or
inactive) of the single-particle orbital space. 
