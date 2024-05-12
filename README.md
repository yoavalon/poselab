<img src="docs/poselab_logo.jpg" alt="PoseLab Logo" width="250"/>

A colmap pose analysis, filter and visualization toolkit

```
pip3 install poselab
```

# How to use: 

Import pose: 

```
from poselab import pose
```

Load the binaries:
```
input_path = '/home/algo/nerf/exp30/colmap/sparse/0'
pose.load(input_path)
```

Describe the pose and show:
```
pose.describe()    
pose.show()
```

Filter features around a point (0,0,0):
```
pose.filter_features_around([0,0,0], 3)
pose.show()
```

Using this for piping: 
https://packaging.python.org/en/latest/tutorials/packaging-projects/

python3 -m pip install --upgrade build
python3 -m build
python3 -m twine upload --repository testpypi dist/*

https://test.pypi.org/project/poselab/0.1.0/

#uplad to the real pip
twine upload dist/*
