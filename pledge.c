#include <unistd.h>
#include "Python.h"

static PyObject *
py_pledge(PyObject *self, PyObject *args)
{
	const char *promises;
	int r;

	if (!PyArg_ParseTuple(args, "s", &promises))
		return NULL;

	r = pledge(promises);

#if PY_MAJOR_VERSION >= 3
	return PyLong_FromLong(r);
#else
	return Py_BuildValue("i", r);
#endif
}

static PyMethodDef PledgeMethods[] = {
	{"pledge", py_pledge, METH_VARARGS, "Call OpenBSD pledge"},
	{NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef pledgemodule = {
	PyModuleDef_HEAD_INIT,
	"pledge",
	"OpenBSD pledge binding",
	-1,
	PledgeMethods
};

PyMODINIT_FUNC
PyInit_pledge(void)
{
	return PyModule_Create(&pledgemodule);
}

#else

PyMODINIT_FUNC
initpledge(void)
{
	(void) Py_InitModule("pledge", PledgeMethods);
}

#endif
