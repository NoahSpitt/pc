"""Simple shell simulator."""

import os
import shlex
import readline
from typing import Dict, Set

from pc_sim import VirtualPC
from builder import PCBuilder


class VirtualFileSystem:
    def __init__(self):
        self.fs: Dict[str, str] = {}
        self.dirs: Set[str] = {"/"}
        self.cwd = "/"

    def _path(self, path: str) -> str:
        if path.startswith('/'):
            return os.path.normpath(path)
        return os.path.normpath(os.path.join(self.cwd, path))

    def _ensure_dir(self, path: str) -> bool:
        return path in self.dirs

    def ls(self, path: str = '.'):
        prefix = self._path(path)
        prefix = prefix.rstrip('/')
        entries = set()
        for d in self.dirs:
            if d != prefix and d.startswith(prefix + '/'):
                rest = d[len(prefix) + 1:]
                if '/' not in rest:
                    entries.add(rest + '/')
        for f in self.fs:
            if f.startswith(prefix + '/'):
                rest = f[len(prefix) + 1:]
                if '/' not in rest:
                    entries.add(rest)
        for e in sorted(entries):
            print(e)

    def cat(self, path: str):
        p = self._path(path)
        if p in self.fs:
            print(self.fs[p])
        else:
            print("File not found")

    def echo(self, text: str, path: str):
        p = self._path(path)
        dir_path = os.path.dirname(p)
        if not self._ensure_dir(dir_path):
            print('Directory not found')
            return
        self.fs[p] = text

    def cd(self, path: str):
        new = self._path(path)
        if new in self.dirs:
            self.cwd = new
        else:
            print('Directory not found')

    def mkdir(self, path: str):
        p = self._path(path)
        if p in self.dirs:
            print('Directory already exists')
        else:
            parent = os.path.dirname(p)
            if self._ensure_dir(parent):
                self.dirs.add(p)
            else:
                print('Parent directory does not exist')

    def touch(self, path: str):
        p = self._path(path)
        dir_path = os.path.dirname(p)
        if self._ensure_dir(dir_path):
            self.fs.setdefault(p, '')
        else:
            print('Directory not found')

    def rm(self, path: str):
        p = self._path(path)
        if p in self.fs:
            del self.fs[p]
        elif p in self.dirs and p != '/':
            self.dirs.remove(p)
        else:
            print('No such file or directory')

    def mv(self, src: str, dst: str):
        s = self._path(src)
        d = self._path(dst)
        if s in self.fs:
            dir_path = os.path.dirname(d)
            if not self._ensure_dir(dir_path):
                print('Destination directory not found')
                return
            self.fs[d] = self.fs.pop(s)
        elif s in self.dirs:
            if not self._ensure_dir(os.path.dirname(d)):
                print('Destination directory not found')
                return
            # move directory
            for path in list(self.fs.keys()):
                if path.startswith(s + '/'):
                    new_path = d + path[len(s):]
                    self.fs[new_path] = self.fs.pop(path)
            for path in list(self.dirs):
                if path.startswith(s + '/') or path == s:
                    new_dir = d + path[len(s):]
                    self.dirs.add(new_dir)
            self.dirs.discard(s)
        else:
            print('No such file or directory')

    def cp(self, src: str, dst: str):
        s = self._path(src)
        d = self._path(dst)
        if s in self.fs:
            dir_path = os.path.dirname(d)
            if not self._ensure_dir(dir_path):
                print('Destination directory not found')
                return
            self.fs[d] = self.fs[s]
        else:
            print('Source file not found')


class Shell:
    PROMPT = "$ "

    def __init__(self, pc_config_name: str):
        builder = PCBuilder()
        cfg = builder.load_config(pc_config_name)
        self.pc = VirtualPC(cfg)
        self.fs = VirtualFileSystem()
        self.config_name = pc_config_name

    def loop(self):
        while True:
            try:
                line = input(self.PROMPT)
            except EOFError:
                break
            if not line:
                continue
            args = shlex.split(line)
            if not args:
                continue
            cmd = args[0]
            if cmd == 'exit':
                break
            elif cmd == 'ls':
                path = args[1] if len(args) > 1 else '.'
                self.fs.ls(path)
            elif cmd == 'cd':
                path = args[1] if len(args) > 1 else '/'
                self.fs.cd(path)
            elif cmd == 'cat':
                if len(args) > 1:
                    self.fs.cat(args[1])
                else:
                    print("Usage: cat <file>")
            elif cmd == 'echo':
                if len(args) >= 3 and args[-2] == '>':
                    text = ' '.join(args[1:-2])
                    self.fs.echo(text, args[-1])
                else:
                    print('Usage: echo <text> > <file>')
            elif cmd == 'mkdir':
                if len(args) > 1:
                    self.fs.mkdir(args[1])
                else:
                    print('Usage: mkdir <dir>')
            elif cmd == 'touch':
                if len(args) > 1:
                    self.fs.touch(args[1])
                else:
                    print('Usage: touch <file>')
            elif cmd == 'rm':
                if len(args) > 1:
                    self.fs.rm(args[1])
                else:
                    print('Usage: rm <path>')
            elif cmd == 'mv':
                if len(args) == 3:
                    self.fs.mv(args[1], args[2])
                else:
                    print('Usage: mv <src> <dst>')
            elif cmd == 'cp':
                if len(args) == 3:
                    self.fs.cp(args[1], args[2])
                else:
                    print('Usage: cp <src> <dst>')
            elif cmd == 'run':
                if len(args) == 3:
                    ram = int(args[1])
                    cycles = int(args[2])
                    self.pc.run_program(ram, cycles)
                else:
                    print('Usage: run <ram_gb> <cycles>')
            elif cmd == 'download':
                if len(args) == 2:
                    size = int(args[1])
                    self.pc.download(size)
                else:
                    print('Usage: download <size_mb>')
            elif cmd == 'free':
                print(f"{self.pc.used_ram_gb}/{self.pc.total_ram_gb} GB used")
            elif cmd == 'cpuinfo':
                print(self.pc.info())
            else:
                print(f"Unknown command: {cmd}")


