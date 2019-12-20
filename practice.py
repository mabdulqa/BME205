seq1 = 'GGCTT'
seq2 = 'CTTACCA'
seq = "Lol"

if seq1[-3:] == seq2[:3]:
        seq = seq1 + seq2[3:]

print(seq1[-3:])
print(seq2[:3])
print(seq)