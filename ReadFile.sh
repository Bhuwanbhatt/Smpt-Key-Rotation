#!/bin/bash
input="password.txt"
while IFS= read -r line
do
  echo "$line"
done < "$input"
