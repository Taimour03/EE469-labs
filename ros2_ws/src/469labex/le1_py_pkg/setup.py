import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'le1_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vboxuser',
    maintainer_email='taimour.abbasi01@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'integer_publisher = le1_py_pkg.integer_publisher:main',
            'cumulative_adder = le1_py_pkg.cumulative_adder:main',
            'le1_lifecycle_manager = le1_py_pkg.le1_lifecycle_manager:main',
        ],
    },
)
