import sys
from ..java import (
    Annotation, Code as JavaCode, ConstantElementValue, Method as JavaMethod,
    RuntimeVisibleAnnotations, opcodes as JavaOpcodes, Classref as JavaClassref
)
from .blocks import Block, Accumulator, BlockCodeTooLarge
from .structures import (
    TRY, CATCH, END_TRY,
    ArgType, IF, END_IF
)
from .types import java, python
from .types.primitives import (
    ALOAD_name, ASTORE_name, free_name,
    DLOAD_name, FLOAD_name,
    ICONST_val, ILOAD_name,
    LLOAD_name,
)
# from .debug import DEBUG, DEBUG_value


CO_VARARGS = 0x0004
CO_VARKEYWORDS = 0x0008
CO_GENERATOR = 0x0020


def descriptor(annotation):
    if annotation == 'bool':
        return 'Z'
    elif annotation == 'byte':
        return 'B'
    elif annotation == 'char':
        return 'C'
    elif annotation == 'short':
        return 'S'
    elif annotation == 'int':
        return 'I'
    elif annotation == 'long':
        return 'J'
    elif annotation == 'float':
        return 'F'
    elif annotation == 'double':
        return 'D'
    elif annotation is None or annotation == 'void':
        return 'V'
    else:
        return 'L%s;' % annotation.replace('.', '/')


def to_python(accumulator, annotation, var_name):
    if annotation == "bool":
        accumulator.add_opcodes(
            # DEBUG("INPUT %s TRANSFORM %s" % (i, annotation)),

            ILOAD_name(var_name),
            JavaOpcodes.INVOKESTATIC(
                'org/python/types/Bool',
                'getBool',
                args=['Ljava/lang/Long;'],
                returns='Lorg/python/types/Bool;'),
        )
    elif annotation == "byte":
        accumulator.add_opcodes(
            # DEBUG("INPUT %s TRANSFORM %s" % (i, annotation)),

            ILOAD_name(var_name),
            JavaOpcodes.INVOKESTATIC(
                'org/python/types/Int',
                'getInt',
                args=['B'],
                returns='Lorg/python/types/Int;'
            ),
        )
    elif annotation == 'char':
        accumulator.add_opcodes(
            # DEBUG("INPUT %s TRANSFORM %s" % (i, annotation)),

            ILOAD_name(var_name),
            JavaOpcodes.INVOKESTATIC(
                'org/python/types/Int',
                'getInt',
                args=['C'],
                returns='Lorg/python/types/Int;'
            ),
        )
    elif annotation == "short":
        accumulator.add_opcodes(
            # DEBUG("INPUT %s TRANSFORM %s" % (i, annotation)),

            ILOAD_name(var_name),
            JavaOpcodes.INVOKESTATIC(
                'org/python/types/Int',
                'getInt',
                args=['S'],
                returns='Lorg/python/types/Int;'
            ),
        )
    elif annotation == "int":
        accumulator.add_opcodes(
            # DEBUG("INPUT %s TRANSFORM %s" % (i, annotation)),

            ILOAD_name(var_name),
            JavaOpcodes.INVOKESTATIC(
                'org/python/types/Int',
                'getInt',
                args=['I'],
                returns='Lorg/python/types/Int;'
            ),
        )
    elif annotation == "long":
        accumulator.add_opcodes(
            # DEBUG("INPUT %s TRANSFORM %s" % (i, annotation)),

            LLOAD_name(var_name),
            JavaOpcodes.INVOKESTATIC(
                'org/python/types/Int',
                'getInt',
                args=['J'],
                returns='Lorg/python/types/Int;'
            ),
        )
    elif annotation == "float":
        accumulator.add_opcodes(
            # DEBUG("INPUT %s TRANSFORM %s" % (i, annotation)),

            java.New('org/python/types/Float'),
            FLOAD_name(var_name),
            java.Init('org/python/types/Float', 'F'),
        )
    elif annotation == "double":
        accumulator.add_opcodes(
            # DEBUG("INPUT %s TRANSFORM %s" % (i, annotation)),

            java.New('org/python/types/Float'),
            DLOAD_name(var_name),
            java.Init('org/python/types/Float', 'D'),
        )
    else:
        accumulator.add_opcodes(
            # DEBUG("INPUT %s TRANSFORM %s" % (i, annotation)),
            ALOAD_name(var_name),
            python.Type.to_python(),
        )


def to_java(accumulator, annotation):
    if annotation == 'void':
        accumulator.add_opcodes(
            JavaOpcodes.POP(),
        )
    elif annotation == 'bool':
        accumulator.add_opcodes(
            JavaOpcodes.CHECKCAST('org/python/types/Bool'),
            JavaOpcodes.GETFIELD('org/python/types/Bool', 'value', 'Z'),
        )
    elif annotation == 'byte':
        accumulator.add_opcodes(
            JavaOpcodes.CHECKCAST('org/python/types/Int'),
            JavaOpcodes.GETFIELD('org/python/types/Int', 'value', 'J'),
            JavaOpcodes.L2I(),
            JavaOpcodes.I2B(),
        )
    elif annotation == 'char':
        accumulator.add_opcodes(
            JavaOpcodes.INVOKEINTERFACE('org/python/Object', 'toJava', args=[], returns='Ljava/lang/Object;'),
            JavaOpcodes.CHECKCAST('java/lang/String'),
            ICONST_val(0),
            JavaOpcodes.INVOKEVIRTUAL('java/lang/String', 'charAt', args=['I'], returns='C'),
        )
    elif annotation == 'short':
        accumulator.add_opcodes(
            JavaOpcodes.CHECKCAST('org/python/types/Int'),
            JavaOpcodes.GETFIELD('org/python/types/Int', 'value', 'J'),
            JavaOpcodes.L2I(),
            JavaOpcodes.I2S(),
        )
    elif annotation == 'int':
        accumulator.add_opcodes(
            JavaOpcodes.CHECKCAST('org/python/types/Int'),
            JavaOpcodes.GETFIELD('org/python/types/Int', 'value', 'J'),
            JavaOpcodes.L2I(),
        )
    elif annotation == 'long':
        accumulator.add_opcodes(
            JavaOpcodes.CHECKCAST('org/python/types/Int'),
            JavaOpcodes.GETFIELD('org/python/types/Int', 'value', 'J'),
        )
    elif annotation == 'float':
        accumulator.add_opcodes(
            JavaOpcodes.CHECKCAST('org/python/types/Float'),
            JavaOpcodes.GETFIELD('org/python/types/Float', 'value', 'D'),
            JavaOpcodes.DTOF(),
        )
    elif annotation == 'double':
        accumulator.add_opcodes(
            JavaOpcodes.CHECKCAST('org/python/types/Float'),
            JavaOpcodes.GETFIELD('org/python/types/Float', 'value', 'D'),
        )
    elif annotation != 'org/python/Object':
        accumulator.add_opcodes(
            JavaOpcodes.INVOKEINTERFACE('org/python/Object', 'toJava', args=[], returns='Ljava/lang/Object;'),
            JavaOpcodes.CHECKCAST(annotation.replace('.', '/')),
        )


def return_statement(accumulator, annotation):
    if annotation == 'void':
        accumulator.add_opcodes(
            JavaOpcodes.RETURN()
        )
    elif annotation in ['bool', 'byte', 'char', 'short', 'int']:
        accumulator.add_opcodes(
            JavaOpcodes.IRETURN(),
        )
    elif annotation == 'long':
        accumulator.add_opcodes(
            JavaOpcodes.LRETURN(),
        )
    elif annotation == 'float':
        accumulator.add_opcodes(
            JavaOpcodes.FRETURN(),
        )
    elif annotation == 'double':
        accumulator.add_opcodes(
            JavaOpcodes.DRETURN(),
        )
    else:
        accumulator.add_opcodes(
            JavaOpcodes.ARETURN()
        )


class MethodCodeTooLarge(Exception):
    pass


class Function(Block):
    def __init__(self, parent, name, code, parameters, returns, static=False):
        super().__init__(parent=parent)
        self.name = name

        # Python can redefine function symbols. Keep a track of any
        # function that is defined; if the symbol has already been
        # defined in this context, then append $n to the symbol in
        # the Java classfile.
        duplicates = self._parent.symbols.setdefault(self.name, [])
        duplicates.append(self.method_name)
        if len(duplicates) > 1:
            self._java_suffix = '$%d' % (len(duplicates) - 1)
        else:
            self._java_suffix = ''

        self.code = code
        self.parameters = parameters
        self.returns = returns

        # Reserve space for the register that will hold self (if required)
        self.add_self()

        # Reserve space for the registers that will hold arguments.
        for i, param in enumerate(self.parameters):
            self.local_vars[param['name']] = len(self.local_vars)

        # Reserve space for the register that will hold locals
        self.local_vars['#locals'] = len(self.local_vars)

        self.static = static

    def __repr__(self):
        return '<Function %s (%s parameters)>' % (self.name, len(self.parameters))

    @property
    def is_constructor(self):
        return False

    def add_self(self):
        pass

    def store_module(self):
        # Stores the current module as a local variable
        if ('#module') not in self.local_vars:
            self.add_opcodes(
                JavaOpcodes.GETSTATIC('python/sys', 'modules', 'Lorg/python/types/Dict;'),

                python.Str(self.module.full_name),

                python.Object.get_item(),
                JavaOpcodes.CHECKCAST('org/python/types/Module'),

                ASTORE_name('#module'),
            )

    def store_name(self, name, declare=False):
        if declare or name in self.local_vars:
            self.add_opcodes(
                # Store in a local variable
                ASTORE_name(name),
            )
            self.add_opcodes(
                # Also store in the locals variable
                ALOAD_name('#locals'),
                JavaOpcodes.LDC_W(name),
                ALOAD_name(name),
                java.Map.put(),
            )
        else:
            self.add_opcodes(
                ASTORE_name('#value'),

                ALOAD_name('#module'),

                ALOAD_name('#value'),

                python.Object.set_attr(name),
                free_name('#value')
            )

    def store_dynamic(self):
        raise NotImplementedError('Functions cannot dynamically store variables.')

    def load_name(self, name):
        if name in self.local_vars:
            self.add_opcodes(
                ALOAD_name('#locals'),
                java.Map.get(name),
                JavaOpcodes.DUP(),
                IF([], JavaOpcodes.IFNONNULL),
                java.THROW(
                    'org/python/exceptions/UnboundLocalError',
                    ['Ljava/lang/String;', JavaOpcodes.LDC_W(name)]
                ),
                END_IF(),
            )
        else:
            self.add_opcodes(
                ALOAD_name('#module'),
                python.Object.get_attribute(name),
            )

    def load_globals(self):
        self.add_opcodes(
            ALOAD_name('#module'),
            JavaOpcodes.GETFIELD('org/python/types/Module', '__dict__', 'Ljava/util/Map;'),
        )

    def load_locals(self):
        self.add_opcodes(
            ALOAD_name('#locals')
        )

    def load_vars(self):
        self.load_locals()

    def delete_name(self, name):
        try:
            self.add_opcodes(
                free_name(name),
                ALOAD_name('#locals'),
                java.Map.remove(name)
            )
        except NameError:
            self.add_opcodes(
                ALOAD_name('#module'),
                python.Object.del_attr(name),
            )

    @property
    def can_ignore_empty(self):
        return False

    @property
    def signature(self):
        return_descriptor = 'Lorg/python/Object;'
        return '(%s)%s' % (
            ''.join('Lorg/python/Object;' for p in self.parameters),
            return_descriptor
        )

    @property
    def method_name(self):
        return self.name

    @property
    def java_name(self):
        return self.name + self._java_suffix

    @property
    def pyimpl_name(self):
        return self.name + self._java_suffix

    @property
    def module(self):
        return self._parent

    @property
    def class_descriptor(self):
        return self.module.class_descriptor

    def add_class(self, class_name, extends, implements):
        from .klass import Class

        klass = Class(
            self.module,
            name=class_name,
            extends=extends,
            implements=implements
        )

        self.module.classes.append(klass)

        self.add_opcodes(
            # Stack contains the bases list
            ASTORE_name('#bases'),

            # DEBUG("FORCE LOAD OF CLASS %s AT DEFINITION" % klass.descriptor),
            # - class
            JavaOpcodes.LDC_W(JavaClassref(klass.descriptor)),

            # - name
            JavaOpcodes.LDC_W(klass.name),

            # - bases
            ALOAD_name('#bases'),

            # - dict
            JavaOpcodes.ACONST_NULL(),

            JavaOpcodes.INVOKESTATIC(
                'org/python/types/Type',
                'declarePythonType',
                args=[
                    'Ljava/lang/Class;',
                    'Ljava/lang/String;',
                    'Ljava/util/List;',
                    'Ljava/util/Map;'
                ],
                returns='Lorg/python/types/Type;'
            ),

            free_name('#bases')
        )

        self.store_name(klass.name)

        self.add_opcodes(
            JavaOpcodes.INVOKESTATIC(
                klass.descriptor,
                'class$init',
                args=[],
                returns='V'
            ),
        )

        return klass

    def add_function(self, name, code, parameter_signatures, return_signature):
        # If a function is added to a function, it is added as an anonymous
        # inner class to the function/method's parent module/class.
        from .klass import ClosureClass
        if not (isinstance(self, Closure) or isinstance(self, GeneratorClosure)):
            # prepend name to first level nested function
            name = self.name + '$' + name

        klass = ClosureClass(
            parent=self._parent,
            name=name,
        )
        self.module.classes.append(klass)

        klass.visitor_setup()

        if hasattr(self, "outer_contexts") and self.outer_contexts:
            outer_contexts = self.outer_contexts + [self]
        else:
            outer_contexts = [self]

        if code.co_flags & CO_GENERATOR:
            closure = GeneratorClosure(
                klass,
                code=code,
                generator=code.co_name,
                parameters=parameter_signatures,
                returns=return_signature,
                outer_contexts=outer_contexts
            )
        else:
            closure = Closure(
                klass,
                code=code,
                parameters=parameter_signatures,
                returns=return_signature,
                outer_contexts=outer_contexts
            )

        klass.methods.append(closure)

        for field in code.co_names:
            klass.fields[field] = 'Lorg/python/Object;'

        klass.visitor_teardown()

        # closure has reference to outer context's local variables by maintaining a list of #locals
        self.add_opcodes(
            java.New(klass.descriptor),
            java.List(),
            JavaOpcodes.DUP(),
            ALOAD_name('#locals'),
            java.List.add(),
        )

        if isinstance(self, Closure):
            self.add_opcodes(
                JavaOpcodes.DUP(),
                ALOAD_name('<closure>'),
                JavaOpcodes.CHECKCAST('org/python/types/Closure'),
                JavaOpcodes.GETFIELD('org/python/types/Closure', 'locals_list', 'Ljava/util/List;'),
                java.List.addAll(),
            )
        elif isinstance(self, GeneratorClosure):
            self.add_opcodes(
                JavaOpcodes.DUP(),
                ALOAD_name('<generator>'),
                JavaOpcodes.CHECKCAST('org/python/types/Generator'),
                JavaOpcodes.GETFIELD('org/python/types/Generator', 'closure', 'Lorg/python/types/Closure;'),
                JavaOpcodes.GETFIELD('org/python/types/Closure', 'locals_list', 'Ljava/util/List;'),
                java.List.addAll(),
            )

        self.add_opcodes(
            java.Init(klass.descriptor, 'Ljava/util/List;'),

            python.Type.for_name(klass.descriptor),
        )

        self.add_callable(closure)

        self.add_opcodes(
            python.Object.set_attr('invoke'),
            python.Object.get_attribute('invoke'),
        )

        return closure

    def visitor_setup(self):
        self.add_opcodes(
            java.Map(),
            ASTORE_name('#locals')
        )

        # stores parameters in #locals
        for param in self.parameters:
            self.add_opcodes(
                ALOAD_name('#locals'),
                JavaOpcodes.LDC_W(param['name']),
                ALOAD_name(param['name']),
                java.Map.put(),
            )

        self.store_module()

    def visitor_teardown(self):
        if len(self.opcodes) == 0:
            # If there is no content in this method, add a RETURN.
            return_required = True
        elif isinstance(self.opcodes[-1], (JavaOpcodes.RETURN, JavaOpcodes.ARETURN)):
            # If the last opcode in the method is a RETURN, but that
            # return was not added at the root level (i.e., it's not a return
            # as the last statement of an IF statement), add one.
            try:
                return_required = self.opcodes[-1].needs_implicit_return
            except AttributeError:
                return_required = True
        else:
            # If the last statement in the block isn't a RETURN, add one.
            return_required = True

        if return_required:
            self.add_opcodes(
                python.NONE(),
                JavaOpcodes.ARETURN()
            )

    def method_attributes(self):
        return [
            RuntimeVisibleAnnotations([
                Annotation(
                    'Lorg/python/Method;',
                    {
                        '__doc__': ConstantElementValue("Python method (insert docs here)")
                    }
                )
            ])
        ]

    def transpile_method(self):
        try:
            return [
                JavaMethod(
                    self.pyimpl_name,
                    self.signature,
                    static=self.static,
                    attributes=[self.transpile_code()] + self.method_attributes()
                )
            ]
        except BlockCodeTooLarge as e:
            raise MethodCodeTooLarge("Code is too large for method %s: %d > 65534"
                                     % (self.name, e.code_length))

    def transpile_wrapper(self):
        return []

    def transpile(self):
        return self.transpile_method() + self.transpile_wrapper()


class InitMethod(Function):
    def __init__(self, klass, args=None, super_args=None, parameters=None):
        super().__init__(
            klass,
            name='<init>',
            code=None,
            parameters=parameters if parameters else [
                {
                    'name': 'self',
                    'kind': ArgType.POSITIONAL_OR_KEYWORD,
                    'annotation': 'org/python/Object'
                },
                {
                    'name': 'args',
                    'kind': ArgType.VAR_POSITIONAL,
                    'annotation': '[Lorg/python/Object;'
                },
                {
                    'name': 'kwargs',
                    'kind': ArgType.VAR_KEYWORD,
                    'annotation': 'java/util/Map'
                }
            ],
            returns={'annotation': None},
        )
        self.args = args if args else {}
        self.super_args = super_args if super_args else []

        self.store_module()

    def __repr__(self):
        return '<Constructor %s (%s parameters)>' % (self.klass.name, len(self.parameters))

    @property
    def is_constructor(self):
        return True

    @property
    def klass(self):
        return self._parent

    @property
    def module(self):
        return self.klass.module

    @property
    def class_descriptor(self):
        return self.klass.descriptor

    @property
    def can_ignore_empty(self):
        return False

    @property
    def signature(self):
        return '([Lorg/python/Object;Ljava/util/Map;)V'

    def load_name(self, name):
        if name in self.args:
            index = self.args[name]
            if index is None:
                self.add_opcodes(
                    JavaOpcodes.ALOAD_2(),
                    java.Map.get(name)
                )
            else:
                self.add_opcodes(
                    JavaOpcodes.ALOAD_1(),
                    java.Array.get(index),
                )
        else:
            self.add_opcodes(
                ALOAD_name('#module'),
                python.Object.get_attribute(name),
            )

    def visitor_setup(self):
        # Construct the contents of the constructor method...
        self.add_opcodes(
            # Create the instance
            JavaOpcodes.ALOAD_0(),
            JavaOpcodes.DUP(),
        )

    def visitor_teardown(self):
        self.add_opcodes(
            java.Init(self.klass.extends_descriptor, *[descriptor(arg) for arg in self.super_args]),
            python.Type.to_python(),

            python.Object.get_attribute('__init__', use_null=True),
            # If no __init__ exists, just return.
            JavaOpcodes.DUP(),
            JavaOpcodes.IFNULL(13),  # 3

            # Check that it is a callable
            JavaOpcodes.CHECKCAST('org/python/Callable'),  # 3

            # ...and invoke it
            JavaOpcodes.ALOAD_1(),  # 1
            JavaOpcodes.ALOAD_2(),  # 1
            python.Callable.invoke(),  # 5

            JavaOpcodes.POP(),  # 1

            JavaOpcodes.RETURN()
        )


class Method(Function):
    def __init__(self, klass, name, code, parameters, returns=None, static=False):
        super().__init__(
            klass,
            name=name,
            code=code,
            parameters=parameters,
            returns=returns,
            static=static,
        )

        self.store_module()

    def __repr__(self):
        return '<Method %s.%s (%s parameters)>' % (self.klass.name, self.name, len(self.parameters))

    @property
    def pyimpl_name(self):
        return self.java_name + "$py" + self._java_suffix

    @property
    def klass(self):
        return self._parent

    @property
    def module(self):
        return self.klass.module

    @property
    def class_descriptor(self):
        return self.klass.descriptor

    @property
    def bound_signature(self):
        return_descriptor = descriptor(self.returns.get('annotation'))
        return '(%s)%s' % (
            ''.join(descriptor(p['annotation']) for p in self.parameters[1:]),
            return_descriptor
        )

    def transpile_wrapper(self, local_vars=None):
        # The first register holds "self"; since the binding is only
        # invoked via a native call, wrap it in a Java Object - unless
        # the object is an extension type, in which case the wrapper
        # object should already exist.
        binding = Accumulator(local_vars if local_vars is not None
                              else self.local_vars)

        binding.add_opcodes(
            # DEBUG("BINDING FOR " + self.name + self.signature),
            # DEBUG("BOUND AS " + self.name + self.bound_signature),
            # JavaOpcodes.ALOAD_0(),
            # DEBUG_value("BINDING SELF IN"),

            JavaOpcodes.ALOAD_0(),
            python.Type.to_python(),  # 3

            # DEBUG_value("BINDING SELF OUT", dup=True),
        )

        # Then extract each argument, converting to Python types as required.
        for i, param in enumerate(self.parameters[1:]):
            if param['annotation'] is None:
                raise Exception("Parameters can't be void")
            else:
                to_python(binding, param['annotation'], param['name'])
            # binding.add_opcodes(
            #     DEBUG("INPUT %s TRANSFORMED" % (i)),
            # )
        # binding.add_opcodes(
        #     DEBUG("INPUTS TRANSFORMED"),
        # )

        # Then call the method, and process the return type.
        binding.add_opcodes(
            JavaOpcodes.INVOKESTATIC(self.klass.descriptor, self.pyimpl_name, self.signature),
        )

        to_java(binding, self.returns['annotation'])
        return_statement(binding, self.returns['annotation'])

        # binding.add_opcodes(
        #     DEBUG("BINDING OUTPUT to type %s" % self.returns['annotation']),
        # )

        wrapper_methods = [
            JavaMethod(
                self.java_name,
                self.bound_signature,
                attributes=[
                    JavaCode(
                        max_stack=len(self.parameters) + 5,
                        max_locals=len(self.parameters),
                        code=binding.opcodes
                    )
                ]
            ),
        ]

        if self.klass.extends:
            # We also need to generate a manual call to the super
            super_wrapper = Accumulator()
            super_wrapper.add_opcodes(
                JavaOpcodes.ALOAD_0(),
            )

            # Then extract each argument:
            for i, param in enumerate(self.parameters[1:]):
                super_wrapper.add_opcodes({
                        'bool': JavaOpcodes.ILOAD(i + 1),
                        'byte': JavaOpcodes.ILOAD(i + 1),
                        'char': JavaOpcodes.ILOAD(i + 1),
                        'short': JavaOpcodes.ILOAD(i + 1),
                        'int': JavaOpcodes.ILOAD(i + 1),
                        'long': JavaOpcodes.ILOAD(i + 1),
                        'float': JavaOpcodes.FLOAD(i + 1),
                        'double': JavaOpcodes.DLOAD(i + 1),
                    }.get(param['annotation'], JavaOpcodes.ALOAD(i + 1))
                )

            # Then call the method, and process the return type.
            super_wrapper.add_opcodes(
                JavaOpcodes.INVOKESPECIAL(self.klass.extends.replace('.', '/'), self.name, self.bound_signature),

                {
                    'void': JavaOpcodes.RETURN(),
                    'bool': JavaOpcodes.IRETURN(),
                    'byte': JavaOpcodes.IRETURN(),
                    'char': JavaOpcodes.IRETURN(),
                    'short': JavaOpcodes.IRETURN(),
                    'int': JavaOpcodes.IRETURN(),
                    'long': JavaOpcodes.LRETURN(),
                    'float': JavaOpcodes.FRETURN(),
                    'double': JavaOpcodes.DRETURN(),
                }.get(self.returns['annotation'], JavaOpcodes.ARETURN()),

                # DEBUG("SUPER WRAPPER OUTPUT to type %s" % self.returns['annotation']),
            )

            wrapper_methods.append(
                JavaMethod(
                    self.java_name + "$super",
                    self.bound_signature,
                    attributes=[
                        JavaCode(
                            max_stack=len(self.parameters) + 2,
                            max_locals=len(self.parameters) + 2,
                            code=super_wrapper.opcodes
                        )
                    ]
                )
            )

        return wrapper_methods


class MainFunction(Function):
    def __init__(self, module):
        super().__init__(
            module,
            name='__main__',
            code=None,
            parameters=[{'name': 'args', 'annotation': 'argv'}],
            returns={'annotation': None},
            static=True,
        )

    def __repr__(self):
        return '<MainFunction %s>' % self.module.name

    @property
    def java_name(self):
        return 'main'

    @property
    def pyimpl_name(self):
        return self.java_name

    @property
    def module(self):
        return self._parent

    @property
    def signature(self):
        return '([Ljava/lang/String;)V'

    @property
    def can_ignore_empty(self):
        return True

    def store_name(self, name, declare=False):
        self.add_opcodes(
            ASTORE_name('#value'),
            ALOAD_name('#module'),  # #module is available as a local var after visitor_setup has been called

            ALOAD_name('#value'),
            python.Object.set_attr(name),
            free_name('#value')
        )

    def store_dynamic(self):
        self.add_opcodes(
            ASTORE_name('#value'),
            python.Type.for_name(self.module.class_name),
            JavaOpcodes.GETFIELD('org/python/types/Type', '__dict__', 'Ljava/util/Map;'),
            ALOAD_name('#value'),

            java.Map.putAll(),
            free_name('#value')
        )

    def load_name(self, name):
        self.add_opcodes(
            ALOAD_name('#module'),  # #module is available as a local var after visitor_setup has been called
            python.Object.get_attribute(name),
        )

    def delete_name(self, name):
        self.add_opcodes(
            ALOAD_name('#module'),  # #module is available as a local var after visitor_setup has been called
            python.Object.del_attr(name),
        )

    def visitor_setup(self):
        self.add_opcodes(
            # Add a TRY-CATCH for SystemExit
            TRY(),
        )
        self.add_opcodes(
                # Set the Python version
                JavaOpcodes.LDC_W(sys.hexversion),
                JavaOpcodes.PUTSTATIC('org/Python', 'VERSION', 'I'),

                # Construct this module
                java.New(self.module.class_descriptor),
                java.Init(self.module.class_descriptor),
                ASTORE_name('#module'),

                # Register the module by it's full name
                JavaOpcodes.GETSTATIC('python/sys', 'modules', 'Lorg/python/types/Dict;'),
                python.Str(self.module.full_name),
                ALOAD_name('#module'),
                python.Object.set_item(),

                # Register the same module as __main__
                JavaOpcodes.GETSTATIC('python/sys', 'modules', 'Lorg/python/types/Dict;'),
                python.Str('__main__'),
                ALOAD_name('#module'),
                python.Object.set_item(),

                # Set the module's __name__
                ALOAD_name('#module'),
                python.Str("__main__"),
                python.Object.set_attr('__name__'),

                # Set the module's __package__
                ALOAD_name('#module'),
                python.NONE(),
                python.Object.set_attr("__package__"),

                # Run the module block.
                ALOAD_name('#module'),
                JavaOpcodes.INVOKEVIRTUAL(self.module.class_descriptor, 'module$import', args=[], returns='V'),
        )

    def visitor_teardown(self):
        # Close out the TRY-CATCH for SystemExit
        self.add_opcodes(
            CATCH('org/python/exceptions/SystemExit'),
        )
        self.add_opcodes(
                JavaOpcodes.GETFIELD('org/python/exceptions/SystemExit', 'return_code', 'I'),
                JavaOpcodes.INVOKESTATIC('java/lang/System', 'exit', args=['I'], returns='V'),
        )
        self.add_opcodes(
            END_TRY(),
            JavaOpcodes.RETURN()
        )

    def method_attributes(self):
        return []


def _get_enclosing_context_level(child_context, name):
    # returns level of enclosing context that defined the variable `name`
    # i.e. level = 2 means `name` is found two levels up from the nested `child_context`
    if name in child_context.local_vars:
        return None
    else:
        level = 0
        for context in child_context.outer_contexts[::-1]:
            level += 1
            if name in context.local_vars and context.local_vars[name] is not None:
                return level

    return None


class Closure(Function):
    def __init__(self, klass, code, parameters, returns=None, static=False, outer_contexts=None):
        super().__init__(
            klass,
            name='invoke',
            code=code,
            parameters=parameters,
            returns=returns,
            static=static,
        )
        self.nonlocal_vars = []  # holds nonlocal variable names for `store_name`
        self.outer_contexts = outer_contexts  # parent scopes of this closure, excluding global scope

        self.store_module()

    def __repr__(self):
        return '<Closure %s (%s parameters)>' % (self.name, len(self.parameters))

    def store_name(self, name, declare=False):
        if name in self.nonlocal_vars:
            # updates closure
            self.add_opcodes(
                ALOAD_name('<closure>'),
                JavaOpcodes.CHECKCAST('org/python/types/Closure'),
                ICONST_val(_get_enclosing_context_level(self, name)),
                JavaOpcodes.INVOKEVIRTUAL(
                    'org/python/types/Closure',
                    'get_locals',
                    args=['I'],
                    returns='Ljava/util/Map;'
                ),
                JavaOpcodes.SWAP(),
                JavaOpcodes.LDC_W(name),
                JavaOpcodes.SWAP(),
                java.Map.put()
            )
        else:
            super().store_name(name, declare)

    def load_name(self, name):
        parent_level = _get_enclosing_context_level(self, name)
        if parent_level:
            self.add_opcodes(
                ALOAD_name('<closure>'),
                JavaOpcodes.CHECKCAST('org/python/types/Closure'),
                ICONST_val(parent_level),
                JavaOpcodes.INVOKEVIRTUAL(
                    'org/python/types/Closure',
                    'get_locals',
                    args=['I'],
                    returns='Ljava/util/Map;'
                ),
                java.Map.get(name),
            )
        else:
            super().load_name(name)

    @property
    def klass(self):
        return self._parent

    @property
    def module(self):
        return self.klass.module

    @property
    def class_descriptor(self):
        return self.klass.descriptor

    def add_self(self):
        # In a closure method, the first argument is the closure,
        # not self. self *might* be the first argument -- but in
        # that case, it's just the first argument in an unbound
        # method.
        self.local_vars['<closure>'] = len(self.local_vars)
        self.has_self = True


class ClosureInitMethod(InitMethod):
    def __init__(self, klass):
        super().__init__(
            klass,
            parameters=[
                {
                    'name': 'self',
                    'kind': ArgType.POSITIONAL_OR_KEYWORD,
                    'annotation': 'org/python/Object'
                },
                {
                    'name': 'kwargs',
                    'kind': ArgType.VAR_KEYWORD,
                    'annotation': 'java/util/Map'
                }
            ],
        )

    def __repr__(self):
        return '<Closure constructor %s (%s parameters)>' % (self.klass.name, len(self.parameters))

    @property
    def signature(self):
        return '(Ljava/util/List;)V'

    def visitor_teardown(self):
        self.add_opcodes(
            JavaOpcodes.ALOAD_1(),
            java.Init(self.klass.extends_descriptor, 'Ljava/util/List;'),

            JavaOpcodes.RETURN()
        )


class GeneratorFunction(Function):
    def __init__(self, module, name, code, generator, parameters, returns=None, static=False):
        super().__init__(
            module,
            name=name,
            code=code,
            parameters=parameters,
            returns=returns,
            static=static,
        )
        self.generator = generator

    @property
    def klass(self):
        return self.module

    def add_self(self):
        self.local_vars['<generator>'] = len(self.local_vars)
        self.has_self = True

    def visitor_setup(self):
        self.add_opcodes(
            # Restore the variables needed for the entry of the generator.
            ALOAD_name('<generator>'),
            JavaOpcodes.GETFIELD('org/python/types/Generator', 'stack', 'Ljava/util/Map;'),
            ASTORE_name('#locals'),
        )

        for param in self.parameters:
            self.add_opcodes(
                ALOAD_name('#locals'),
                java.Map.get(param['name']),
                ASTORE_name(param['name'])
            )

    def visitor_teardown(self):
        # implicit return for generator
        # PEP 380: return statement in generator is equivalent to raise StopIteration(value)
        # if not isinstance(self.opcodes[-1], (JavaOpcodes.ATHROW, JavaOpcodes.ARETURN)):
        # TODO: Uncomment the condition above once the issue described is resolved:
        # TODO: Currently need to throw StopIteration at the end of generator even when ATHROW/ARETURN is the last
        # TODO: instruction, to fix "'TRY' object has no attribute 'next_op'" error during transpilation
        self.add_opcodes(
            # StopIteration is a singleton by design, see org/python/exceptions/StopIteration
            JavaOpcodes.GETSTATIC(
                'org/python/exceptions/StopIteration', 'STOPITERATION', 'Lorg/python/exceptions/StopIteration;'
            ),
            JavaOpcodes.ATHROW(),
        )

    def transpile_method(self):
        return [
            JavaMethod(
                self.method_name + "$generator",
                '(Lorg/python/types/Generator;)Lorg/python/Object;',
                static=True,
                attributes=[self.transpile_code()] + self.method_attributes()
            )
        ]

    def transpile_wrapper(self):
        wrapper = Accumulator()

        wrapper.add_opcodes(
            # Construct a generator instance
            java.New('org/python/types/Generator'),

            # p1: The name of the generator
            JavaOpcodes.LDC_W(self.generator),

            # p2: The actual generator method
            java.Class.forName(self.class_descriptor.replace('/', '.')),

            JavaOpcodes.LDC_W(self.method_name + "$generator"),
            java.Array(1, 'java/lang/Class'),

            JavaOpcodes.DUP(),
            ICONST_val(0),
            java.Class.forName('org.python.types.Generator'),
            JavaOpcodes.AASTORE(),

            JavaOpcodes.INVOKEVIRTUAL(
                'java/lang/Class',
                'getMethod',
                args=['Ljava/lang/String;', '[Ljava/lang/Class;'],
                returns='Ljava/lang/reflect/Method;'
            ),

            # p3: The arguments passed to the generator method. These will be
            # restored on the first call to the generator.
            java.Map(),
        )

        for i, param in enumerate(self.parameters):
            wrapper.add_opcodes(
                JavaOpcodes.DUP(),
                JavaOpcodes.LDC_W(param['name']),

                JavaOpcodes.ALOAD(i + (0 if self.static else 1)),
                java.Map.put(),
            )

        if isinstance(self, GeneratorClosure):
            # stores a copy of closure variables
            wrapper.add_opcodes(
                JavaOpcodes.ALOAD_0(),  # first register contains initialized Closure object reference
                JavaOpcodes.CHECKCAST('org/python/types/Closure')
            )
            wrapper.add_opcodes(
                java.Init(
                    'org/python/types/Generator',
                    'Ljava/lang/String;',
                    'Ljava/lang/reflect/Method;',
                    'Ljava/util/Map;',
                    'Lorg/python/types/Closure;'
                ),
                JavaOpcodes.ARETURN(),
            )
        else:
            # Construct and return the generator object.
            wrapper.add_opcodes(
                java.Init(
                    'org/python/types/Generator',
                    'Ljava/lang/String;',
                    'Ljava/lang/reflect/Method;',
                    'Ljava/util/Map;'
                ),
                JavaOpcodes.ARETURN(),
            )

        return [
            JavaMethod(
                self.method_name,
                self.signature,
                static=self.static,
                attributes=[
                    JavaCode(
                        max_stack=len(self.parameters) + 9,
                        max_locals=len(self.parameters) + 8,
                        code=wrapper.opcodes
                    )
                ]
            )
        ]

    def store_name(self, name, declare=False):
        if declare or name in self.local_vars:
            self.add_opcodes(
                # Store in a local variable
                ASTORE_name(name),
            )
            self.add_opcodes(
                # Also store in the locals variable
                ALOAD_name('#locals'),
                JavaOpcodes.LDC_W(name),
                ALOAD_name(name),
                java.Map.put(),
            )
        else:
            # Unlike other Functions, GeneratorFunctions do not cache the current Module
            # locally, so it must be fetched on each use.
            self.add_opcodes(
                ASTORE_name('#value'),

                JavaOpcodes.GETSTATIC('python/sys', 'modules', 'Lorg/python/types/Dict;'),

                python.Str(self.module.full_name),

                python.Object.get_item(),
                JavaOpcodes.CHECKCAST('org/python/types/Module'),

                ALOAD_name('#value'),

                python.Object.set_attr(name),
                free_name('#value')
            )

    def load_name(self, name):
        if name == '<generator>':  # `<generator>` is not included in #locals
            self.add_opcodes(
                ALOAD_name(name)
            )
        elif name in self.local_vars:
            self.add_opcodes(
                ALOAD_name('#locals'),
                java.Map.get(name),
            )
        else:
            # Unlike other Functions, GeneratorFunctions do not cache the current Module
            # locally, so it must be fetched on each use.
            self.add_opcodes(
                JavaOpcodes.GETSTATIC('python/sys', 'modules', 'Lorg/python/types/Dict;'),

                python.Str(self.module.full_name),

                python.Object.get_item(),
                JavaOpcodes.CHECKCAST('org/python/types/Module'),
                python.Object.get_attribute(name),
            )

    def delete_name(self, name):
        try:
            self.add_opcodes(
                free_name(name),
                ALOAD_name('#locals'),
                java.Map.remove(name)
            )
        except NameError:
            # Unlike other Functions, GeneratorFunctions do not cache the current Module
            # locally, so it must be fetched on each use.
            self.add_opcodes(
                JavaOpcodes.GETSTATIC('python/sys', 'modules', 'Lorg/python/types/Dict;'),

                python.Str(self.module.full_name),

                python.Object.get_item(),
                JavaOpcodes.CHECKCAST('org/python/types/Module'),
                python.Object.del_attr(name),
            )


class GeneratorMethod(Method):
    def __init__(self, klass, name, code, generator, parameters, returns=None, static=False):
        super().__init__(
            klass,
            name=name,
            code=code,
            parameters=parameters,
            returns=returns,
            static=static,
        )
        self.generator = generator

    @property
    def klass(self):
        return self._parent

    def add_self(self):
        self.local_vars['<generator>'] = len(self.local_vars)
        self.has_self = True

    def visitor_setup(self):
        self.add_opcodes(
            # Restore the variables needed for the entry of the generator.
            ALOAD_name('<generator>'),
            JavaOpcodes.GETFIELD('org/python/types/Generator', 'stack', 'Ljava/util/Map;'),
            ASTORE_name('#locals'),
        )

        for param in self.parameters:
            self.add_opcodes(
                ALOAD_name('#locals'),
                java.Map.get(param['name']),
                ASTORE_name(param['name'])
            )

    def visitor_teardown(self):
        # implicit return for generator
        # PEP 380: return statement in generator is equivalent to raise StopIteration(value)
        # if not isinstance(self.opcodes[-1], (JavaOpcodes.ATHROW, JavaOpcodes.ARETURN)):
        # TODO: Uncomment the condition above once the issue described is resolved:
        # TODO: Currently need to throw StopIteration at the end of generator even when ATHROW/ARETURN is the last
        # TODO: instruction, to fix "'TRY' object has no attribute 'next_op'" error during transpilation
        self.add_opcodes(
            # StopIteration is a singleton by design, see org/python/exceptions/StopIteration
            JavaOpcodes.GETSTATIC(
                'org/python/exceptions/StopIteration', 'STOPITERATION', 'Lorg/python/exceptions/StopIteration;'
            ),
            JavaOpcodes.ATHROW(),
        )

    def transpile_method(self):
        return [
            JavaMethod(
                self.method_name + "$generator",
                '(Lorg/python/types/Generator;)Lorg/python/Object;',
                static=True,
                attributes=[self.transpile_code()] + self.method_attributes()
            )
        ]

    def transpile_wrapper(self):
        wrapper = Accumulator()

        wrapper.add_opcodes(
            # Construct a generator instance
            java.New('org/python/types/Generator'),

            # p1: The name of the generator
            JavaOpcodes.LDC_W(self.generator),

            # p2: The actual generator method
            java.Class.forName(self.klass.class_name),

            JavaOpcodes.LDC_W(self.method_name + "$generator"),
            java.Array(1, 'java/lang/Class'),

            JavaOpcodes.DUP(),
            ICONST_val(0),
            java.Class.forName('org.python.types.Generator'),
            JavaOpcodes.AASTORE(),

            JavaOpcodes.INVOKEVIRTUAL(
                'java/lang/Class',
                'getMethod',
                args=['Ljava/lang/String;', '[Ljava/lang/Class;'],
                returns='Ljava/lang/reflect/Method;'
            ),

            # p3: The arguments passed to the generator method. These will be
            # restored on the first call to the generator.
            java.Map(),
        )

        for i, param in enumerate(self.parameters, 0 if self.static else 1):
            wrapper.add_opcodes(
                JavaOpcodes.DUP(),
                JavaOpcodes.LDC_W(param['name']),

                JavaOpcodes.ALOAD(i),
                java.Map.put(),
            )
            wrapper.local_vars[param['name']] = i

        # Construct and return the generator object.
        wrapper.add_opcodes(
            java.Init(
                'org/python/types/Generator',
                'Ljava/lang/String;',
                'Ljava/lang/reflect/Method;',
                'Ljava/util/Map;',
            ),
            JavaOpcodes.ARETURN(),
        )

        return super().transpile_wrapper(wrapper.local_vars) + [
            JavaMethod(
                self.pyimpl_name,
                self.signature,
                static=self.static,
                attributes=[
                    JavaCode(
                        max_stack=len(self.parameters) + 9,
                        max_locals=len(self.parameters) + 8,
                        code=wrapper.opcodes
                    )
                ]
            )
        ]

    def store_name(self, name, declare=False):
        if declare or name in self.local_vars:
            self.add_opcodes(
                # Store in a local variable
                ASTORE_name(name),
            )
            self.add_opcodes(
                # Also store in the locals variable
                ALOAD_name('#locals'),
                JavaOpcodes.LDC_W(name),
                ALOAD_name(name),
                java.Map.put(),
            )
        else:
            # Unlike other Functions, GeneratorFunctions do not cache the current Module
            # locally, so it must be fetched on each use.
            self.add_opcodes(
                ASTORE_name('#value'),

                JavaOpcodes.GETSTATIC('python/sys', 'modules', 'Lorg/python/types/Dict;'),

                python.Str(self.module.full_name),

                python.Object.get_item(),
                JavaOpcodes.CHECKCAST('org/python/types/Module'),

                ALOAD_name('#value'),

                python.Object.set_attr(name),
                free_name('#value')
            )

    def load_name(self, name):
        if name == '<generator>':  # `<generator>` is not included in #locals
            self.add_opcodes(
                ALOAD_name(name)
            )
        else:
            super().load_name(name)

    def delete_name(self, name):
        try:
            self.add_opcodes(
                free_name(name)
            )
        except NameError:
            # Unlike other Functions, GeneratorFunctions do not cache the current Module
            # locally, so it must be fetched on each use.
            self.add_opcodes(
                JavaOpcodes.GETSTATIC('python/sys', 'modules', 'Lorg/python/types/Dict;'),

                python.Str(self.module.full_name),

                python.Object.get_item(),
                JavaOpcodes.CHECKCAST('org/python/types/Module'),
                python.Object.del_attr(name),
            )


class GeneratorClosure(GeneratorFunction):
    def __init__(self, module, code, generator, parameters, returns=None, static=False, outer_contexts=None):
        super().__init__(
            module,
            name='invoke',
            code=code,
            generator=generator,
            parameters=parameters,
            returns=returns,
            static=static,
        )
        self.nonlocal_vars = []  # holds nonlocal variable names for `store_name`
        self.outer_contexts = outer_contexts  # parent scopes of this closure, excluding global scope

    def __repr__(self):
        return '<GeneratorClosure %s (%s parameters)>' % (
            self.name, len(self.parameters)
        )

    @property
    def klass(self):
        return self._parent

    @property
    def module(self):
        return self.klass.module

    @property
    def class_descriptor(self):
        return self.klass.descriptor

    def store_name(self, name, declare=False):
        if name in self.nonlocal_vars:
            # updates closure
            self.add_opcodes(
                ALOAD_name('<generator>'),
                JavaOpcodes.CHECKCAST('org/python/types/Generator'),
                JavaOpcodes.GETFIELD('org/python/types/Generator', 'closure', 'Lorg/python/types/Closure;'),
                ICONST_val(_get_enclosing_context_level(self, name)),
                JavaOpcodes.INVOKEVIRTUAL(
                    'org/python/types/Closure',
                    'get_locals',
                    args=['I'],
                    returns='Ljava/util/Map;'
                ),
                JavaOpcodes.SWAP(),
                JavaOpcodes.LDC_W(name),
                JavaOpcodes.SWAP(),
                java.Map.put()
            )
        else:
            super().store_name(name, declare)

    def load_name(self, name):
        parent_level = _get_enclosing_context_level(self, name)

        if parent_level:
            self.add_opcodes(
                ALOAD_name('<generator>'),
                JavaOpcodes.CHECKCAST('org/python/types/Generator'),
                JavaOpcodes.GETFIELD('org/python/types/Generator', 'closure', 'Lorg/python/types/Closure;'),
                ICONST_val(parent_level),
                JavaOpcodes.INVOKEVIRTUAL(
                    'org/python/types/Closure',
                    'get_locals',
                    args=['I'],
                    returns='Ljava/util/Map;'
                ),
                java.Map.get(name),
            )
        else:
            super().load_name(name)
