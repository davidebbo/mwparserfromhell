# -*- coding: utf-8  -*-
#
# Copyright (C) 2012-2013 Ben Kurtovic <ben.kurtovic@verizon.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals
import unittest

from mwparserfromhell.nodes import (Argument, Comment, Heading, HTMLEntity,
                                    Tag, Template, Text, Wikilink)
from mwparserfromhell.nodes.extras import Attribute, Parameter
from mwparserfromhell.parser import tokens
from mwparserfromhell.parser.builder import Builder
from mwparserfromhell.smart_list import SmartList
from mwparserfromhell.wikicode import Wikicode

from ._test_tree_equality import TreeEqualityTestCase

wrap = lambda L: Wikicode(SmartList(L))

class TestBuilder(TreeEqualityTestCase):
    """Tests for the builder, which turns tokens into Wikicode objects."""

    def setUp(self):
        self.builder = Builder()

    def test_text(self):
        """tests for building Text nodes"""
        tests = [
            ([tokens.Text(text="foobar")], wrap([Text("foobar")])),
            ([tokens.Text(text="fóóbar")], wrap([Text("fóóbar")])),
            ([tokens.Text(text="spam"), tokens.Text(text="eggs")],
             wrap([Text("spam"), Text("eggs")])),
        ]
        for test, valid in tests:
            self.assertWikicodeEqual(valid, self.builder.build(test))

    def test_template(self):
        """tests for building Template nodes"""
        tests = [
            ([tokens.TemplateOpen(), tokens.Text(text="foobar"),
              tokens.TemplateClose()],
             wrap([Template(wrap([Text("foobar")]))])),

            ([tokens.TemplateOpen(), tokens.Text(text="spam"),
              tokens.Text(text="eggs"), tokens.TemplateClose()],
             wrap([Template(wrap([Text("spam"), Text("eggs")]))])),

            ([tokens.TemplateOpen(), tokens.Text(text="foo"),
              tokens.TemplateParamSeparator(), tokens.Text(text="bar"),
              tokens.TemplateClose()],
             wrap([Template(wrap([Text("foo")]), params=[
                 Parameter(wrap([Text("1")]), wrap([Text("bar")]),
                     showkey=False)])])),

            ([tokens.TemplateOpen(), tokens.Text(text="foo"),
              tokens.TemplateParamSeparator(), tokens.Text(text="bar"),
              tokens.TemplateParamEquals(), tokens.Text(text="baz"),
              tokens.TemplateClose()],
             wrap([Template(wrap([Text("foo")]), params=[
                 Parameter(wrap([Text("bar")]), wrap([Text("baz")]))])])),

            ([tokens.TemplateOpen(), tokens.Text(text="foo"),
              tokens.TemplateParamSeparator(), tokens.Text(text="bar"),
              tokens.TemplateParamEquals(), tokens.Text(text="baz"),
              tokens.TemplateParamSeparator(), tokens.Text(text="biz"),
              tokens.TemplateParamSeparator(), tokens.Text(text="buzz"),
              tokens.TemplateParamSeparator(), tokens.Text(text="3"),
              tokens.TemplateParamEquals(), tokens.Text(text="buff"),
              tokens.TemplateParamSeparator(), tokens.Text(text="baff"),
              tokens.TemplateClose()],
             wrap([Template(wrap([Text("foo")]), params=[
                 Parameter(wrap([Text("bar")]), wrap([Text("baz")])),
                 Parameter(wrap([Text("1")]), wrap([Text("biz")]),
                     showkey=False),
                 Parameter(wrap([Text("2")]), wrap([Text("buzz")]),
                     showkey=False),
                 Parameter(wrap([Text("3")]), wrap([Text("buff")])),
                 Parameter(wrap([Text("3")]), wrap([Text("baff")]),
                     showkey=False)])])),
        ]
        for test, valid in tests:
            self.assertWikicodeEqual(valid, self.builder.build(test))

    def test_argument(self):
        """tests for building Argument nodes"""
        tests = [
            ([tokens.ArgumentOpen(), tokens.Text(text="foobar"),
              tokens.ArgumentClose()],
             wrap([Argument(wrap([Text("foobar")]))])),

            ([tokens.ArgumentOpen(), tokens.Text(text="spam"),
              tokens.Text(text="eggs"), tokens.ArgumentClose()],
             wrap([Argument(wrap([Text("spam"), Text("eggs")]))])),

            ([tokens.ArgumentOpen(), tokens.Text(text="foo"),
              tokens.ArgumentSeparator(), tokens.Text(text="bar"),
              tokens.ArgumentClose()],
             wrap([Argument(wrap([Text("foo")]), wrap([Text("bar")]))])),

            ([tokens.ArgumentOpen(), tokens.Text(text="foo"),
              tokens.Text(text="bar"), tokens.ArgumentSeparator(),
              tokens.Text(text="baz"), tokens.Text(text="biz"),
              tokens.ArgumentClose()],
             wrap([Argument(wrap([Text("foo"), Text("bar")]),
                            wrap([Text("baz"), Text("biz")]))])),
        ]
        for test, valid in tests:
            self.assertWikicodeEqual(valid, self.builder.build(test))

    def test_wikilink(self):
        """tests for building Wikilink nodes"""
        pass

    def test_html_entity(self):
        """tests for building HTMLEntity nodes"""
        pass

    def test_heading(self):
        """tests for building Heading nodes"""
        pass

    def test_comment(self):
        """tests for building Comment nodes"""
        pass

    @unittest.skip("holding this until feature/html_tags is ready")
    def test_tag(self):
        """tests for building Tag nodes"""
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)
