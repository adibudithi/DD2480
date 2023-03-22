package org.python.types;

public class NotImplementedType extends org.python.types.Object {
    public static org.python.Object NOT_IMPLEMENTED = new org.python.types.NotImplementedType();
    public static final java.lang.String PYTHON_TYPE_NAME = "NotImplementedType";

    NotImplementedType() {
    }

    public java.lang.Object toJava() {
        return null;
    }

    @org.python.Method(
            __doc__ = ""
    )
    public org.python.types.Str __repr__() {
        return new org.python.types.Str("NotImplemented");
    }

    public boolean __setattr_null(java.lang.String name, org.python.Object value) {
        return false;
    }

    @org.python.Method(
            __doc__ = ""
    )
    public org.python.types.Bool __bool__() {
        return org.python.types.Bool.TRUE;
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
        if (other instanceof org.python.types.NotImplementedType) {
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
            __doc__ = "",
            args = {"other"}
    )
    public org.python.Object __mul__(org.python.Object other) {
        if (other instanceof org.python.types.Str || other instanceof org.python.types.List || other instanceof org.python.types.Tuple || other instanceof org.python.types.Bytes || other instanceof org.python.types.ByteArray) {
            throw new org.python.exceptions.TypeError("can't multiply sequence by non-int of type 'NotImplementedType'");
        } else {
            throw new org.python.exceptions.TypeError(
                    String.format("unsupported operand type(s) for *: 'NotImplementedType' and '%s'",
                            other.typeName())
            );
        }
    }

    @org.python.Method(
            __doc__ = "",
            args = {"other"}
    )
    public org.python.Object __imul__(org.python.Object other) {
        try {
            return this.__mul__(other);
        } catch (org.python.exceptions.TypeError e) {
            if (other instanceof org.python.types.Str || other instanceof org.python.types.List || other instanceof org.python.types.Tuple || other instanceof org.python.types.Bytes || other instanceof org.python.types.ByteArray) {
                throw new org.python.exceptions.TypeError("can't multiply sequence by non-int of type 'NotImplementedType'");
            } else {
                throw new org.python.exceptions.TypeError(
                        String.format("unsupported operand type(s) for *=: 'NotImplementedType' and '%s'",
                                other.typeName())
                );
            }
        }
    }
}
