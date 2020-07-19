from setuptools import setup

setup(name='aisimpoker',
      version='0.1',
      description='The poker player behavior simulator.',
      license='MIT',
      install_requires=[
          'lark-parser',
          'python-dotenv'
      ],
    
      zip_safe=False)