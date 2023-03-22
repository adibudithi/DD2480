package org.python.types;


public class Reversed extends Object implements org.python.Object {
    org.python.Object sequence;
    long index;

    public Reversed(org.python.Object sequence) {
        this.sequence = sequence;
        this.index = ((Int) sequence.__len__()).value - 1;
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
        if (this.index < 0) {
            // StopIteration is a singleton by design, see org/python/exceptions/StopIteration
            throw org.python.exceptions.StopIteration.STOPITERATION;
        }
        org.python.Object item = this.sequence.__getitem__(org.python.types.Int.getInt(this.index));
        this.index--;
        return item;
    }
}
