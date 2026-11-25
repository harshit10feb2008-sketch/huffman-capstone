"""Huffman Coding File Compression - Capstone Project
Run: python main.py
"""
from collections import Counter
import heapq
import os
import time

class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char, self.freq, self.left, self.right = char, freq, left, right
    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(text):
    if not text:
        return None
    heap = [Node(ch, f) for ch, f in Counter(text).items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        return Node(None, heap[0].freq, heap[0], None)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, Node(None, a.freq+b.freq, a, b))
    return heap[0]

def make_codes(root):
    codes = {}
    def walk(node, path):
        if node is None: return
        if node.char is not None:
            codes[node.char] = path or "0"
            return
        walk(node.left, path+"0")
        walk(node.right, path+"1")
    walk(root, "")
    return codes

def encode(text, codes):
    return "".join(codes[ch] for ch in text)

def decode(bits, root):
    if root is None: return ""
    if root.char is not None: return root.char * len(bits)
    out, node = [], root
    for bit in bits:
        node = node.left if bit == "0" else node.right
        if node.char is not None:
            out.append(node.char)
            node = root
    return "".join(out)

def format_codes(codes):
    return "\\n".join(f"{repr(ch)} : {code}" for ch, code in sorted(codes.items()))

def run():
    print("\\n=== HUFFMAN CODING FILE COMPRESSOR ===")
    print("1. Compress a text file  2. Decode demo text  3. Exit")
    choice = input("Choose: ").strip()
    if choice == "1":
        path = input("Enter text file path: ").strip().strip('"')
        if not os.path.isfile(path):
            print("File not found."); return
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        if not text:
            print("File is empty."); return
        start = time.perf_counter()
        root = build_tree(text)
        codes = make_codes(root)
        bits = encode(text, codes)
        elapsed = time.perf_counter()-start
        output = os.path.splitext(path)[0]+"_compressed.txt"
        with open(output, "w", encoding="utf-8") as f:
            f.write(bits)
        decoded = decode(bits, root)
        print("\\nCharacter codes:\\n", format_codes(codes))
        print(f"\\nOriginal size (UTF-8): {len(text.encode('utf-8'))*8} bits")
        print(f"Encoded size (bit string): {len(bits)} bits")
        print(f"Encoded text file saved: {output}")
        print(f"Decoded successfully: {decoded == text}")
        print(f"Algorithm processing time: {elapsed:.6f} seconds")
        if len(text.encode('utf-8'))*8:
            ratio = len(bits)/(len(text.encode('utf-8'))*8)*100
            print(f"Encoded bits / original UTF-8 bits: {ratio:.2f}% (not including codebook/storage overhead)")
    elif choice == "2":
        sample = "huffman coding is a compression technique"
        root = build_tree(sample)
        codes = make_codes(root)
        bits = encode(sample, codes)
        print("Sample:", sample)
        print("Codes:\\n", format_codes(codes))
        print("Encoded bit string:", bits)
        print("Decoded:", decode(bits, root))
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    run()
