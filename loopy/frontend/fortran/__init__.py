from __future__ import division, with_statement

__copyright__ = "Copyright (C) 2013 Andreas Kloeckner"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from loopy.diagnostic import LoopyError


def f2loopy(source, free_form=True, strict=True,
        pre_transform_code=None, pre_transform_code_context=None,
        use_c_preprocessor=False,
        file_name="<floopy code>"):
    if use_c_preprocessor:
        try:
            import ply.lex as lex
            import ply.cpp as cpp
        except ImportError:
            raise LoopyError("Using the C preprocessor requires PLY to be installed")

        lexer = lex.lex(cpp)

        from ply.cpp import Preprocessor
        p = Preprocessor(lexer)
        p.parse(source, file_name)

        tokens = []
        while True:
            tok = p.token()

            if not tok:
                break

            if tok.type == "CPP_COMMENT":
                continue

            tokens.append(tok.value)

        source = "".join(tokens)

    from fparser import api
    tree = api.parse(source, isfree=free_form, isstrict=strict,
            analyze=False, ignore_comments=False)

    from loopy.frontend.fortran.translator import F2LoopyTranslator
    f2loopy = F2LoopyTranslator(file_name)
    f2loopy(tree)

    return f2loopy.make_kernels(pre_transform_code=pre_transform_code,
            pre_transform_code_context=pre_transform_code_context)

# vim: foldmethod=marker
