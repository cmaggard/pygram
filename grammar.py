import re

class Grammar(object):
  def __init__(self, filename):
    self.regex = re.compile("<([-\w]+?)>")
    self.tokens = {}
    self._process_file(filename)
    self._dims = {}
    for x in self.tokens.keys():
      self._dims[x] = len(self.tokens[x])

  def _process_file(self, filename):
    self._cur_token = ""
    file = open(filename)
    lines = file.readlines()
    for line in lines:
      self._process_line(line)

  def _process_line(self, line):
    line = line.strip()
    if "::=" in line:
      split_rule = line.partition("::=")
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

  def _replace(self, expr, match, codon):
    rep_str = self.tokens[match][codon % self._dims[match]]
    return expr.replace(match, rep_str, 1)

  def expand(self, expr, genome):
    l_gen = len(genome)
    new_expr = expr
    idx = 0
    x = self.regex.search(new_expr)
    while x:
      new_expr = self._replace(new_expr, x.group(0), genome[idx])
      idx += 1
      if idx >= l_gen:
        idx %= l_gen
      x = self.regex.search(new_expr)
    return new_expr 

