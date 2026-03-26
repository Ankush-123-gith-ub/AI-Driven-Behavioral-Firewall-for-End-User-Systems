import math

def calculate_entropy(file_path, chunk_size=8192):
    try:
        with open(file_path, "rb") as f:
            byte_counts = [0] * 256
            total_bytes = 0

            while chunk := f.read(chunk_size):
                total_bytes += len(chunk)
                for byte in chunk:
                    byte_counts[byte] += 1

        if total_bytes == 0:
            return 0.0

        entropy = 0.0
        for count in byte_counts:
            if count == 0:
                continue
            probability = count / total_bytes
            entropy -= probability * math.log2(probability)

        return entropy

    except Exception:
        return 0.0