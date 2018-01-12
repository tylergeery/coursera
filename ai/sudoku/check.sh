while read line; do
  if ! read -u 3 line2
  then
    break
  fi
  python3 driver_3.py $line2
  solution=$(head -1 output.txt)

  if [[ $line == $solution ]]; then
    printf "\e[1;32m%s\n%s\n\n\e[m" "$line" "$solution"
  else
    printf "\e[1;31m%s\n%s\n\n\e[m" "$line" "$solution"
  fi

done < sudokos_finish.txt 3< sudokus_start.txt
