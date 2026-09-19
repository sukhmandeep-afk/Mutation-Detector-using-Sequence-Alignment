def align_sequences(seq1, seq2, match=2, mismatch=-1, gap=-2):
    n, m = len(seq1), len(seq2)
    
    # Initialize DP matrix and Traceback matrix
    score = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        score[i][0] = i * gap
    for j in range(m + 1):
        score[0][j] = j * gap
        
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match_score = score[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            delete_score = score[i-1][j] + gap
            insert_score = score[i][j-1] + gap
            score[i][j] = max(match_score, delete_score, insert_score)
            
    # Traceback
    align1, align2 = [], []
    i, j = n, m
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and score[i][j] == score[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch):
            align1.append(seq1[i-1])
            align2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and score[i][j] == score[i-1][j] + gap:
            align1.append(seq1[i-1])
            align2.append('-')
            i -= 1
        else:
            align1.append('-')
            align2.append(seq2[j-1])
            j -= 1
            
    return ''.join(reversed(align1)), ''.join(reversed(align2)), score[n][m]
