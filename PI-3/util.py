def converter(n):
  out = 0
  for bit in n:
    out = (out << 1) | bit

  return out