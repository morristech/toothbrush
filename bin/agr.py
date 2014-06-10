#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import click

sys.path.append('/Users/agr/Projects/odoo/odoo/')
sys.path.append('/Users/agr/Projects/odoo/.env/lib/python2.7/site-packages/')

class DB(object):
    def __init__(self, db):
        import openerp
        self._db = db
        self._pool = openerp.registry(db)
        self._cr = self._pool.cursor()
    def __getattr__(self, attr):
        model = attr.replace('_', '.')
        return self._pool[model]

@click.group()
def cli():
    pass


"""
A pretty-printing dump function for the ast module.  The code was copied from
the ast.dump function and modified slightly to pretty-print.

Alex Leone (acleone ~AT~ gmail.com), 2010-01-30
"""
import ast
def dump(node, annotate_fields=True, include_attributes=False, indent='  '):
    """
    Return a formatted dump of the tree in *node*.  This is mainly useful for
    debugging purposes.  The returned string will show the names and the values
    for fields.  This makes the code impossible to evaluate, so if evaluation is
    wanted *annotate_fields* must be set to False.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    *include_attributes* can be set to True.
    """
    def _format(node, level=0):
        if isinstance(node, ast.AST):
            fields = [(a, _format(b, level)) for a, b in ast.iter_fields(node)]
            if include_attributes and node._attributes:
                fields.extend([(a, _format(getattr(node, a), level))
                               for a in node._attributes])
            return ''.join([
                node.__class__.__name__,
                '(',
                ', '.join(('%s=%s' % field for field in fields)
                           if annotate_fields else
                           (b for a, b in fields)),
                ')'])
        elif isinstance(node, list):
            lines = ['[']
            lines.extend((indent * (level + 2) + _format(x, level + 2) + ','
                         for x in node))
            if len(lines) > 1:
                lines.append(indent * (level + 1) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(node)
    if not isinstance(node, ast.AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)

@cli.command()
@click.argument('code')
def ppast(code):
    """
    Print pretty ast.
    """
    """
    Used this before
    http://furius.ca/pubcode/pub/conf/lib/python/astpretty.py.html#download
    but now, just `pip install astor`
    """
    # print dump(ast.parse(code, filename=filename), include_attributes=True)
    print dump(ast.parse(code), include_attributes=True)


if __name__ == '__main__':
    cli()
