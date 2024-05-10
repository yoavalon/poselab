<img src="docs/poselab_logo.jpg" alt="PoseLab Logo" width="250"/>

A colmap pose analysis, filter and visualization toolkit

```
pip install poselab==0.1.0
```

```
pip install -i https://test.pypi.org/simple/ poselab==0.1.0
```

Using this for piping: 
https://packaging.python.org/en/latest/tutorials/packaging-projects/

python3 -m pip install --upgrade build
python3 -m build
python3 -m twine upload --repository testpypi dist/*

https://test.pypi.org/project/poselab/0.1.0/

#uplad to the real pip
twine upload dist/*
