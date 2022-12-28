from distutils.core import setup
setup(
  name='ocsp-responder-server',
  packages=['ocsp_responder_server'],
  version='0.1',
  license='MIT',
  description='Simple OCSP Responder RPC Server',
  long_description='Simple OCSP Responder Server using json-rpc and openssl-ocsp-responder',
  author='Deborah Jalfon',
  author_email='deborah.jalfon@redis.com',
  url='https://github.com/deborahjalfont/ocsp-responder-server',
  keywords=['ocsp', 'responder', 'server'],
  install_requires=['json-rpc', 'openssl-ocsp-responder'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
  ],
)
