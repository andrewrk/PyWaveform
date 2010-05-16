from distutils.core import setup, Extension
import subprocess

p = subprocess.Popen(['MagickWand-config', '--cflags'], stdout=subprocess.PIPE)
extra_compile_args = p.communicate()[0].strip().split()

p = subprocess.Popen(['MagickWand-config', '--ldflags', '--libs'], stdout=subprocess.PIPE)
extra_link_args = p.communicate()[0].strip().split()

cwaveform = Extension(
    'cwaveformmodule',
    sources = [
        'cwaveformmodule.c',
    ],
    define_macros = [],
    include_dirs=[],
    library_dirs=[],
    libraries=['sndfile'],
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
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

