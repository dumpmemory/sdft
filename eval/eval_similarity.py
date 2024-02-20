import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm  

import argparse
from sentence_transformers import SentenceTransformer, util
from utils import get_outputs
plt.figure(figsize=(10, 7.5))
plt.rcParams['font.size'] = 26
font_path = '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'
font_prop = fm.FontProperties(fname=font_path)  
plt.rcParams['font.family'] = font_prop.get_name()  

def get_similairy_array(encoder, outputs_1, outputs_2):
    assert len(outputs_1) == len(outputs_2)
    similarity_array = np.zeros(len(outputs_1))
    for idx, (output_1, output_2) in enumerate(zip(outputs_1, outputs_2)):
        embeddings1 = encoder.encode(output_1, convert_to_tensor=True)
        embeddings2 = encoder.encode(output_2, convert_to_tensor=True)
        cosine_similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
        similarity_array[idx] = cosine_similarity.item()
    return similarity_array
  
def draw(sft_similarity_array, distill_similarity_array):  
    plt.hist(  
        sft_similarity_array,  
        color="#A16058",  
        bins=30,  
        alpha=0.7,  
        label="Vanilla FT",  
    )  
    plt.hist(  
        distill_similarity_array,  
        color="#85BFAC",  
        bins=30,  
        alpha=0.7,  
        label="SDFT",  
    )  
      
    sft_mean = sft_similarity_array.mean()  
    distill_mean = distill_similarity_array.mean()  
      
    plt.scatter([sft_mean], [0], color="#A16058", s=200, label="Vanilla FT Mean", zorder=5)  
    plt.scatter([distill_mean], [0], color="#616C6E", s=200, label="SDFT Mean", zorder=5)  
      
    plt.text(sft_mean, plt.ylim()[1]*0.05, f'{sft_mean:.2f}', color="#A16058", ha='center')  
    plt.text(distill_mean, plt.ylim()[1]*0.05, f'{distill_mean:.2f}', color="#616C6E", ha='center')  
      
    plt.legend()  
    plt.xlabel("Embedding Similarity to Original Model")  
    plt.ylabel("Count")  
    plt.tight_layout(pad=1)  
      
    plt.savefig("similarity.pdf")


def main(dataset, instruction_dataset):
    origin_file = f"predictions/origin/{instruction_dataset}/generated_predictions.jsonl"
    sft_file = f"predictions/{dataset}/sft/{instruction_dataset}/generated_predictions.jsonl"
    distill_file = f"predictions/{dataset}/distill-using/{instruction_dataset}/generated_predictions.jsonl"
    encoder = SentenceTransformer("all-MiniLM-L6-v2")
    origin_outputs = get_outputs(origin_file)
    sft_outputs = get_outputs(sft_file)
    distill_outputs = get_outputs(distill_file)
    sft_similarity_array = get_similairy_array(encoder, origin_outputs, sft_outputs)
    distill_similarity_array = get_similairy_array(encoder, origin_outputs, distill_outputs)
    mean_similarity = np.mean(sft_similarity_array)
    distill_similarity = np.mean(distill_similarity_array)
    draw(sft_similarity_array, distill_similarity_array)
    print(f"sft similarity: {mean_similarity:.4f}")
    print(f"distill similarity: {distill_similarity:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--instruction_dataset", type=str, default="advbench")
    args = parser.parse_args()
    main(args.dataset, args.instruction_dataset)
