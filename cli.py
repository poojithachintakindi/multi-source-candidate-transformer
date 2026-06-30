"""Simple CLI to run the pipeline."""
import argparse
import json
from pipeline import runner


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--inputs', nargs='+', required=True)
    p.add_argument('--config', default=None)
    p.add_argument('--out', default=None)
    args = p.parse_args()
    config = {}
    if args.config:
        with open(args.config, encoding='utf-8') as fh:
            config = json.load(fh)
    result = runner.run(args.inputs, config)
    out_text = json.dumps(result, indent=2)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as fh:
            fh.write(out_text)
    else:
        print(out_text)


if __name__ == '__main__':
    main()
