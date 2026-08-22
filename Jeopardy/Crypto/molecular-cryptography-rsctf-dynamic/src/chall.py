import numpy as np
from secret import flag
from chaotic import generate_sequences

dna_rules = {
    1: {'00': 'A', '11': 'T', '01': 'G', '10': 'C'},
    2: {'00': 'A', '11': 'T', '10': 'G', '01': 'C'},
    3: {'01': 'A', '10': 'T', '00': 'G', '11': 'C'},
    4: {'01': 'A', '10': 'T', '11': 'G', '00': 'C'},
    5: {'10': 'A', '01': 'T', '00': 'G', '11': 'C'},
    6: {'10': 'A', '01': 'T', '11': 'G', '00': 'C'},
    7: {'11': 'A', '00': 'T', '01': 'G', '10': 'C'},
    8: {'11': 'A', '00': 'T', '10': 'G', '01': 'C'}
}

def dna_encode_matrix(P, rule_number):
    rule = dna_rules[rule_number]
    return np.array([
        [rule[f'{num:08b}'[i:i+2]] for num in row for i in range(0, 8, 2)]
        for row in P
    ])

def xor_matrices(matrix1, matrix2, rule_number):
    rule = dna_rules[rule_number]
    rev_rule = {v: k for k, v in rule.items()}
    return np.array([
        [rule[format(int(rev_rule[b1], 2) ^ int(rev_rule[b2], 2), '02b')]
         for b1, b2 in zip(row1, row2)]
        for row1, row2 in zip(matrix1, matrix2)
    ])

def generate_random_keystream(total_bases):
    return np.random.choice(['A', 'C', 'G', 'T'], size=total_bases)

def scramble_matrix(P, lx, ly):
    return P[lx, :][:, ly]

def string_to_matrix(s, num_columns=4):
    ascii_vals = [ord(c) for c in s]
    padded_len = -(-len(ascii_vals) // num_columns) * num_columns
    padded_vals = ascii_vals + [0] * (padded_len - len(ascii_vals))
    return np.array(padded_vals).reshape(-1, num_columns)

def dna_sequence_to_dna_matrix(s, num_columns=16):
    padding_length = (num_columns - len(s) % num_columns) % num_columns
    s_padded = s + 'A' * padding_length
    return np.array(list(s_padded)).reshape(-1, num_columns)

def adjust_sequences(seq, new_length):
    filtered_seq = seq[seq < new_length]
    repeats = -(-new_length // len(filtered_seq))
    return np.tile(filtered_seq, repeats)[:new_length]

if __name__ == "__main__":
    P0 = string_to_matrix(flag)
    rule_number = 3
    dna_encoded_P = dna_encode_matrix(P0, rule_number)
    total_bases = dna_encoded_P.size
    keystream = generate_random_keystream(total_bases)
    key_matrix = keystream.reshape(dna_encoded_P.shape)

    row, col = P0.shape
    lx, ly = generate_sequences(row, 4 * col)
    lx, ly = np.array(lx), np.array(ly)

    scrambled_P = scramble_matrix(dna_encoded_P, lx, ly)
    Pc = xor_matrices(scrambled_P, key_matrix, rule_number)
    print("Encrypted Flag:")
    print(''.join(Pc.flatten()))

    for i in range(1, 3):
        user_input = input(f"Give DNA encryption a try! What do you want to encrypt? ({i}/2)")
        if not all(c in 'ACGT' for c in user_input):
            print("Invalid input")
            continue

        dna_matrix_user = dna_sequence_to_dna_matrix(user_input, num_columns=16)
        data_rows, data_cols = dna_matrix_user.shape
        total_bases_user = data_rows * data_cols

        repeats_key = -(-total_bases_user // total_bases)
        extended_keystream = np.tile(keystream, repeats_key)[:total_bases_user]
        extended_key_matrix = extended_keystream.reshape((data_rows, data_cols))

        lx_user = adjust_sequences(lx, data_rows)
        ly_user = adjust_sequences(ly, data_cols)

        scrambled_user = scramble_matrix(dna_matrix_user, lx_user, ly_user)
        result = xor_matrices(scrambled_user, extended_key_matrix, rule_number)
        print("Encryption Result:")
        print(''.join(result.flatten()))
