#include "Python.h"

#include <stdio.h>
#include <sndfile.h>
#include <string.h>
#include <limits.h>

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

    // open the file
    SF_INFO sfInfo;
    memset(&sfInfo, 0, sizeof(SF_INFO));
    SNDFILE * file = sf_open(inAudioFile, SFM_READ, &sfInfo);
    if (file == NULL) {
        PyErr_SetString(PyExc_IOError, "Error reading the audio file.");
        return NULL;
    }

    // draw the wave
    float framesPerPixel = sfInfo.frames / ((float)imageWidth);
    int framesToSee = (int)framesPerPixel;
    // speed hack
    if (cheat) {
        if (framesToSee > 500)
            framesToSee = 500;
    }
    int pixelFramesByteSize = framesToSee * sfInfo.channels;
    
    // for each pixel
    int * frames = (int *) malloc(sizeof(int) * sfInfo.channels * framesToSee);
    if (frames == NULL) {
        sf_close(file);
        PyErr_SetString(PyExc_MemoryError, "Out of memory.");
        return NULL;
    }

    float sampleMin = INT_MIN;
    float sampleMax = INT_MAX;
    float sampleRange = (sampleMax - sampleMin);
    int x;
    for (x=0; x<imageWidth; ++x) {
        // range of frames that fit in this pixel
        int start = x * framesPerPixel;

        // get the min and max of this range
        sf_seek(file, start, SEEK_SET);
        sf_readf_int(file, frames, framesToSee);
        float min = sampleMin;
        float max = sampleMax;
        // for each frame from start to end
        int i;
        for (i=0; i<pixelFramesByteSize; i+=sfInfo.channels) {
            // average the channels
            float value = 0;
            int c;
            for (c=0; c<sfInfo.channels; ++c)
                value += frames[i+c];
            value /= sfInfo.channels;
            
            // keep track of max/min
            if (value < min)
                min = value;
            if (value > max)
                max = value;
        }
        // translate into y pixel coord
        int y_min = (int)((min - sampleMin) / sampleRange * imageHeight);
        int y_max = (int)((max - sampleMin) / sampleRange * imageHeight);

        // draw
        // TODO: imagemagick
    }
    // TODO: save the image

    // clean up
    free(frames);
    sf_close(file);
    
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
