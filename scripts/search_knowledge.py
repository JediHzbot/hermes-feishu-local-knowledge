"""Read-only literal search of UTF-8 Markdown; emits relative source paths."""

import argparse
import json
import os
import stat
from pathlib import Path


def is_link(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, 'st_file_attributes', 0)
        & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0)
    )


def search(root, query, limit):
    results, errors = [], []
    folded = query.casefold()

    def walk_error(error):
        try:
            relative = str(Path(error.filename).relative_to(root))
        except (TypeError, ValueError):
            relative = '.'
        errors.append({'path': relative, 'error': type(error).__name__})

    for directory, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        safe_dirs = []
        for name in sorted(dirs):
            entry = Path(directory) / name
            try:
                if not name.startswith('.') and not is_link(entry):
                    safe_dirs.append(name)
            except OSError as error:
                walk_error(error)
        dirs[:] = safe_dirs
        for name in sorted(files):
            if not name.lower().endswith('.md'):
                continue
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            try:
                if is_link(path):
                    continue
                with path.open(encoding='utf-8-sig') as stream:
                    for number, line in enumerate(stream, 1):
                        if folded in line.casefold():
                            if len(results) < limit:
                                results.append({'path': relative, 'line': number,
                                                'snippet': line.strip()[:400]})
                            break
            except (OSError, UnicodeError) as error:
                errors.append({'path': relative, 'error': type(error).__name__})
    return {'results': results, 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--query', required=True)
    parser.add_argument('--limit', type=int, default=5)
    args = parser.parse_args()
    if not args.query.strip() or not 1 <= args.limit <= 100:
        parser.error('query must be nonempty; limit must be between 1 and 100')
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error('authorized knowledge root does not exist or is not a directory')
    report = search(root, args.query, args.limit)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
