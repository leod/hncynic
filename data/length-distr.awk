#!/usr/bin/awk -f

{
  if (NF > max_len) {
    max_len = NF;
    a[NF] = 0;
  }
  a[NF] += 1;
  sum += 1;
}
END {
  for (i = 1; i <= max_len; i++)
      printf "%d %.18f\n", i, a[i]/sum
}
