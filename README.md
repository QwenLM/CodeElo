# CodeElo

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2501.01257" target="_blank" style="margin: 2px;">
    <img alt="" src="https://img.shields.io/badge/Paper-gray?logo=arxiv" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://huggingface.co/datasets/Qwen/CodeElo" target="_blank" style="margin: 2px;">
    <img alt="" src="https://img.shields.io/badge/🤗%20%20Dataset-gray" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://codeelo-bench.github.io/" target="_blank" style="margin: 2px;">
    <img alt="" src="https://img.shields.io/badge/🏆%20%20Leaderboard-gray" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>


This repository is used to evaluate a model's competition-level code generation abilities on [CodeForces](https://codeforces.com/) with human-comparable Elo ratings and percentiles among humans, using the method proposed in [CodeElo: Benchmarking Competition-level Code Generation of LLMs with Human-comparable Elo Ratings](https://arxiv.org/abs/2501.01257).


> [!IMPORTANT]
> Due to ethical considerations, you need to agree to the AGREEMENT to obtain a token and server ip to use the repository. Please fill in the blanks and email the letter to `binyuan.hby@alibaba-inc.com`, and we will review it and respond as soon as possible.

### Quick Start

1. Send a request via email to obtain your access `TOKEN`, then set `TOKEN` variable in environment.
   
    ```bash
    export TOKEN="your_actual_token" # replace with your actual token
    export BASE_URL="your_base_url" # replace with base url
    ```

2. To test a local model, you need first host an LLM server. Here's an example:

    ```bash
    vllm serve Qwen/Qwen2.5-Coder-7B-Instruct
    ```

    If you're testing models via a third-party API, you can modify the `get_response` function with your custom calling method in `llm_client`.

3. To test the model, use the following command:

    ```bash
    python main.py --model Qwen/Qwen2.5-Coder-7B-Instruct \
        --bid 2000 --eid 2030
    ```

    This command will test all eligible contests with IDs ranging from 2000 to 2030.

### API

We have open-sourced all of the Elo calculation logic and ranking methods. The `BASE_URL` provided here points to our automated submission system. In order to prevent meaningless mass submissions and to comply with CodeForces policies, we require verified submissions. If you prefer not to use our automated system, you are free to implement your own submission mechanism by configuring the interfaces in `api.py`


### Citation
```
@article{quan2025codeelo,
  title={CodeElo: Benchmarking Competition-level Code Generation of LLMs with Human-comparable Elo Ratings},
  author={Quan, Shanghaoran and Yang, Jiaxi and Yu, Bowen and Zheng, Bo and Liu, Dayiheng and Yang, An and Ren, Xuancheng and Gao, Bofei and Miao, Yibo and Feng, Yunlong and others},
  journal={arXiv preprint arXiv:2501.01257},
  year={2025}
}
```