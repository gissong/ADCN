# ADCN
[Anisotropic Density-Based Trajectory Clustering with Noise](https://github.com/gengchenmai/adcn) 

Density-based clustering algorithms such as DBSCAN have been widely used for spatial knowledge discovery as they offer several key advantages compared to other clustering algorithms. They can discover clusters with arbitrary shapes, are robust to noise and do not require prior knowledge (or estimation) of the number of clusters. The idea of using a scan circle centered at each point with a search radius Eps to find at least MinPts points as a criterion for deriving local density is sufficient for exploring isotropic spatial point patterns. However, there are many cases that cannot be adequately captured this way, particularly if they involve linear features or shapes with a continuously changing density such as a spiral. In such cases, DBSCAN tends to either create an increasing number of small clusters or add noise points into large clusters. Therefore, in this paper, we propose a novel anisotropic density-based clustering algorithm (ADCN). To motivate our work, we introduce synthetic and real-world cases that cannot be sufficiently handled by DBSCAN (and OPTICS). We then present our clustering algorithm and test it with a wide range of cases. We demonstrate that our algorithm can perform as equally well as DBSCAN in cases that do not explicitly benefit from an anisotropic perspective and that it outperforms DBSCAN in cases that do. We show that our approach has the same time complexity as DBSCAN and OPTICS, namely O(n log n) when using a spatial index and O(n^2) otherwise. We provide an implementation and test the runtime over multiple cases. Finally, we apply DBSCAN, OPTICS, and our ADCN to the extraction of urban Areas of interest (AOI) from geotagged photos in six cities. Visual comparison shows that, comparing to DBSCAN and OPTICS, ADCN is inclined to extract AOI with linear shapes which follow the underline road network. ADCN also turn out to connect areas when the spatial distribution of them shows similar direction.

# References:
[1] Gengchen Mai, Krzysztof Janowicz, Yingjie Hu, Song Gao. ADCN: An Anisotropic Density-Based Clustering Algorithm for Discovering Spatial Point Patterns with Noise. Transactions in GIS, 22(2018), 348-369. [DOI:10.1111/tgis.12313](https://onlinelibrary.wiley.com/doi/full/10.1111/tgis.12313)
[2] 
 ```
@article{mai2018adcn,
  title={ADCN: An anisotropic density-based clustering algorithm for discovering spatial point patterns with noise},
  author={Mai, Gengchen and Janowicz, Krzysztof and Hu, Yingjie and Gao, Song},
  journal={Transactions in GIS},
  volume={22},
  number={1},
  pages={348--369},
  year={2018},
  publisher={Wiley Online Library}
}
```

# Code Versions
The original code and experiments were developed in [Javascript](https://github.com/gengchenmai/adcn) by UCSB Geography Gengchen Mai.
![Image description](https://github.com/gissong/ADCN/blob/master/figures/interface.png)

The Python version of the ADCN-KNN was further developed by Mingxiao Li (Chinese Academy of Sciences) and Song Gao (UW-Madison). 
![Image description](https://github.com/gissong/ADCN/blob/master/figures/vectorzation.png)

