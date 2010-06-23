from distutils.core import setup, Extension
import subprocess

# ---- edit these variables to configure -----
mpg123_include_dir = '/usr/include/'
mpg123_libs = 'mpg123'
mpg123_lib_dir = '/usr/lib'
# --------------------------------------------
# note: it may be necessary to swap #include <Python.h> and #include <mpg123.h>
#       depending on your architecture
# --------------------------------------------

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
    undef_macros = [],
    include_dirs=mpg123_include_dir.split(),
    library_dirs=[mpg123_lib_dir],
    libraries=['sndfile'] + mpg123_libs.split(),
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
)

setup(
    name='waveform',
    version=__import__('waveform').__version__,
    author="Andrew Kelley",
    author_email="superjoe30@gmail.com",
    description='Create an image of the waveform of an audio file.',
    py_modules=["waveform"],
    ext_modules=[cwaveform],
)

