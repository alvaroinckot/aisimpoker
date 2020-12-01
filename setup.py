from setuptools import setup

setup(name='aisimpoker',
      version='0.2',
      description='The poker player behavior simulator.',
      license='MIT',
      install_requires=[
          'lark-parser',
          'python-dotenv',
          'treys',
          'pandas',
          'numpy',
          'sklearn',
          'matplotlib'
      ],

      zip_safe=False)
