# -*- coding: utf-8 -*-
from __future__ import with_statement

import platform
import tempfile

import pexpect
import unittest
import PexpectTestCase

# the program cat(1) may display ^D\x08\x08 when \x04 (EOF, Ctrl-D) is sent
_CAT_EOF = '^D\x08\x08'

class UnicodeTests(PexpectTestCase.PexpectTestCase):
    def test_expect_basic (self):
        p = pexpect.spawnu('cat')
        p.sendline(u'Hello')
        p.sendline(u'there')
        p.sendline(u'Mr. þython') # þ is more like th than p, but never mind
        p.expect(u'Hello')
        p.expect(u'there')
        p.expect(u'Mr. þython')
        p.sendeof ()
        p.expect (pexpect.EOF)

    def test_expect_exact_basic (self):
        p = pexpect.spawnu('cat')
        p.sendline(u'Hello')
        p.sendline(u'there')
        p.sendline(u'Mr. þython')
        p.expect_exact(u'Hello')
        p.expect_exact(u'there')
        p.expect_exact(u'Mr. þython')
        p.sendeof()
        p.expect_exact (pexpect.EOF)

    def test_expect_echo (self):
        '''This tests that echo can be turned on and off.
        '''
        p = pexpect.spawnu('cat', timeout=10)
        self._expect_echo(p)

    def test_expect_echo_exact (self):
        '''Like test_expect_echo(), but using expect_exact().
        '''
        p = pexpect.spawnu('cat', timeout=10)
        p.expect = p.expect_exact
        self._expect_echo(p)

    def _expect_echo (self, p):
        p.sendline(u'1234') # Should see this twice (once from tty echo and again from cat).
        index = p.expect ([u'1234', u'abcdé', u'wxyz', pexpect.EOF, pexpect.TIMEOUT])
        assert index == 0, (index, p.before)
        index = p.expect ([u'1234', u'abcdé', u'wxyz', pexpect.EOF])
        assert index == 0, index
        p.setecho(0) # Turn off tty echo
        p.sendline(u'abcdé') # Now, should only see this once.
        p.sendline(u'wxyz') # Should also be only once.
        index = p.expect ([pexpect.EOF,pexpect.TIMEOUT, u'abcdé', u'wxyz', u'1234'])
        assert index == 2, index
        index = p.expect ([pexpect.EOF, u'abcdé', u'wxyz', u'7890'])
        assert index == 2, index
        p.setecho(1) # Turn on tty echo
        p.sendline (u'7890') # Should see this twice.
        index = p.expect ([pexpect.EOF, u'abcdé', u'wxyz', u'7890'])
        assert index == 3, index
        index = p.expect ([pexpect.EOF, u'abcdé', u'wxyz', u'7890'])
        assert index == 3, index
        p.sendeof()

    def test_log_unicode(self):
        msg = u"abcΩ÷"
        filename_send = tempfile.mktemp()
        filename_read = tempfile.mktemp()
        p = pexpect.spawnu('cat')
        if platform.python_version_tuple() < ('3', '0', '0'):
            import codecs
            def open(fname, mode, **kwargs):
                if 'newline' in kwargs:
                    del kwargs['newline']
                return codecs.open(fname, mode, **kwargs)
        else:
            import io
            open = io.open

        p.logfile_send = open(filename_send, 'w', encoding='utf-8')
        p.logfile_read = open(filename_read, 'w', encoding='utf-8')
        p.sendline(msg)
        p.sendeof()
        p.expect(pexpect.EOF)
        p.close()
        p.logfile_send.close()
        p.logfile_read.close()

        # ensure the 'send' log is correct,
        with open(filename_send, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), msg + u'\n\x04')

        # ensure the 'read' log is correct,
        with open(filename_read, 'r', encoding='utf-8', newline='') as f:
            output = f.read().replace(_CAT_EOF, u'')
            self.assertEqual(output, (msg + u'\r\n')*2 )


    def test_spawn_expect_ascii_unicode(self):
        # A bytes-based spawn should be able to handle ASCII-only unicode, for
        # backwards compatibility.
        p = pexpect.spawn('cat')
        p.sendline('Camelot')
        p.expect('Camelot')

        p.sendline('Aargh')
        p.sendline('Aårgh')
        p.expect_exact('Aargh')

        p.sendeof()
        p.expect(pexpect.EOF)

    def test_spawn_send_unicode(self):
        # A bytes-based spawn should be able to send arbitrary unicode
        p = pexpect.spawn('cat')
        p.sendline('3½')
        p.sendeof()
        p.expect(pexpect.EOF)

if __name__ == '__main__':
    unittest.main()

suite = unittest.makeSuite(UnicodeTests, 'test')