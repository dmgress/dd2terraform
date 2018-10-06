from setuptools import setup, find_packages
setup(
    name="Wuuf",
    version="0.1",
    install_requires=[
      'datadog >= 0.22.0',
      'jinja2 >= 2.10',
      'python-dotenv >= 0.9.1',
      'click >= 7.0'
      ],
    entry_points={
      'console_scripts': [
        'wuuf = wuuf:main',
        ]
      }
    )
