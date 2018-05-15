from setuptools import setup, find_packages
version = '1.0.0'
dependencies = ['requests==2.18.4']
setup_config = {'name': 'stackstats',
                'version': version,
                'description': 'A StackExchange API simple stats calculator',
                'install_requires': dependencies,
                'entry_points': {
                    'console_scripts': ['stats=stackstats:main']
                }
            }


if __name__ == '__main__':
    setup(**setup_config)
