from setuptools import setup, find_packages
# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    # $ pip install sampleproject    
    name='rowordnet',  # Required
   
    version='1.0.0',  # Required

    description='Python API for the Romanian WordNet',  # Required

    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer = "Stefan Daniel Dumitrescu and Andrei Marius Avram",
    maintainer_email = "dumitrescu.stefan@gmail.com, avram.andreimarius@gmail.com",
    author = "Stefan Daniel Dumitrescu and Andrei Marius Avram",
    author_email = "dumitrescu.stefan@gmail.com, avram.andreimarius@gmail.com",
    
    url='https://github.com/dumitrescustefan/RoWordNet',  # Optional

    classifiers=[  # Optional        
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
        
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
               
        'Programming Language :: Python :: 3'        
    ],

    keywords='romanian wordnet rowordnet rown python',  # Optional

    #packages=find_packages(exclude=['jupyter']),  # Required
    packages=find_packages("."),  # Required

    install_requires=['networkx','lxml'],  # Optional
    
    zip_safe=False,
    
    package_data={  # Optional
        'rowordnet': ['rowordnet.pickle'],
    }
)