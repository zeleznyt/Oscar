import json
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default='oscar/output/split_statistics', type=str, required=False)
    args = parser.parse_args()

    dir_list = [os.path.join(args.data_dir, i) for i in os.listdir(args.data_dir) if os.path.isdir(os.path.join(args.data_dir, i))]
    for directory in dir_list:
        results = {}
        for checkpoint in os.listdir(directory):
            checkpoint_dir = os.path.join(directory, checkpoint)
            if not os.path.isdir(checkpoint_dir):
                continue
            for file in os.listdir(checkpoint_dir):
                if 'val' in file and 'eval.json' in file:
                    eval_file = os.path.join(checkpoint_dir, file)
                    break
            else:
                print('No eval file was found in {}'.format(checkpoint_dir))
                continue
            with open(eval_file, 'r') as f:
                eval_scores = json.load(f)
            if len(results) == 0:
                for key in eval_scores:
                    results[key] = [eval_scores[key]]
                results['checkpoint'] = [checkpoint.split('/')[-1]]
            else:
                for key in eval_scores:
                    results[key].append(eval_scores[key])
                results['checkpoint'].append(checkpoint.split('/')[-1])
        with open(os.path.join(directory, 'evaluation.json'), 'w') as f:
            json.dump(results, f)
        print('Evaluation with length {} saved in {}'.format(len(results), directory))

