#!/bin/sh
{
  echo "n"
  echo "subj_fifthRound"
  echo "n"
  echo 0
} | python Query/QueryCaller/QueryCaller.py
{
  echo "n"
  echo "subj_firstRound"
  echo "n"
  echo 0
} | python Query/QueryCaller/QueryCaller.py

{
  echo "n"
  echo "1.1_firstRound"
  echo "n"
  echo 1
} | python Query/QueryCaller/QueryCaller.py
{
  echo "n"
  echo "1.3_firstRound"
  echo "n"
  echo 2
} | python Query/QueryCaller/QueryCaller.py
{
  echo "n"
  echo "1.3.1_firstRound"
  echo "n"
  echo 3
} | python Query/QueryCaller/QueryCaller.py
{
  echo "n"
  echo "1.4_firstRound"
  echo "n"
  echo 4
} | python Query/QueryCaller/QueryCaller.py
{
  echo "n"
  echo "1.7_firstRound"
  echo "n"
  echo 5
} | python Query/QueryCaller/QueryCaller.py
{
  echo "n"
  echo "1.7.1_firstRound"
  echo "n"
  echo 6
} | python Query/QueryCaller/QueryCaller.py