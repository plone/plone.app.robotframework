# -*- coding: utf-8 -*-
"""Standalone Python keyword-libraries"""


class LayoutMath:

    def get_offset_difference(self, source_offset, dest_offset, padding):
        """Return dest_offset - source_offset + padding"""
        return (int(dest_offset) - int(source_offset)) + int(padding)


class Debugging:

    def stop(self):
        """Pauses the test runner and drops it into Python debugger.
        Enter 'c' into debugger to continue.
        """
        import sys
        for attr in ('stdin', 'stdout', 'stderr'):
            setattr(sys, attr, getattr(sys, '__%s__' % attr))
        import pdb
        pdb.set_trace()
