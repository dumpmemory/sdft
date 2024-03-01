# Implementation for Self-Distillation Bridges Distribution Gap in Language Model Fine-Tuning

Here is the code for our work [Self-Distillation Bridges Distribution Gap in Language Model Fine-Tuning](https://arxiv.org/abs/2402.13669). 

## Introduction
Fine-tuning LLMs for downstream tasks frequently leads to catastrophic forgetting, negatively affecting models' perfromance on other tasks and alignment. To address the problem, we introduce Self-Distillation Fine-Tuning (SDFT), a novel approach that bridges the distribution gap by guiding fine-tuning with a distilled dataset generated by the model itself to match its original distribution. The workflow of SDFT is shown in the following figure:

<div align='center'><img src="./images/intro.jpg" alt="Workflow of SDFT" width="80%"/></div>

To ensure the quality of distilled responses, we employ simple heuristics. For responses that are not qualified, we preserve original response. 

This selection process is implementd in [eval/gen_distilled_data.py](eval/gen_distilled_data.py). Initially, we exclude responses containing specific words, which typically signify irrelevant repetitions rather than meaningful replies. Subsequently, for datasets pertaining to downstream tasks, we isolate the final answer and remove any that are inconsistent.

To accommodate the self-distillation process, we altered a single line of the source code at `[LLaMA-Factory/src/llmtuner/data/template.py](LLaMA-Factory/src/llmtuner/data/template.py)` on line 92.

## Setup
Clone the repo with submodules:
```bash
git clone --recurse-submodules https://github.com/sail-sg/sdft.git
```

Install all dependencies via:
```bash
pip install -r requirements.txt
pip install -e LLaMA-Factory
pip install -e bigcode-evaluation-harness
```

Our experiments are based on [Llama-2-chat-7b-hf](https://huggingface.co/meta-llama/Llama-2-7b-hf) model, so it is necessary to obtain the appropriate grant.

## Usage
All required bash scripts for replicating the experimental results are located in the [scripts](scripts) directory. Prior to execution, ensure that the `model_path` argument is accurately configured. This argument denotes the identifier on Hugging Face or the local path containing the weights of the language model intended for fine-tuning.

To evaluate the seed language model, execute the following command: `bash scripts/test_seed_LM.sh`

For vanilla fine-tuning on a specific task dataset, use: `bash scripts/[dataset]/sft.sh`

For instance, to fine-tune on the Alpaca dataset, the command is: `bash scripts/alpaca/sft.sh`

Similarly, to perform Self-Distillation Fine (SDFT), the corresponding command is: `bash scripts/[dataset]/sdft.sh`

## Structure
The [data](data) directory houses the datasets utilized for fine-tuning and evaluation. After SDFT, corresponding distilled dataset will be created, denoted by a filename beginning with `distilled`.

The [eval](eval) directory encompasses Python files that are used for evaluation purposes.

The [checkpoints](checkpoints) directory stores the LoRA checkpoints, which are generated subsequent to the fine-tuning process.

Within the [predictions](predictions) directory, one can find the outputs generated for each benchmark following the evaluation phase.

Lastly, the [results](results) directory contains logs of the evaluation results.


## Acknowledgement
Our implementation is based on [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory), for which we are thankful for the exceptional work. For evaluation purposes, we employ tools including [AlpacaEval](https://github.com/tatsu-lab/alpaca_eval), [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness), and [bigcode-evaluation-harness](https://github.com/bigcode-project/bigcode-evaluation-harness). Both AlpacaEval and lm-evaluation-harness are included as dependencies in `requirements.txt`, while LLaMA-Factory and bigcode-evaluation-harness have been integrated as a Git submodule.

To facilitate the self-distillation process, we created a fork of [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) at [this repository](https://github.com/rickyang1114/LLaMA-Factory), incorporating a modification to a single line of code.

The `main` branch has undergone refactoring. To accurately replicate the results presented in the paper, switching to the `reproduce` branch is recommended.

## Citation
If you find our paper helpful, consider citing us via:
```
@article{sdft,
  title={Self-Distillation Bridges Distribution Gap in Language Model Fine-Tuning},
  author={Yang, Zhaorui and Liu, Qian and Pang, Tianyu and Wang, Han and Feng, Haozhe and Zhu, Minfeng and Chen, Wei},
  journal={arXiv preprint arXiv:2402.13669},
  year={2024}
}
```