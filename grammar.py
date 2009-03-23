from __future__ import with_statement

class Grammar(object):
  SEP = ':=='
  def __init__(self, filename):
    self.tokens = {}
    self._process_file(filename)

  def _process_file(self, filename):
    self._cur_token = ""
    file = open(filename)
    lines = file.readlines()
    for line in lines:
      self._process_line(line)

  def _process_line(self, line):
    line = line.strip()
    if ":==" in line:
      split_rule = line.partition(":==")
      self._cur_token = split_rule[0].strip()
      line = split_rule[2].strip()
    self._process_rules(line)

  def _process_rules(self, rules):
    for rule in rules.split("|"):
      rule = rule.strip()
      try:
        if rule:
          self.tokens[self._cur_token].append(rule)
      except KeyError:
        self.tokens[self._cur_token] = []
        self.tokens[self._cur_token].append(rule) 


