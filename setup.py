from distutils.core import setup, Extension

cwaveform = Extension(
    'cwaveformmodule',
    sources = [
        'cwaveformmodule.c',
    ],
    define_macros = [],
    include_dirs=[],
    library_dirs=[],
    libraries=['sndfile'],
)

setup(
    name='waveform',
    version='0.1',
    author="Andrew Kelley",
    author_email="superjoe30@gmail.com",
    description='Create an image of the waveform of an audio file.',
    py_modules=["waveform"],
    ext_modules=[cwaveform],
)

