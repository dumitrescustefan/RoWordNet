from setuptools import setup, find_packages
# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    # $ pip install sampleproject    
    name='rowordnet',  # Required
   
    version='0.9.0',  # Required

    description='Python API for the Romanian WordNet',  # Required

    url='https://github.com/dumitrescustefan/RoWordNet',  # Optional

    classifiers=[  # Optional        
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',        
        'Programming Language :: Python :: 3'        
    ],

    keywords='romanian wordnet rowordnet rown python',  # Optional

    packages=find_packages(exclude=['jupyter']),  # Required

    install_requires=['networkx','lxml'],  # Optional

    package_data={  # Optional
        'rowordnet': ['rowordnet.pickle'],
    }
)