def detect_mutations(aligned_ref, aligned_seq):
    mutations = []
    ref_pos = 0  # 1-based tracking for the reference sequence

    for i in range(len(aligned_ref)):
        ref_char = aligned_ref[i]
        seq_char = aligned_seq[i]

        if ref_char != '-':
            ref_pos += 1  # Increment reference position for real bases

        # 1. Insertion (Gap in reference, base in sample)
        if ref_char == '-' and seq_char != '-':
            mutations.append({
                "Position": ref_pos,
                "Type": "Insertion",
                "Ref": "-",
                "Alt": seq_char
            })

        # 2. Deletion (Base in reference, gap in sample)
        elif ref_char != '-' and seq_char == '-':
            mutations.append({
                "Position": ref_pos,
                "Type": "Deletion",
                "Ref": ref_char,
                "Alt": "-"
            })

        # 3. Substitution (Base mismatch, neither is a gap)
        elif ref_char != '-' and seq_char != '-' and ref_char != seq_char:
            mutations.append({
                "Position": ref_pos,
                "Type": "Substitution",
                "Ref": ref_char,
                "Alt": seq_char
            })

    return mutations
