#!/usr/bin/env python
'''
PEXPECT LICENSE

    This license is approved by the OSI and FSF as GPL-compatible.
        http://opensource.org/licenses/isc-license.txt

    Copyright (c) 2012, Noah Spurrier <noah@noah.org>
    PERMISSION TO USE, COPY, MODIFY, AND/OR DISTRIBUTE THIS SOFTWARE FOR ANY
    PURPOSE WITH OR WITHOUT FEE IS HEREBY GRANTED, PROVIDED THAT THE ABOVE
    COPYRIGHT NOTICE AND THIS PERMISSION NOTICE APPEAR IN ALL COPIES.
    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

'''
from __future__ import with_statement

import unittest, time, sys
import pexpect
import PexpectTestCase

from pexpect import six

# This isn't exactly a unit test, but it fits in nicely with the rest of the tests.

class PerformanceTestCase (PexpectTestCase.PexpectTestCase):

    '''Testing the performance of expect, with emphasis on wading through long
    inputs. '''

    def plain_range(self, n):
        e = pexpect.spawn('python')
        self.assertEqual(e.expect(six.b('>>>')), 0)
        e.sendline(six.b('for n in range(1, %d+1): print(n)' % n))
        self.assertEqual(e.expect(six.b(r'\.{3}')), 0)
        e.sendline(six.b(''))
        self.assertEqual(e.expect([six.b('inquisition'), six.b('%d' % n)]), 1)

    def window_range(self, n):
        e = pexpect.spawn('python')
        self.assertEqual(e.expect(six.b('>>>')), 0)
        e.sendline(six.b('for n in range(1, %d+1): print(n)' % n))
        self.assertEqual(e.expect(r'\.{3}'), 0)
        e.sendline(six.b(''))
        self.assertEqual(e.expect([six.b('inquisition'), six.b('%d' % n)], searchwindowsize=10), 1)

    def exact_range(self, n):
        e = pexpect.spawn('python')
        self.assertEqual(e.expect_exact([six.b('>>>')]), 0)
        e.sendline(six.b('for n in range(1, %d+1): print(n)' % n))
        self.assertEqual(e.expect_exact([six.b('...')]), 0)
        e.sendline(six.b(''))
        self.assertEqual(e.expect_exact([six.b('inquisition'), six.b('%d' % n)],timeout=520), 1)

    def ewin_range(self, n):
        e = pexpect.spawn('python')
        self.assertEqual(e.expect_exact([six.b('>>>')]), 0)
        e.sendline(six.b('for n in range(1, %d+1): print(n)' % n))
        self.assertEqual(e.expect_exact([six.b('...')]), 0)
        e.sendline(six.b(''))
        self.assertEqual(e.expect_exact([six.b('inquisition'), six.b('%d' % n)], searchwindowsize=10), 1)

    def faster_range(self, n):
        e = pexpect.spawn('python')
        self.assertEqual(e.expect(six.b('>>>')), 0)
        e.sendline(six.b('range(1, %d+1)' % n))
        self.assertEqual(e.expect([six.b('inquisition'), six.b('%d' % n)]), 1)

    def test_100000(self):
        start_time = time.time()
        self.plain_range (100000)
        six.print_("100000 calls to plain_range:", (time.time() - start_time))
        start_time = time.time()
        self.window_range(100000)
        six.print_("100000 calls to window_range:", (time.time() - start_time))
        start_time = time.time()
        self.exact_range (100000)
        six.print_("100000 calls to exact_range:", (time.time() - start_time))
        start_time = time.time()
        self.ewin_range  (100000)
        six.print_("100000 calls to ewin_range:", (time.time() - start_time))
        start_time = time.time()
        self.faster_range(100000)
        six.print_("100000 calls to faster_range:", (time.time() - start_time))

if __name__ == "__main__":
    unittest.main()

suite = unittest.makeSuite(PerformanceTestCase,'test')