from setuptools import setup

setup(
    name='posefilter',
    version='0.1.0',    
    description='A colmap parser',
    url='https://github.com/yoavalon/posefilter',
    author='Yoav Alon',
    author_email='algoretics@gmail.com',
    license='BSD 2-clause',
    packages=['posefilter'],
    install_requires=['numpy', 'tqdm'                    
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',   
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
