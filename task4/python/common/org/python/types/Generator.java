package org.python.types;

/**
 * Possible states of a generator:
 * 1. yield_point == 0    : The generator has just started
 * 2. expression  == null : The generator is exhausted
 * 3. message     != none : The generator currently holds value sent from caller via send() method
 * 4. exception   != null : The generator currently holds exception sent from caller via throw() method
 *
 * Notes: All states are mutually exclusive, (e.g if generator is in state 1 (yield_point == 0),
 * expression must not be null, message must be none and exception must be null, similarly for states 2, 3 and 4)
 */
public class Generator extends org.python.types.Object {
    java.lang.String name;
    java.lang.reflect.Method expression;
    public int yield_point;
    public java.util.Map<java.lang.String, org.python.Object> stack;
    public org.python.types.Closure closure; // null for non-closure Generator

    public org.python.Object message;
    public org.python.exceptions.BaseException exception;

    public int hashCode() {
        return this.expression.hashCode();
    }

    public Generator(
            java.lang.String name,
            java.lang.reflect.Method expression,
            java.util.Map<java.lang.String, org.python.Object> stack
    ) {
        // System.out.println("GENERATOR: " + expression);
        // for (org.python.Object obj: stack) {
        //     System.out.println("     : " + obj);
        // }
        this.name = name;
        this.expression = expression;
        this.yield_point = 0;
        this.stack = stack;
        this.message = org.python.types.NoneType.NONE;
        this.closure = null;
    }

    public Generator(
            java.lang.String name,
            java.lang.reflect.Method expression,
            java.util.Map<java.lang.String, org.python.Object> stack,
            org.python.types.Closure closure
    ) {
        // System.out.println("GENERATOR: " + expression);
        // for (org.python.Object obj: stack) {
        //     System.out.println("     : " + obj);
        // }
        this.name = name;
        this.expression = expression;
        this.yield_point = 0;
        this.stack = stack;
        this.message = new org.python.types.NoneType();
        this.closure = closure;
    }

    protected void finalize() throws Throwable {
        super.finalize();
        this.__del__();
    }

    /**
     * API exposed primarily to handle `yield from`
     * Intercepts exception and decide whether to yield next value from `iterator` (via send or __next__)
     * or throw exception into `iterator` if `iterator` is a generator
     *
     * Flow:
     * 1. this.exception == null
     *    1.1 Get next yield value via `get_next_yield_value`
     *    1.2 If StopIteration, re-throw that exception
     *
     * 2. this.exception != null, intercepts this.exception.
     *    2.1 If `iterator` is not a generator, the exception is thrown back to caller.
     *    2.2 If this.exception is GeneratorExit, close the sub-generator
     *    2.3 Otherwise throws the exception into sub-generator
     *        2.2.1 If the sub-generator handles the exception and returns a value,
     *              returns that value as next yield value.
     *        2.2.2 If the sub-generator raises StopIteration, re-throw that exception
     *
     */
    public org.python.Object intercept_exception(org.python.Object iterator) {
        if (this.exception == null) {
            org.python.Object msg = this.message;
            this.reset_message();
            try {
                return get_next_yield_value(iterator, msg);
            } catch (org.python.exceptions.StopIteration stopIteration) {
                throw stopIteration;
            }
            //return null;
        } else {
            org.python.exceptions.BaseException exception = this.exception;
            this.exception = null;
            try {
                throw exception;
            } catch (org.python.exceptions.GeneratorExit generatorExit) {
                try {
                    ((org.python.types.Generator) iterator).close();
                } catch (java.lang.ClassCastException e) {
                    // pass
                }
                throw generatorExit;
            } catch (org.python.exceptions.BaseException baseException) {
                try {
                    // pass baseException into sub-generator
                    return ((org.python.types.Generator) iterator).throw$(baseException.type(), baseException.args, null);
                } catch (java.lang.ClassCastException e) {
                    // if iterator is not a generator, just throw the baseException
                    throw baseException;
                } catch (org.python.exceptions.StopIteration stopIteration) {
                    throw stopIteration;
                }
            }
        }
    }

    /**
     * Returns the next item from iterator
     *
     * Invokes __next__() on iterator if message is None
     * Invokes send() if message is not None, and if iterator is not a generator, raise AttributeError
     */
    private static org.python.Object get_next_yield_value(org.python.Object iterator, org.python.Object message) {
        if (message instanceof org.python.types.NoneType) {
            return iterator.__next__();
        } else {
            try {
                return ((org.python.types.Generator) iterator).send(message);
            } catch (ClassCastException e) {
                throw new org.python.exceptions.AttributeError(
                    "'" + iterator.typeName() + "' object has no attribute 'send'");
            }
        }
    }

    public void yield(java.util.Map<java.lang.String, org.python.Object> stack, int yield_point) {
        // System.out.println("YIELD: " + yield_point);
        // for (org.python.Object obj: stack) {
        //     System.out.println("     : " + obj);
        // }
        this.yield_point = yield_point;
        this.stack = stack;
    }

    @org.python.Method(
            __doc__ = "Implement send(message).",
            args = {"message"}
    )
    public org.python.Object send(org.python.Object message) {
        if (this.yield_point == 0 && !(message instanceof org.python.types.NoneType)) {
            throw new org.python.exceptions.TypeError("can't send non-None value to a just-started generator");
        }
        this.message = message;
        return this.__next__();
    }

    public void reset_message() {
        this.message = org.python.types.NoneType.NONE;
    }

    /**
     * Construct an exception and store it in `this.exception` then call __next__() on this generator.
     * `this.exception` will then be thrown by `this.throw_exception` when the generator resumes.
     */
    @org.python.Method(
            name = "throw",
            __doc__ = "Implement throw(type, value=None, traceback=None).",
            args = {"type"},
            default_args = {"exception_args", "traceback"}
    )
    public org.python.Object throw$(org.python.Object type, org.python.Object exception_args, org.python.Object traceback) {
        if (exception_args == null) {
            exception_args = org.python.types.NoneType.NONE;
        }

        if (traceback != null) {
            throw new org.python.exceptions.NotImplementedError("traceback currently not supported");
        }

        String exception_name;

        try {
            exception_name = org.Python.typeName(((org.python.types.Type) type).klass);
        } catch (ClassCastException e) {
            throw new org.python.exceptions.TypeError(
                "exceptions must be classes or instances deriving from BaseException, not " + type.typeName());
        }

        try {
            Class<?> exception_class = Class.forName("org.python.exceptions." + exception_name);
            java.lang.reflect.Constructor exception_constructor;
            if (exception_args instanceof org.python.types.NoneType) {
                // value = None
                exception_constructor = exception_class.getConstructor();
                this.exception = (org.python.exceptions.BaseException)
                    Type.toPython(exception_constructor.newInstance());
            } else if (exception_args instanceof org.python.types.Tuple) {
                // value is variable arguments
                exception_constructor = exception_class.getConstructor(org.python.Object[].class, java.util.Map.class);
                int size = ((org.python.types.Tuple) exception_args).value.size();
                org.python.Object[] vargs = new org.python.Object[size];
                for (int i = 0; i < size; i++) {
                    vargs[i] = ((org.python.types.Tuple) exception_args).value.get(i);
                }
                this.exception = (org.python.exceptions.BaseException)
                    Type.toPython(exception_constructor.newInstance(vargs, null));
//            } else if (exception_args instanceof org.python.types.Dict) {
//                // TODO: Test/modify this when custom exception that supports kwargs is implemented
//                exception_constructor = exception_class.getConstructor(org.python.Object[].class, java.util.Map.class);
//                java.util.Map kwargs = new java.util.HashMap<java.lang.String, org.python.Object>();
//                for (java.util.Map.Entry entry : ((org.python.types.Dict)exception_args).value.entrySet()) {
//                    java.lang.String key = entry.getKey().toString();
//                    org.python.Object item = (org.python.Object)entry.getValue();
//                    kwargs.put(key, item);
//                }
//                this.exception = Type.toPython(exception_constructor.newInstance(null, kwargs));
            } else {
                // use value.__str__() as exception argument
                exception_constructor = exception_class.getConstructor(String.class);
                this.exception = (org.python.exceptions.BaseException)
                    Type.toPython(exception_constructor.newInstance(exception_args.toString()));
            }
        } catch (ClassNotFoundException e) {
            throw new org.python.exceptions.NameError(exception_name);
        } catch (NoSuchMethodException |
            InstantiationException | IllegalAccessException | java.lang.reflect.InvocationTargetException e) {
            throw new org.python.exceptions.RuntimeError(e.getMessage());
        }

        if (this.yield_point == 0) {
            this.close();
            throw this.exception;
        }

        try {
            return this.__next__();
        } catch (org.python.exceptions.BaseException e) {
            this.cleanup(); // close this generator if it did not catch the exception
            throw e; // re-throw exception after closing
        }
    }

    /**
     * Called when generator is restored.
     * The exception stored in `this.exception` is thrown here
     * NO-OP if this.exception == null
     */
    public void throw_exception() {
        if (this.exception != null) {
            org.python.exceptions.BaseException exception = this.exception;
            this.exception = null;
            throw exception;
        }
    }

    @org.python.Method(
            __doc__ = "Implement close(self)."
    )
    public org.python.Object close() {
        if (this.yield_point == 0) {
            this.expression = null;
        }

        if (this.expression == null) {
            // Do nothing if generator has already exited
            return org.python.types.NoneType.NONE;
        }

        boolean has_exit_normally = false;
        try {
            this.exception = new org.python.exceptions.GeneratorExit();
            this.__next__();
        } catch (org.python.exceptions.GeneratorExit | org.python.exceptions.StopIteration e) {
            has_exit_normally = true;
        }
        if (!has_exit_normally) {
            // Generator caught GeneratorExit exception and yields
            throw new org.python.exceptions.RuntimeError("generator ignored GeneratorExit");
        }

        this.cleanup();
        return org.python.types.NoneType.NONE;
    }

    private void cleanup() {
        this.expression = null;
        this.message = null;
        this.exception = null;
    }

    @org.python.Method(
            __doc__ = "Return del(self)."
    )
    public void __del__() {
        try {
            this.close();
        } catch (Exception e) {
            java.lang.String message = e.getCause().getMessage();
            if (message == null) {
                message = e.getCause().getClass().getName();
            }
            System.err.println(message);
        }
    }

    @org.python.Method(
            __doc__ = "Return repr(self)."
    )
    public org.python.Object __repr__() {
        // if (this.expression.getName().startswith("genexpr_"))
        return new org.python.types.Str(String.format("<%s object (%s) at 0x%x>", this.typeName(), this.name, this.hashCode()));
    }

    @org.python.Method(
            __doc__ = "Implement iter(self)."
    )
    public org.python.Object __iter__() {
        return this;
    }

    @org.python.Method(
            __doc__ = "Implement next(self)."
    )
    public org.python.Object __next__() {
        if (this.expression == null) {
            // Generator has already exited
            throw org.python.exceptions.StopIteration.STOPITERATION;
        }
        try {
            return (org.python.Object) this.expression.invoke(null, new java.lang.Object[]{this});
        } catch (java.lang.IllegalAccessException e) {
            throw new org.python.exceptions.RuntimeError("Illegal access to Java method " + this.expression);
        } catch (java.lang.reflect.InvocationTargetException e) {
            try {
                // org.Python.debug("Exception:", e.getTargetException());
                // for (java.lang.StackTraceElement ste: e.getTargetException().getStackTrace()) {
                //     org.Python.debug("     ", ste);
                // }

                // If the Java method raised an Python exception, re-raise that
                // exception as-is. If it wasn"t a Python exception, wrap it
                // as one and continue.
                throw (org.python.exceptions.BaseException) e.getCause();
            } catch (ClassCastException java_e) {
                java.lang.String message = e.getCause().getMessage();
                if (message == null) {
                    message = e.getCause().getClass().getName();
                }
                throw new org.python.exceptions.RuntimeError(message);
            }
        // } finally {
            //     System.out.println("INVOKE METHOD DONE");
        }
    }
}
