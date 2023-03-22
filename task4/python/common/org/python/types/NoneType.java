package org.python.types;

import org.Python;

public class NoneType extends org.python.types.Object {
    public static org.python.Object NONE = new org.python.types.NoneType();
    public static final java.lang.String PYTHON_TYPE_NAME = "NoneType";

    NoneType() {
    }

    @org.python.Method(
            __doc__ = ""
    )
    public org.python.Object __ilshift__(org.python.Object other) {
        throw new org.python.exceptions.TypeError("unsupported operand type(s) for <<=: 'NoneType' and '" + other.typeName() + "'");
    }

    @org.python.Method(
            __doc__ = ""
    )
    public org.python.Object __irshift__(org.python.Object other) {
        throw new org.python.exceptions.TypeError("unsupported operand type(s) for >>=: 'NoneType' and '" + other.typeName() + "'");
    }

    @org.python.Method(
            __doc__ = ""
    )
    public org.python.Object __bool__() {
        return org.python.types.Bool.FALSE;
    }

    @org.python.Method(
            __doc__ = "",
            args = {"other"}
    )
    public org.python.Object __ge__(org.python.Object other) {
        return org.python.types.NotImplementedType.NOT_IMPLEMENTED;
    }

    @org.python.Method(
            __doc__ = "",
            args = {"other"}
    )
    public org.python.Object __gt__(org.python.Object other) {
        return org.python.types.NotImplementedType.NOT_IMPLEMENTED;
    }

    @org.python.Method(
            __doc__ = "",
            args = {"other"}
    )
    public org.python.Object __eq__(org.python.Object other) {
        if (other instanceof org.python.types.NoneType) {
            return org.python.types.Bool.TRUE;
        }
        return org.python.types.NotImplementedType.NOT_IMPLEMENTED;
    }

    @org.python.Method(
            __doc__ = "",
            args = {"other"}
    )
    public org.python.Object __lt__(org.python.Object other) {
        return org.python.types.NotImplementedType.NOT_IMPLEMENTED;
    }

    @org.python.Method(
            __doc__ = "",
            args = {"other"}
    )
    public org.python.Object __le__(org.python.Object other) {
        return org.python.types.NotImplementedType.NOT_IMPLEMENTED;
    }

    @org.python.Method(
            __doc__ = ""
    )
    public org.python.Object __mul__(org.python.Object other) {
        if (org.python.types.Object.isSequence(other)) {
            throw new org.python.exceptions.TypeError("can't multiply sequence by non-int of type 'NoneType'");
        } else {
            throw new org.python.exceptions.TypeError(
                    String.format("unsupported operand type(s) for *: 'NoneType' and '%s'",
                            Python.typeName(other.getClass())));
        }
    }


    @org.python.Method(
            __doc__ = ""
    )
    public org.python.Object __imul__(org.python.Object other) {
        if (org.python.types.Object.isSequence(other)) {
            throw new org.python.exceptions.TypeError("can't multiply sequence by non-int of type 'NoneType'");
        } else {
            throw new org.python.exceptions.TypeError(
                    String.format("unsupported operand type(s) for *=: 'NoneType' and '%s'",
                            Python.typeName(other.getClass())));
        }
    }

    @org.python.Method(
            __doc__ = ""
    )
    public org.python.Object __getitem__(org.python.Object other) {
        throw new org.python.exceptions.TypeError("'NoneType' object is not subscriptable");
    }

    public java.lang.Object toJava() {
        return null;
    }

    @org.python.Method(
            __doc__ = ""
    )
    public org.python.types.Str __repr__() {
        return new org.python.types.Str("None");
    }

    public boolean __setattr_null(java.lang.String name, org.python.Object value) {
        return false;
    }

    @org.python.Method(
            __doc__ = ""
    )
    public org.python.Object __round__(org.python.Object ndigits) {

        throw new org.python.exceptions.TypeError("type NoneType doesn't define __round__ method");
    }
}
