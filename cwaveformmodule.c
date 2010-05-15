#include "Python.h"

static PyObject *
cwaveform_draw(self, args, keywds)
    PyObject *self; /* Not used */
    PyObject *args;
    PyObject *keywds;
{
    // arg list
    char * inAudioFile;
    char * outImageFile;
    long imageWidth;
    long imageHeight;
    char bgColorRed;
    char bgColorGreen;
    char bgColorBlue;
    char bgColorAlpha;
    char fgColorRed;
    char fgColorGreen;
    char fgColorBlue;
    char fgColorAlpha;
    char cheat; //bool

    // get arguments
    if (!PyArg_ParseTuple(args, "ssllbbbbbbbbb",
        &inAudioFile, &outImageFile, &imageWidth, &imageHeight,
        &bgColorRed, &bgColorGreen, &bgColorBlue, &bgColorAlpha,
        &fgColorRed, &fgColorGreen, &fgColorBlue, &fgColorAlpha,
        &cheat))
    {
        return NULL;
    }
    
    // no return value
    Py_INCREF(Py_None);
    return Py_None;
}


/* List of functions defined in the module */

static PyMethodDef cwaveform_methods[] = {
    {"draw",        cwaveform_draw,        METH_VARARGS|METH_KEYWORDS},
    {NULL,        NULL}        /* sentinel */
};


/* Initialization function for the module (*must* be called initcwaveform) */

DL_EXPORT(void)
initcwaveform()
{
    PyObject *m, *d;

    /* Create the module and add the functions */
    m = Py_InitModule("cwaveform", cwaveform_methods);
}
