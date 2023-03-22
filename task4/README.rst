
VOC
===

.. image:: https://img.shields.io/pypi/pyversions/voc.svg
    :target: https://pypi.python.org/pypi/voc

.. image:: https://img.shields.io/pypi/v/voc.svg
    :target: https://pypi.python.org/pypi/voc

.. image:: https://img.shields.io/pypi/status/voc.svg
    :target: https://pypi.python.org/pypi/voc

.. image:: https://img.shields.io/pypi/l/voc.svg
    :target: https://github.com/beeware/voc/blob/master/LICENSE

.. image:: https://beekeeper.beeware.org/projects/beeware/voc/shield
    :target: https://beekeeper.beeware.org/projects/beeware/voc

.. image:: https://badges.gitter.im/beeware/general.svg
    :target: https://gitter.im/beeware/general

A transpiler that converts Python code into Java bytecode.

This is experimental code. If it breaks, you get to keep all the shiny pieces.

What it does:

* Provides an API to let you programmatically create Java class files.

* Compiles Python 3.4 source files into Java class files, enabling you to run
  Python code on a JVM (including Android's VM).

It isn't a *completely* compliant Python 3.4 implementation - there are some
language features (some builtin functions) that still need to be
implemented, and there is only a bare bones standard library implementation.
However, it is possible to convert simple Python programs, and even write
simple Android applications.

Tutorial
--------

To take VOC for a spin, run through the `Getting Started guide`_, then start
with `the first tutorial`_.

If you'd like to contribute to VOC development, we have a `guide for first time contributors`_.

.. _Getting Started guide: https://voc.readthedocs.io/en/latest/index.html
.. _the first tutorial: https://voc.readthedocs.io/en/latest/tutorial/tutorial-0.html

.. _guide for first time contributors: https://beeware.org/contributing/how/first-time/what/voc/

Documentation
-------------

Documentation for VOC can be found on `Read The Docs`_.

Why "VOC"?
----------

VOC is a backronym for "Vestigial Output Compiler". Or "Vexing Obtuse
Compiler". Or "Valuable Obscure Compiler". Or "Varigated Ocelot Calibrator".
It's your choice.

Historically, VOC was the `Vereenigde Oostindische Compagnie (VOC)`_, or Dutch
East India Company, often considered to be the world's first multinational
corporation. It was also the first company to issue shares, and facilitate the
trading of those shares. It was granted a 21 year monopoly to carry out trade
activities in Asia, primarily the Spice Islands - the Dutch East Indies. They
established a major trading port at Batavia - now Jakarta - on the island of
Java (now part of Indonesia).

While VOC was a very profitable business for it's shareholders, it operated as
a colonial power. Modern historians have `expressed criticism of their business
practices`_, which included exploitation of indigenous populations (including
use of slave labour), slave trade, use of violence, and environmental
destruction (including deforestation).

VOC also played a role in the European discovery of Australia, and there are
many VOC shipwrecks on the coast of Western Australia.

The name VOC was chosen by the project because the project founder is from
Western Australia, and VOC has a strong non-colonial presence in that state's
history. It was also a convenient pun, as VOC was an enterprise Java company.

It should not be considered an endorsement or glorification of the
exploitative business practices of the company.

.. _Vereenigde Oostindische Compagnie (VOC): https://en.wikipedia.org/wiki/Dutch_East_India_Company
.. _expressed criticism of their business practices: https://en.wikipedia.org/wiki/Dutch_East_India_Company#Criticism

Community
---------

VOC is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `beeware/general`_ channel on Gitter.

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct`_.

Contributing
------------

To get started with contributing to VOC, head over to our `First Timers Guide`_.

If you experience problems with VOC, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: https://beeware.org
.. _Read The Docs: https://voc.readthedocs.io
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _beeware/general: https://gitter.im/beeware/general
.. _BeeWare Community Code of Conduct: https://beeware.org/community/behavior/
.. _First Timers Guide: https://beeware.org/contributing/how/first-time/what/voc/
.. _log them on Github: https://github.com/beeware/voc/issues
.. _fork the code: https://github.com/beeware/voc
.. _submit a pull request: https://github.com/beeware/voc/pulls
