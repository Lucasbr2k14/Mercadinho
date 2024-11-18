def table(fildsName, values):
  
  filds_len = []

  for fildNum in range(len(fildsName)):
    filds_len.append(len(fildsName[fildNum]))

  for fildNum in range(len(fildsName)):

    for prodNum in range(len(values)):

      lenFild = len(str(values[prodNum][fildNum]))
      
      if lenFild > filds_len[fildNum]:
        filds_len[fildNum] = lenFild
  

  lines = []

  top_line = "+"

  for i in range(len(fildsName)):
    top_line += '-'*filds_len[i] + '+'

  lines.append(top_line)

  segund_line = "|"

  for i in range(len(fildsName)):
    segund_line += fildsName[i] + ' ' * (filds_len[i] - len(fildsName[i])) + '|'

  lines.append(segund_line)
  lines.append(top_line)

  for i in range(len(values)):
    line = '|'
    for j in range(len(fildsName)):
      line += str(values[i][j]) + ' ' * (filds_len[j] - len(str(values[i][j]))) + '|'
    lines.append(line)

  lines.append(top_line)

  return '\n'.join(lines)