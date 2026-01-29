import math
from typing import List, Dict, Sequence


class VectorUtil:
    @staticmethod
    def norm(vec: Sequence[float]) -> float:
        sum_sq = 0.0
        for val in vec:
            sum_sq += val * val
        return math.sqrt(sum_sq)

    @staticmethod
    def normalize(vec: Sequence[float]) -> List[float]:
        vec_norm = VectorUtil.norm(vec)
        if vec_norm == 0.0:
            return [0.0 for _ in vec]
        return [val / vec_norm for val in vec]

    @staticmethod
    def similarity(vector_1: Sequence[float], vector_2: Sequence[float]) -> float:
        norm_vec1 = VectorUtil.normalize(vector_1)
        norm_vec2 = VectorUtil.normalize(vector_2)
        dot_product = 0.0
        for a, b in zip(norm_vec1, norm_vec2):
            dot_product += a * b
        return dot_product

    @staticmethod
    def cosine_similarities(
        vector_1: Sequence[float],
        vectors_all: List[Sequence[float]]
    ) -> List[float]:
        similarities: List[float] = []
        norm_vec1 = VectorUtil.norm(vector_1)

        for vec in vectors_all:
            norm_vec_all = VectorUtil.norm(vec)
            if norm_vec_all == 0.0:
                similarities.append(0.0)
                continue
            dot_product = 0.0
            for a, b in zip(vec, vector_1):
                dot_product += a * b
            similarity = dot_product / (norm_vec1 * norm_vec_all)
            similarities.append(similarity)

        return similarities

    @staticmethod
    def n_similarity(
        vector_list_1: List[Sequence[float]],
        vector_list_2: List[Sequence[float]]
    ) -> float:
        if not vector_list_1 or not vector_list_2:
            raise ValueError("At least one of the lists is empty.")

        dim = len(vector_list_1[0])
        mean_vec1 = [0.0] * dim
        mean_vec2 = [0.0] * dim

        for vec in vector_list_1:
            for i in range(dim):
                mean_vec1[i] += vec[i]

        for vec in vector_list_2:
            for i in range(dim):
                mean_vec2[i] += vec[i]

        for i in range(dim):
            mean_vec1[i] /= len(vector_list_1)
            mean_vec2[i] /= len(vector_list_2)

        return VectorUtil.similarity(mean_vec1, mean_vec2)

    @staticmethod
    def compute_idf_weight_dict(
        total_num: int,
        number_dict: Dict[str, float]
    ) -> Dict[str, float]:
        result: Dict[str, float] = {}
        for key, count in number_dict.items():
            idf = math.log((total_num + 1.0) / (count + 1.0))
            result[key] = idf
        return result
